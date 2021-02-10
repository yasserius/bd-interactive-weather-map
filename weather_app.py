
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State

import json

# ------------------------------------------------------------------------------

app = dash.Dash(__name__,
                external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'])
server = app.server

app.title = "Bangladesh Interactive Map"

# ------------------------------------------------------------------------------

df = pd.read_csv('weather_data_cleaned.csv', index_col=0, header=0)

years = df['year'].unique().tolist()

geojson_path = 'small_bangladesh_geojson_adm2_64_districts_zillas.json'

with open(geojson_path) as f:
    shapes = json.load(f)

# ------------------------------------------------------------------------------

import plotly.express as px

colorscales = {
    'max_temp': 'Hot_r',
    'min_temp': 'Blues_r',
    'humidity': 'Mint',
    'rainfall': 'dense',
}

titles = {
    'max_temp': 'Maximum temperature (degree celsius)',
    'min_temp': 'Minimum temperature (degree celsius)',
    'humidity': 'Humidity (%)',
    'rainfall': 'Rainfall (millimeter)',
}

labels = {
    'max_temp': 'Maximum temperature',
    'min_temp': 'Minimum temperature',
    'humidity': 'Humidity',
    'rainfall': 'Rainfall',
}



def get_map(dataframe,
            geojson,
            column='max_temp',
            locations='zila',
            feature_id_key='properties.ADM2_EN'):
    colorscale = colorscales[column]
    max_val = dataframe[column].max()
    min_val = dataframe[column].min()
    fig = px.choropleth(dataframe, geojson=geojson, color=column,
                        labels={
                            column: labels[column],
                            'zila': "Zila",
                        },
                        # title=titles[column],
                        color_continuous_scale=colorscale,
                        range_color=(min_val, max_val),
                        locations=locations, featureidkey=feature_id_key,
                        projection="mercator", scope="asia")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30})
    fig.update_layout(title_text=titles[column], title_x=0.5)

    return fig

# ------------------------------------------------------------------------------

title_section = html.Div(children=[

    html.H1(children="Bangladesh Interactive Map",
            style={
                'margin': 30,
                'margin-bottom': 10,
                'color': '#346eeb',
            }),

    html.P(children="Choropleth (heatmap) of weather data from 2011 Census by Bangladesh Bureau of Statitics",
            style={
                'margin': '5px 30px',
                'color': '#8f939c',
            }),

], className='col-md-9',
style= {
    'display': 'inline-block',
    'vertical-align': 'top'
})

logo_section = html.Div(children=[

    html.A(children="view code",
            href='#',
            style={
                # 'padding': 30,
                'font-weight': 'thin',
                'text-transform': 'uppercase',
                'margin': 'auto',
                'background-color': 'grey',
                'color': 'white',
                'padding': '2px 4px',
                'border-radius': 3,
            }),

], className='col-md-3',
style= {
    'display': 'inline-block',
    'vertical-align': 'top',
    'text-align': 'right',
    'padding-top': 20,
})

header = html.Div(children=[

    title_section,

    logo_section

], className='row')

# ------------------------------------------------------------------------------

dropdown1 = html.Div(
    [
        html.Div('Plot type:', style={'padding-bottom': 5}),

        dcc.Dropdown(
            id='type',
            options=[
                {'label': 'Maximum Temperature', 'value': 'max_temp'},
                {'label': 'Minimum Temperature', 'value': 'min_temp'},
                {'label': 'Humidity', 'value': 'humidity'},
                {'label': 'Rainfall', 'value': 'rainfall'},
            ],
            value='max_temp',
            style={
                'padding-bottom': 5,
                'width': '30%',
                'min-width': 250,

            }
        ),
    ], className='',
     style={
        'padding': '10px 20px',
        'display': 'inline-block',
        'vertical-align': 'top',}
)

avgbox = html.Div(
    [
        html.Div('Average',
        style={
         'padding-bottom': 5,
         'font-weight': 'bold',
         'text-transform': 'uppercase',}),

        html.Div(children='',
        style={
            # 'padding-bottom': 5,
            'font-size': 30,

        },
        id='average'),

        html.Div(children='',
        style={
            # 'padding-bottom': 5,
            'font-size': 10,
            'text-transform': 'uppercase',

        },
        id='unit'),

    ], className='',
     style={
        'padding': '10px 20px',
        'display': 'inline-block',
        'vertical-align': 'top',
        'width': '30%',
        'min-width': 250,
    })

graph = html.Div(children=[

    html.Div([
        dropdown1,
        avgbox,
    ],
    className='row',
    style={
        # 'margin': 0,
        'padding': 30,
    }),

    html.Div(
        [
        # https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/spinners_bar.py
            dcc.Loading(children=[
                dcc.Graph(
                    id='choropleth',
                    figure={},
                    style={'margin': 30})
             ],
             color="#119DFF", type="dot", fullscreen=False,),

        ],
        className='row',
    ),

    html.Div(
        [
            dcc.Slider(
                id='year',
                min=min(years),
                max=max(years),
                step=1,
                marks={
                    y: str(y) for y in years
                },
                value=min(years),
            )
        ],
        className='row',
        style={'margin': '10px 20%'}
    ),

], className='')


footer = html.Div(children=[

    html.Small('Built with Plotly Dash')


], className='',
style={
    'padding': 10,
})

# ------------------------------------------------------------------------------

# full page
app.layout = html.Div(children=[
    header,
    html.Hr(),
    graph,
    html.Hr(),
    footer,
], className='container')

# ------------------------------------------------------------------------------

units = {
    'max_temp': 'degrees centigrade',
    'min_temp': 'degrees centigrade',
    'rainfall': 'cubic centimeters per sq area',
    'humidity': 'percent',
}

@app.callback(
    [Output("choropleth", "figure"),
    Output("average", "children"),
    Output("unit", "children")],
    [Input("type", "value"),
     Input("year", "value"),])
def display_choropleth(type, year):
    df_inner = df.copy()

    df_yearly = df_inner[df_inner['year'] == year]

    if not type: type = 'max_temp'

    fig = get_map(df_yearly,
                 shapes,
                 column=type)

    average = round(df_yearly[type].mean())

    unit = units[type]

    return fig, average, unit

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
