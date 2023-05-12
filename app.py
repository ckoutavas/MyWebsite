import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import plotly.express as px

# setup
external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# get the Stack Overflow question, answer and rep data form SQL DB
db = sqlite3.connect('StackOverflow.db')
recent_answers_df = pd.read_sql('SELECT * FROM recent_answers LIMIT 5', db)
top_answers_df = pd.read_sql('SELECT * FROM top_answers ORDER BY score DESC LIMIT 5', db) \
    .sort_values('score', ascending=False)
rep_df = pd.read_sql('SELECT * FROM reputation', db)

# create the cards for stack overflow answers
recent_answer_cards = [
    dbc.Card([
        dbc.Row([
            dbc.Col(dbc.CardBody(html.P(score)), style={'textAlign': 'center'}),
            dbc.Col(dbc.CardBody(dbc.CardLink(title, href=link, target='_blank')), className='col-md-6'),
            dbc.Col(dbc.CardBody(html.P(date)))
        ])
    ])
    for score, title, link, date in zip(recent_answers_df['score'],
                                        recent_answers_df['title'],
                                        recent_answers_df['link_a'],
                                        recent_answers_df['creation_date'])
]

top_answer_cards = [
    dbc.Card([
        dbc.Row([
            dbc.Col(dbc.CardBody(html.P(score)), style={'textAlign': 'center'}),
            dbc.Col(dbc.CardBody(dbc.CardLink(title, href=link, target='_blank')), className='col-md-6'),
            dbc.Col(dbc.CardBody(html.P(date)))
        ])
    ])
    for score, title, link, date in zip(top_answers_df['score'],
                                        top_answers_df['title'],
                                        top_answers_df['link_a'],
                                        top_answers_df['creation_date'])
]

# create reputation graph
rep_fig = px.line(rep_df, x='creation_date', y='rep_cumsum', title='Stack Overflow Reputation', height=390,
                  labels={'creation_date': 'Date', 'rep_cumsum': 'Reputation'}, template='plotly_dark')
rep_fig.update_layout(plot_bgcolor='#303030', paper_bgcolor='#303030', xaxis=dict(gridcolor='lightgrey'),
                      yaxis=dict(gridcolor='lightgrey'), hovermode='x unified')
rep_fig.update_traces(line_color='#00bc8c')

# get my current ranking on Stack Overflow
soup = BeautifulSoup(requests.get('https://stackoverflow.com/users/rank?userId=9177877').text.strip(),
                     'html.parser')

# webpage layout
app.layout = html.Div([
    # page heading
    html.Center(html.H1("Chris Koutavas' Portfolio")),
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
    html.Div(
        children=[
            html.Button('Top Answers on Stack Overflow', id='top-answers', style={'marginRight': '10px'}),
            html.Button('Recent Answers on Stack Overflow', id='recent-answers'),
            html.H2(id='card-title')
        ],
        style={'margin': '0px 0px 20px 20px'}
    ),
    # container for the stack overflow answer data
    html.Div(
        children=[
            html.Div(id='answer-data', style={'marginRight': '20px'}),
            dcc.Graph(id='rep-graph', style={'marginRight': '20px'})
        ],
        style={'display': 'flex', 'flexDirection': 'row', 'marginLeft': '20px'}
    )

])


@app.callback(Output('answer-data', 'children'),
              Output('rep-graph', 'figure'),
              Output('card-title', 'children'),
              Input('top-answers', 'n_clicks'),
              Input('recent-answers', 'n_clicks'))
def card_select(top_click, recent_click):
    trigger = dash.callback_context.triggered[0]
    if trigger['prop_id'] == 'recent-answers.n_clicks':
        return recent_answer_cards, rep_fig, 'Recent Answers on Stack Overflow'
    else:
        return top_answer_cards, rep_fig, 'Top Answers on Stack Overflow'


if __name__ == '__main__':
    app.run_server(debug=True)
