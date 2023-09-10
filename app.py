import os
import random
import datetime
from functools import reduce
import dash
from dash import Dash, dcc, html, Input, Output, State, callback

## constants
cards = [y + str(x) for x in range(1,15) for y in ["wands_", "cups_", "swords_", "disks_"]] + ["majors_" + str(x) for x in range(0,22)]

## functions
def draw_cards(n_cards, seed):
    random.seed(str(seed) + " - " + str(datetime.datetime.now()))
    return [x + ".jpg" for x in random.sample(cards, n_cards)]
    
def draw_orientations(n_cards, seed):
    random.seed(str(seed) + " - " + str(datetime.datetime.now()))
    return list(random.choices(["0deg", "180deg"], k = n_cards))

## app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(["Question: ", dcc.Input(id='question_text', type='text')]), ## text of question   
    html.Br(),
    html.Div(["Spread type: ", dcc.RadioItems(['Celtic cross', 'Cross', 'Three-card', 'One-card'], "Celtic cross", id = "spread_type", inline=True)]), ## type of spread
    html.Br(),
    html.Button('Draw cards', id='button_go'), ## button
    html.Div(id='spread') ## spread itself
])

@callback(
    Output('spread', 'children'), ## Output that is updated (spread itself)
    Input('button_go', 'n_clicks'), ## Input that triggers update to output (button)
    State('question_text', 'value'), ## extra value passed along (text of question)
    State('spread_type', 'value'), ## extra value passed along (type of spread)
    prevent_initial_call=True
)
def update_output(n_clicks, question_text, spread_type):
    if spread_type == "Celtic cross":
        cards = draw_cards(n_cards = 10, seed = question_text)
        orients = draw_orientations(n_cards = 10, seed = question_text)
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3("Question: " + str(question_text))),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td([
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[2]), height = 110, width=70, style={"transform": "rotate({})".format(orients[2])})])), 
                            html.Tr([
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[4]), height = 110, width=70, style={"transform": "rotate({})".format(orients[4]), "position": "relative", "left": "7px"})
                                ),
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[0]), height = 110, width=70, style={"transform": "rotate({})".format(orients[0]), "position": "relative", "left": "37px"}), 
                                ), 
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[1]), height = 110, width=70, style={"transform": "rotate({})".format('90deg'), "position": "relative", "left": "-37px"}),
                                ),
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[5]), height = 110, width=70, style={"transform": "rotate({})".format(orients[5]), "position": "relative", "left": "-7px"})
                                )
                            ]),
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[3]), height = 110, width=70, style={"transform": "rotate({})".format(orients[3])})]))  
                        ]), 
                        html.Td([
                            html.Tr(html.Img(src = dash.get_asset_url(cards[6]), height = 110, width=70, style={"transform": "rotate({})".format(orients[6])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[7]), height = 110, width=70, style={"transform": "rotate({})".format(orients[7])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[8]), height = 110, width=70, style={"transform": "rotate({})".format(orients[8])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[9]), height = 110, width=70, style={"transform": "rotate({})".format(orients[9])}))
                        ])
                    ])
                ])
            ])
        ])
    elif spread_type == "Cross":
        cards = draw_cards(n_cards = 5, seed = question_text)
        orients = draw_orientations(n_cards = 5, seed = question_text)
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3("Question: " + str(question_text))),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td([
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[0]), height = 110, width=70, style={"transform": "rotate({})".format(orients[0])})])), 
                            html.Tr([
                                html.Td(html.Img(src = dash.get_asset_url(cards[2]), height = 110, width=70, style={"transform": "rotate({})".format(orients[2])})),
                                html.Td(html.Img(src = dash.get_asset_url(cards[4]), height = 110, width=70, style={"transform": "rotate({})".format(orients[4])})),
                                html.Td(html.Img(src = dash.get_asset_url(cards[3]), height = 110, width=70, style={"transform": "rotate({})".format(orients[3])}))
                            ]),
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[1]), height = 110, width=70, style={"transform": "rotate({})".format(orients[1])})]))  
                        ])
                    ])
                ])
            ])
        ])
    elif spread_type == "Three-card":
        cards = draw_cards(n_cards = 5, seed = question_text)
        orients = draw_orientations(n_cards = 5, seed = question_text)
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3("Question: " + str(question_text))),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td(html.Img(src = dash.get_asset_url(cards[2]), height = 220, width=140, style={"transform": "rotate({})".format(orients[2])})),
                        html.Td(html.Img(src = dash.get_asset_url(cards[4]), height = 220, width=140, style={"transform": "rotate({})".format(orients[4])})),
                        html.Td(html.Img(src = dash.get_asset_url(cards[3]), height = 220, width=140, style={"transform": "rotate({})".format(orients[3])}))
                    ])
                ])
            ])
        ])
    elif spread_type == "One-card":
        cards = draw_cards(n_cards = 5, seed = question_text)
        orients = draw_orientations(n_cards = 5, seed = question_text)
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3("Question: " + str(question_text))),
            html.Center([
                html.Img(src = dash.get_asset_url(cards[2]), height = 220, width=140, style={"transform": "rotate({})".format(orients[2])})
            ])
        ])

    return div

if __name__ == '__main__':
    app.run_server(debug=True)
