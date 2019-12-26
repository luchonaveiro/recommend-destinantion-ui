import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from recommend_destinations import externals as rd
import pandas as pd
import plotly.figure_factory as ff

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        #[html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# Define possible destinantions
possible_destinations = rd.get_possible_destinations()

# Dash
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

group_colors = {"control": "light blue", "reference": "red"}

# App Layout
app.layout = html.Div(
    children=[
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="Travel Recommender"),
                # html.Div(
                #     className="div-logo",
                #     children=html.Img(
                #         className="logo", src=app.get_asset_url("iunigo_blanco.png")
                #     ),
                # ),
                html.H2(className="h2-title-mobile", children="Travel Recommender"),
            ],
        ),
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H4('Elegir Ciudades:'),
                                    ],
                                ),
                                dcc.Dropdown(
                                    id = 'cities',
                                    options = possible_destinations,
                                        multi=True
                                ),  
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.Button('Recomendar', id='button',),
                                    ]
                                ),
                            ],
                        )
                    ],
                ),
                # Resultados
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H4("Recomendaciones: "),
                                html.Br(),
                                dcc.Loading(id="loading-1", children=[
                                    html.Div(id="recommendation")
                                    ], type="default"),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ]
)

# Callback to generate error message
# Also sets the data to be used
# If there is an error use default data else use uploaded data
@app.callback(
    Output(component_id='recommendation', component_property='children'),
    [Input('button', 'n_clicks')],
    state=[State(component_id='cities', component_property='value')]
)
def update_output_div(n_clicks, input_1):
    if n_clicks != None:
        recommendations = rd.recommend_cities(input_1)
        recommendations = pd.DataFrame(recommendations)
        recommendations = recommendations[['name','country','continent']]
        #return str(recommendations)
        return generate_table(recommendations)


# Run Dash
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)