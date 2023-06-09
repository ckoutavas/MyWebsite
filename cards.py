from dash import html
import dash_bootstrap_components as dbc

button_css = {'width': '100%'}
card_css = {'margin': '10px 10px 10px 0px'}

# create cards for Fun Projects
MMM_PiTemp = dbc.Card([
    dbc.CardHeader('MMM-PiTemp'),
    dbc.CardBody([
        html.P('A MagicMirror2 module that tells you the temperature of your Raspberry Pi. The program '
               'shuts down the Pi if the temperature goes above n degrees.'),
        html.P('JavaScript, Python')
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='MMM-PiTemp', style=button_css),
                          href='https://github.com/ckoutavas/MMM-PiTemp', target='_blank'))
], style=card_css)

MMM_DHT = dbc.Card([
    dbc.CardHeader('MMM-DHT'),
    dbc.CardBody([
        html.P('A MagicMirror2 module that uses a DHT22 sensor to read the temperature and humidity, and display it '
               'on your Raspberry Pi.'),
        html.P('JavaScript, Python'),
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='MMM-DHT', style=button_css),
                          href='https://github.com/ckoutavas/MMM-DHT', target='_blank'))
], style=card_css)

covid = dbc.Card([
    dbc.CardHeader('COVID-19 Dash App'),
    dbc.CardBody([
        html.P('A Dash app that plots COVID-19 data pulled from the CDC data API. The state-specific data is '
               'displayed when the user clicks on a state on the map.'),
        html.P('Python'),
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='covid', style=button_css),
                          href='https://github.com/ckoutavas/COVID-Dash-App', target='_blank'))
], style=card_css)

twitter = dbc.Card([
    dbc.CardHeader('Twitter Dash App'),
    dbc.CardBody([
        html.P('Dash app that utilizes the Twitter API to pull public tweet data based on the username and returns '
               'the tweet on hover.'),
        html.P('Python'),
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='twitter', style=button_css),
                          href='https://github.com/ckoutavas/Twitter-Web-App', target='_blank'))
], style=card_css)

ga4 = dbc.Card([
    dbc.CardHeader('Google Analytics 4'),
    dbc.CardBody([
        html.P('A simple python class that uses the GA4 Data API to create a report and return a pandas.DataFrame.'),
        html.P('Python'),
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='ga4', style=button_css),
                          href='https://github.com/ckoutavas/GoogleAnalytics4', target='_blank'))
], style=card_css)

social_media = dbc.Card([
    dbc.CardHeader('Social Media Analytics'),
    dbc.CardBody([
        html.P('A python API wrapper for the Meta Graph API to pull social media posts and analytics over time for '
               'your connected Facebook and Instagram business accounts.'),
        html.P('Python'),
    ]),
    dbc.CardFooter(html.A(html.Button('View on GitHub', id='meta', style=button_css),
                          href='https://github.com/ckoutavas/SocialMediaAnalytics', target='_blank'))
], style=card_css)
