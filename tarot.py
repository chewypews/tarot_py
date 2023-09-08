## load packages
import os
import glob
import datetime
import random
from functools import reduce
import argparse
import webbrowser

## UPDATE ME IF YOU WANT ------------------------------
dir_to_save_spreads = os.path.expanduser("~/Desktop/")
## ----------------------------------------------------

## Function to draw N cards
def draw_cards(n_cards, seed = None):
    ## list files
    cards = [os.path.basename(x) for x in glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/cards/*")]
    cards = [x.removesuffix(".jpg") for x in cards]
    ## set seed
    if seed == None: ## use time
        random.seed(str(datetime.datetime.now()))
    else: 
        random.seed(str(seed) + " - " + str(datetime.datetime.now()))
    ## sample cards
    cards = random.sample(cards, n_cards)
    ## sample directions
    directions = list(random.choices(["+", "-"], k = n_cards))
    draw = reduce(lambda res, l: res + [l[0] + l[1]], zip(directions, cards), [])
    return draw

## Function to convert N cards to a spread (either drawn or inputted)
def draw_spread(spread_type, seed = None, card_list = None):
    ## draw cards set categories
    if spread_type == "celtic":
        if card_list == None:
            cards = draw_cards(10, seed)
        else:
            cards = card_list
        categories = ["center", "cross", "above", "below", "from", "toward", "self", "environment", "hopesfears", "advice"]
    elif spread_type == "cross":
        if card_list == None:
            cards = draw_cards(5, seed)
        else:
            cards = card_list
        categories = ["top", "bottom", "left", "right", "center"]
    elif spread_type == "three":
        if card_list == None:
            cards = draw_cards(3, seed)
        else:
            cards = card_list
        categories = ["left", "middle", "right"]
    elif spread_type == "one":
        cards = draw_cards(1, seed)
        categories = ["one"]
    ## combine cards and categories into spread
    spread = dict(map(lambda i,j : (i,j), categories, cards))
    return spread

def save_html(spread_type, seed = None, card_list = None, out_dir = dir_to_save_spreads):
    ## draw spread
    spread = draw_spread(spread_type, seed, card_list)
    ## open template
    with open(os.path.dirname(os.path.abspath(__file__)) + '/templates/' + spread_type + '_template.html', 'r') as file:
        filedata = file.read()
    # Replace strings in HTML code
    for category in spread:
        find_1 = category + "_card"
        replace_1 = os.path.dirname(os.path.abspath(__file__)) + "/cards/" + spread[category][1:] + ".jpg"
        find_2 = category + "_rotate"
        if spread[category][0] == "-":
            if category in ["cross"]:
                replace_2 = "-90deg"
            else:
                replace_2 = "180deg"
        elif spread[category][0] == "+":
            if category in ["cross"]:
                replace_2 = "90deg"
            else:
                replace_2 = "0deg"
        filedata = filedata.replace(find_1, replace_1)
        filedata = filedata.replace(find_2, replace_2)
    # Write a new file out
    out_file = out_dir + "/tarot_" + spread_type + "_" + str(datetime.datetime.now().strftime("%Y-%d-%m_%Hh%Mm")) + '.html'
    with open(out_file, 'w') as file:
        file.write(filedata)
    browser = webbrowser.get('chrome')
    browser.open("file://" + out_file, new = 2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw tarot spreads :)')
    parser.add_argument('-s','--spread', help='What type of spread?', choices = ["celtic", "cross", "three", "one"], required=True)
    parser.add_argument('-q','--question', help='Question (seed for random draw).', required=False, default = None)
    parser.add_argument('-f','--filepath', help='.txt file containing list of pre-drawn cards', required=False, default = None)
    ## this text file should look the output of draw_cards() where each item is on a new line
    ## an example is contained in this repo as ./example_filepath.txt
    args = vars(parser.parse_args())
    S = args["spread"]
    Q = args["question"]
    F = args["filepath"]

    if F == None: ## draw 
        save_html(spread_type = S, seed = Q)
    else: ## read cards
        assert S != "one" ## no reason to import spread for 1 card
        with open(F) as f:
            cards = f.read().splitlines() 
        if S == "celtic":
            assert len(cards) == 10
        if S == "cross":
            assert len(cards) == 5
        if S == "three":
            assert len(cards) == 3
        save_html(spread_type = S, seed = Q, card_list = cards)
        
