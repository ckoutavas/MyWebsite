import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import plotly.express as px
import cards

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
rep_fig = px.line(rep_df, x='creation_date', y='rep_cumsum', title='Stack Overflow Reputation',
                  labels={'creation_date': 'Date', 'rep_cumsum': 'Reputation'}, template='plotly_dark')
rep_fig.update_layout(plot_bgcolor='#303030', paper_bgcolor='#303030',
                      xaxis=dict(gridcolor='lightgrey', linecolor='lightgrey'),
                      yaxis=dict(gridcolor='lightgrey', linecolor='lightgrey'), hovermode='x unified')
rep_fig.update_traces(line_color='#00bc8c')
rep_graph = dcc.Graph(figure=rep_fig, style={'margin': '20px 0px 20px 0px'})

# add reputation graph to the lists below
recent_answer_cards.append(rep_graph)
top_answer_cards.append(rep_graph)

# fun project cards
fun_project_cards = dbc.CardGroup([
    dbc.CardGroup([
        cards.MMM_PiTemp,
        cards.covid,
        cards.ga4
    ]),
    dbc.CardGroup([
        cards.MMM_DHT,
        cards.twitter,
        cards.social_media
    ])
])

# get my current ranking on Stack Overflow
soup = BeautifulSoup(requests.get('https://stackoverflow.com/users/rank?userId=9177877').text.strip(),
                     'html.parser')

# webpage layout
app.layout = dbc.Container([
    html.Div([
        # layout 1/3 2/3
        dbc.Row([
            # column 1 1/3
            dbc.Col([
                # page heading
                html.Div(
                    children=[
                        html.Img(src=app.get_asset_url('ChrisKoutavas.jpeg'), alt='Chris Koutavas headshot',
                                 style={'borderRadius': '10%', 'marginTop': '20px', 'width': '100%'}),
                        html.Center(html.H1('Chris Koutavas')),
                        html.Br(),
                        # stack exchange reputation image that is updated every 24-48 hours
                        html.Center([
                            html.Div(
                                children=[
                                    html.A(href='https://stackoverflow.com/users/9177877/it-is-chris', target='_blank',
                                           children=[html.Img(src='https://stackexchange.com/users/flair/12623101.png',
                                                              width='80%',
                                                              alt='profile for It_is_Chris on Stack Exchange',
                                                              title='profile for It_is_Chris on Stack Exchange')],
                                           id='stack-rep'),
                                    html.Br(),
                                    # Parse current ranking on Stack Overflow
                                    html.A(href=soup.find('a')['href'], target='_blank',
                                           children=[html.Span(soup.find('a').text)]),
                                ], id='stack-user-data'),
                            html.Br(),
                            dbc.Card(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem('Stack Overflow',
                                                          href='https://stackoverflow.com/users/9177877/it-is-chris',
                                                          target='_blank'),
                                        dbc.ListGroupItem('GitHub',
                                                          href='https://github.com/ckoutavas', target='_blank'),
                                        dbc.ListGroupItem('LinkedIn',
                                                          href='https://www.linkedin.com/in/chris-koutavas-6204a9113/',
                                                          target='_blank'),
                                        dbc.ListGroupItem('Website Source Code',
                                                          href='https://github.com/ckoutavas/MyWebsite',
                                                          target='_blank')
                                    ],
                                    flush=True
                                )
                            ),
                        ]
                        )
                    ]
                ),
            ], md=3),
            # colum 2 2/3
            dbc.Col([
                # stack overflow buttons
                html.Div(
                    children=[
                        html.Button('Top Answers on Stack Overflow', id='top-answers'),
                        html.Button('Recent Answers on Stack Overflow', id='recent-answers'),
                        html.Button('Fun Projects', id='recent-projects')
                    ],
                    style={'margin': '20px 0px 20px 0px'}
                ),
                # container for the stack overflow answer data
                html.Div(id='button-data'),
            ], md=9)
        ]),
    ])
], fluid=True)

# css for button style on click
selected_css = {'backgroundColor': '#00bc8c',
                'marginRight': '20px'}
not_selected_css = {'marginRight': '20px'}


@app.callback(Output('button-data', 'children'),
              Output('top-answers', 'style'),
              Output('recent-answers', 'style'),
              Output('recent-projects', 'style'),
              Input('top-answers', 'n_clicks'),
              Input('recent-answers', 'n_clicks'),
              Input('recent-projects', 'n_clicks'))
def card_select(*args):
    trigger = dash.callback_context.triggered[0]
    if trigger['prop_id'] == 'recent-answers.n_clicks':
        return recent_answer_cards, not_selected_css, selected_css, not_selected_css
    elif trigger['prop_id'] == 'recent-projects.n_clicks':
        return fun_project_cards, not_selected_css, not_selected_css, selected_css
    else:
        return top_answer_cards, selected_css, not_selected_css, not_selected_css


if __name__ == '__main__':
    app.run_server(debug=False)
