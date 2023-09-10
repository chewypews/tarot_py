import os
import time
import random
import datetime
from functools import reduce
import dash
from dash import Dash, dcc, html, Input, Output, State, callback

## constants
cards = [y + str(x) for x in range(1,15) for y in ["wands_", "cups_", "swords_", "disks_"]] + ["majors_" + str(x) for x in range(0,22)]
cards_oriented = [x + "-upright" for x in cards] + [x + "-reversed" for x in cards]

## functions
def time_seed(seed = None):
    if seed == None:
        out = int(time.time() * 256)
    else:
        out = str(int(time.time() * 256)) + seed
    return out
def draw_cards(n_cards, seed):
    random.seed(seed)
    out = [x + ".jpg" for x in random.sample(cards, n_cards)]    
    return out
def draw_orientations(n_cards, seed):
    random.seed(seed)
    out = list(random.choices(["0deg", "180deg"], k = n_cards))
    return out
def parse_manual_cards(manual_cards):
    cards = [x.split("-")[0] for x in manual_cards]
    cards = [x + ".jpg" for x in cards]
    orients = [x.split("-")[1] for x in manual_cards]
    orients_dict = {"upright": "0deg", "reversed": "180deg"}
    orients = [orients_dict[x] for x in orients]
    return cards, orients

## app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(html.Center(html.H1("Tarot-py"))),
    html.Div([ ## type of spread 
        html.Center(dcc.RadioItems(['Celtic cross', 'Simple cross', 'Three card', 'Mini cross', 'One card'], "Celtic cross", id = "spread_type", inline=True, inputStyle={"margin-left": "20px"}))
    ]), 
    html.Br(),
    html.Div([ ## text of question   
        "QUESTION (optional; added to random seed)",
        dcc.Input(id='question_text', type='text')
    ]), 
    html.Br(),
    html.Div([ ## Manual input cards
        "CARDS (optional; manually choose cards)", 
        dcc.Dropdown(cards_oriented,  id = "manual_cards", multi=True)
    ]), 
    html.Br(),
    html.Button('... Go!', id='button_go', style = {"background-color": '#ffa500', "border": "1px solid white"}), ## button
    html.Div(id='spread') ## spread itself
])

@callback(
    Output('spread', 'children'), ## Output that is updated (spread itself)
    Input('button_go', 'n_clicks'), ## Input that triggers update to output (button)
    State('question_text', 'value'), ## extra value passed along (text of question)
    State('spread_type', 'value'), ## extra value passed along (type of spread)
    State('manual_cards', 'value'), ## extra value passed along (manual card draw)
    prevent_initial_call=True
)
def update_output(n_clicks, question_text, spread_type, manual_cards): ## n_clicks = value of button, and the others are extra State() values passed along (all are order dependent)
    
    ## Seed = Time seed
    seed = time_seed(question_text)

    ## Header = question text or empty text
    if(question_text == ""):
        Q = "Question: " + str(question_text)
    else:
        Q = ""

    if spread_type == "Celtic cross":
        ## draw or input cards
        if manual_cards == None or len(manual_cards) == 0:
            cards = draw_cards(10, seed)
            orients = draw_orientations(10, seed)
        else:
            cards, orients = parse_manual_cards(manual_cards)
            if len(cards) != 10:
                return html.Div(html.Center(html.H4("Must select 10 cards to manually input this spread", style = {"color": "#cc0000"})))
        ## fix cross orientation
        if orients[1] == "0deg":
            orients[1] = "90deg"
        else:
            orients[1] = "-90deg"
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3(Q)),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td([
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[2]), height = 110, width=70, style={"transform": "rotate({})".format(orients[2])})])), 
                            html.Tr([
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[4]), height = 110, width=70, style={"transform": "rotate({})".format(orients[4]), "position": "relative", "left": "12px"})
                                ),
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[0]), height = 110, width=70, style={"transform": "rotate({})".format(orients[0]), "position": "relative", "left": "37px"}), 
                                ), 
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[1]), height = 110, width=70, style={"transform": "rotate({})".format(orients[1]), "position": "relative", "left": "-37px"}),
                                ),
                                html.Td(
                                    html.Img(src = dash.get_asset_url(cards[5]), height = 110, width=70, style={"transform": "rotate({})".format(orients[5]), "position": "relative", "left": "-12px"})
                                )
                            ]),
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[3]), height = 110, width=70, style={"transform": "rotate({})".format(orients[3])})]))  
                        ]), 
                        html.Td([
                            html.Tr(html.Img(src = dash.get_asset_url(cards[9]), height = 110, width=70, style={"transform": "rotate({})".format(orients[9])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[8]), height = 110, width=70, style={"transform": "rotate({})".format(orients[8])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[7]), height = 110, width=70, style={"transform": "rotate({})".format(orients[7])})),
                            html.Tr(html.Img(src = dash.get_asset_url(cards[6]), height = 110, width=70, style={"transform": "rotate({})".format(orients[6])}))
                        ])
                    ])
                ])
            ])
        ])
    elif spread_type == "Simple cross":
        ## draw or input cards
        if manual_cards == None or len(manual_cards) == 0:
            cards = draw_cards(5, seed)
            orients = draw_orientations(5, seed)
        else:
            cards, orients = parse_manual_cards(manual_cards)
            if len(cards) != 5:
                return html.Div(html.Center(html.H4("Must select 5 cards to manually input this spread", style = {"color": "red"})))
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3(Q)),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td([
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[1]), height = 110, width=70, style={"transform": "rotate({})".format(orients[1])})])), 
                            html.Tr([
                                html.Td(html.Img(src = dash.get_asset_url(cards[3]), height = 110, width=70, style={"transform": "rotate({})".format(orients[3])})),
                                html.Td(html.Img(src = dash.get_asset_url(cards[0]), height = 110, width=70, style={"transform": "rotate({})".format(orients[0])})),
                                html.Td(html.Img(src = dash.get_asset_url(cards[4]), height = 110, width=70, style={"transform": "rotate({})".format(orients[4])}))
                            ]),
                            html.Center(html.Tr([html.Img(src = dash.get_asset_url(cards[2]), height = 110, width=70, style={"transform": "rotate({})".format(orients[2])})]))  
                        ])
                    ])
                ])
            ])
        ])
    elif spread_type == "Three card":
        ## draw or input cards
        if manual_cards == None or len(manual_cards) == 0:
            cards = draw_cards(3, seed)
            orients = draw_orientations(3, seed)
        else:
            cards, orients = parse_manual_cards(manual_cards)
            if len(cards) != 3:
                return html.Div(html.Center(html.H4("Must select 3 cards to manually input this spread", style = {"color": "red"})))
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3(Q)),
            html.Center([
                html.Table([
                    html.Tr([
                        html.Td(html.Img(src = dash.get_asset_url(cards[0]), height = 220, width=140, style={"transform": "rotate({})".format(orients[0])})),
                        html.Td(html.Img(src = dash.get_asset_url(cards[1]), height = 220, width=140, style={"transform": "rotate({})".format(orients[1])})),
                        html.Td(html.Img(src = dash.get_asset_url(cards[2]), height = 220, width=140, style={"transform": "rotate({})".format(orients[2])}))
                    ])
                ])
            ])
        ])
    elif spread_type == "Mini cross":
        ## draw or input cards
        if manual_cards == None or len(manual_cards) == 0:
            cards = draw_cards(2, seed)
            orients = draw_orientations(2, seed)
        else:
            cards, orients = parse_manual_cards(manual_cards)
            if len(cards) != 2:
                return html.Div(html.Center(html.H4("Must select 2 cards to manually input this spread", style = {"color": "red"})))
        ## fix cross orientation
        if orients[1] == "0deg":
            orients[1] = "90deg"
        else:
            orients[1] = "-90deg"
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3(Q)),
            html.Center([
                html.Td(
                    html.Img(src = dash.get_asset_url(cards[0]), height = 220, width=140, style={"transform": "rotate({})".format(orients[0]), "position": "relative", "left": "70px"}), 
                ), 
                html.Td(
                    html.Img(src = dash.get_asset_url(cards[1]), height = 220, width=140, style={"transform": "rotate({})".format(orients[1]), "position": "relative", "left": "-70px"}),
                )
            ])
        ])
    
    elif spread_type == "One card":
        ## draw or input cards
        if manual_cards == None or len(manual_cards) == 0:
            cards = draw_cards(1, seed)
            orients = draw_orientations(1, seed)
        else:
            cards, orients = parse_manual_cards(manual_cards)
            if len(cards) != 1:
                return html.Div(html.Center(html.H4("Must select 1 card to manually input this spread", style = {"color": "red"})))
        div = html.Div([
            # html.H3("Questions asked: " + str(n_clicks)),
            html.Center(html.H3(Q)),
            html.Center([
                html.Img(src = dash.get_asset_url(cards[0]), height = 220, width=140, style={"transform": "rotate({})".format(orients[0])})
            ])
        ])

    return div

if __name__ == '__main__':
    app.run_server(debug=True)
