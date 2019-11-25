from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import variables
import smtplib, ssl
import os
import json


with open(f'data/gameweeks.json', 'r') as f:
    gameweeks = json.load(f)


def get_deadline(gameweeks=gameweeks):
    '''
    Get's the next gameweek's deadline.
    '''

    for gameweek in gameweeks['events']:
        if gameweek['finished'] == False:
            date = gameweek['deadline_time'].strip('Z')
            date = datetime.fromisoformat(date).strftime('%d %b, %Y %H:%M')
            return date


def get_gameweek(gameweeks=gameweeks):
    '''
    Get's the next gameweek name.
    '''

    for gameweek in gameweeks['events']:
        if gameweek['finished'] == False:
            return gameweek['name']


def html_response(transfers):
    '''
    Creates a HTML response to be sent through email.
    '''

    style = '''
        <style>
            body {
                font-family: arial, sans-serif;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            td, th {
                border: 1px solid #ddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background: #eee;
            }
        </style>
    '''

    html = ''
    for transfer in transfers:
        html += f'''
            <tr>
                <td>{transfer['out'].title()}</td>
                <td>{transfer['in'].title()}</td>
                <td>{transfer['points']}</td>
                <td>{transfer['g/l']}</td>
            </tr>
        '''
    
    response = f'''
        <html>
        <head>
            {style}
        </head>
        <body>
            <h2>Potential Transfers</h2>
            <table>
                <tr>
                    <th>Out</th>
                    <th>In</th>
                    <th>Points</th>
                    <th>Gain/Loss</th>
                </tr>
                {html}
            </table>
            <br>
            <h2>Important Stats</h2>
            <p>Next <b>deadline</b> is <b>{get_deadline()}</b></p>
            <p>Your <b>team value</b> is <b>£{variables.BUDGET}m</b></p>
            <p>You have <b>£{variables.BANK}m</b> in your <b>bank</b></p>
            <p>Your overall <b>rank</b> is <b>{variables.RANK}</b></p>
            <p>Your current <b>points</b> are <b>{variables.CURRENT_POINTS}</b></p>
        </body>
        </html>
    '''

    return response


def send_email(content):
    '''
    Sends an email to the user.
    '''

    sender_email = variables.SENDER_EMAIL
    receiver_email = variables.RECEIVER_EMAIL
    password = variables.PASSWORD

    message = MIMEMultipart('alternative')
    message['Subject'] = f'Fantasy AI - {get_gameweek()}'
    message['From'] = sender_email
    message['To'] = receiver_email
    
    # Turn these into html MIMEText objects
    part = MIMEText(content, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
