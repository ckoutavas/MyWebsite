import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests
from bs4 import BeautifulSoup
import StackData
import sqlite3
import pandas as pd

# setup
external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# get the Stack Overflow question and answer data
db = sqlite3.connect('StackOverflow.db')
recent_answers_df = pd.read_sql('SELECT * FROM recent_answers LIMIT 5', db)
top_answers_df = pd.read_sql('SELECT * FROM top_answers ORDER BY score DESC LIMIT 5', db).sort_values('score', ascending=False)


# create the cards for stack overflow answers
recent_answer_cards = [
    dbc.Card(dbc.CardBody([html.P(score), dbc.CardLink(title, href=link)]),
             style={'margin': '0px 0px 0px 20px', 'width': '60%'})
    for score, title, link in zip(recent_answers_df['score'], recent_answers_df['title'], recent_answers_df['link_a'])
]

top_answer_cards = [
    dbc.Card(dbc.CardBody([html.P(score), dbc.CardLink(title, href=link)]),
             style={'margin': '0px 0px 0px 20px', 'width': '60%'})
    for score, title, link in zip(top_answers_df['score'], top_answers_df['title'], top_answers_df['link_a'])
]

# get my current ranking on Stack Overflow
soup = BeautifulSoup(requests.get('https://stackoverflow.com/users/rank?userId=9177877').text.strip(),
                     'html.parser')

# webpage layout
app.layout = html.Div([
    # page heading
    html.Center(html.H1('Chris Koutavas')),
    # stack exchange reputation image that is updated every 24-48 hours
    html.Div(children=[
        html.A(href='https://stackoverflow.com/users/9177877/it-is-chris', target='_blank',
               children=[html.Img(src='https://stackexchange.com/users/flair/12623101.png',
                                  width=208, height=58, alt='profile for It_is_Chris on Stack Exchange',
                                  title='profile for It_is_Chris on Stack Exchange')], id='stack-rep'),
        html.Br(),
        # Parse current ranking on Stack Overflow
        html.A(href=soup.find('a')['href'], target='_blank',
               children=[html.Span(soup.find('a').text)])

    ], id='stack-user-data', style={'margin': '0px 0px 0px 20px'}),
    html.Br(),
    # stack overflow buttons
    html.Div(children=[html.Button('top answers', id='top-answers'),
                       html.Button('recent answers', id='recent-answers')],
             style={'margin': '0px 0px 0px 20px'}),
    # container for the stack overflow dta
    html.Div(children=top_answer_cards)

])


# @app.callback(Output('stack-data', 'children'),
#               Input("", "n_clicks"))
# def card_select(clicks):
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)
