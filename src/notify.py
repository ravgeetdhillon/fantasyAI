from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import fileinput
import variables
import smtplib, ssl
import os
import json


with open(f'data/gameweeks.json', 'r') as f:
    gameweeks = json.load(f)


def get_cron_date(date):
    '''
    Converts to the given date to cron job format.
    '''

    day = date.day
    month = date.month
    hour = date.hour
    minute = date.minute
    cron = f'{minute} {hour} {day} {month} *'

    return cron


def get_deadline(gameweeks=gameweeks):
    '''
    Get's the next gameweek's deadline and time to notify.
    '''

    for gameweek in gameweeks:
        if gameweek['finished'] == False:
            next_deadline = gameweek['deadline_time']
            break

    # parse the deadline date into string for email notification
    deadline_date = datetime.strptime(next_deadline, '%Y-%m-%dT%H:%M:%SZ')
    deadline_date = deadline_date + timedelta(hours=5, minutes=30)
    deadline_date = deadline_date.isoformat()
    deadline_date = datetime.fromisoformat(deadline_date).strftime('%d %b, %Y %H:%M')

    return deadline_date


def get_notify_time(gameweeks=gameweeks):
    '''
    Get's the email notification time in cron syntax.
    '''
    
    for index, gameweek in enumerate(gameweeks):
        if gameweek['finished'] == False:
            next_deadline = gameweek['deadline_time']
            last_deadline = gameweeks[index - 1]['deadline_time']
            break
    
    last_notify_at = datetime.strptime(last_deadline, '%Y-%m-%dT%H:%M:%SZ')
    last_notify_at = last_notify_at - timedelta(hours=variables.NOTIFY_BEFORE)
    last_notify_at = get_cron_date(last_notify_at)

    next_notify_at = datetime.strptime(next_deadline, '%Y-%m-%dT%H:%M:%SZ')
    next_notify_at = next_notify_at - timedelta(hours=variables.NOTIFY_BEFORE)
    next_notify_at = get_cron_date(next_notify_at)

    return last_notify_at, next_notify_at


def get_gameweek(gameweeks=gameweeks):
    '''
    Get's the next gameweek's ID.
    '''

    for gameweek in gameweeks:
        if gameweek['finished'] == False:
            gameweek_id = gameweek['id']
            return gameweek_id


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
            .header {
                background: #37003c88;
                color: #ffffff;
            }
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background: #eeeeee;
            }
            .btn {
                font-family: Arial, sans-serif;
                background: #37003c;
                border: none;
                color: #ffffff;
                padding: 8px 16px;
                text-decoration: none;
                display: inline-block;
                cursor: pointer;
                border-radius: 4px;
            }
        </style>
    '''

    html = ''
    for transfer in transfers:
        html += f'''
            <tr>
                <td>{transfer['out']['name'].title()}</td>
                <td>{transfer['in']['name'].title()}</td>
                <td>{transfer['points']}</td>
                <td>{transfer['g/l']}</td>
            </tr>
        '''
    
    response = f'''
        <!DOCTYPE html>
        <html>
        <head>
            {style}
        </head>
        <body>
            <p>Hi Ravgeet, </p>
            <p>This is <b>Fantasy AI</b>. Hope you had a great last gameweek and ready to fire again this time. After running through the data, I have done the following analysis for gameweek {get_gameweek()}.</p>
            <h3>Potential Transfers</h3>
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
            <h3>Important Stats</h3>
            <p>Next <b>deadline</b> is <b>{get_deadline()}</b></p>
            <p>Your <b>team value</b> is <b>£{variables.BUDGET}m</b></p>
            <p>You have <b>£{variables.BANK}m</b> in your <b>bank</b></p>
            <p>Your overall <b>rank</b> is <b>{variables.RANK}</b></p>
            <p>Your current <b>points</b> are <b>{variables.CURRENT_POINTS}</b></p>
            <br>
            <a href="https://fantasy.premierleague.com/entry/{variables.TEAM_ID}/event/{get_gameweek()-1}" class="btn">Manage your team</a>
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
    message['Subject'] = f'Fantasy AI - Gameweek {get_gameweek()}'
    message['From'] = sender_email
    message['To'] = receiver_email
    
    # turn these into html MIMEText objects
    part = MIMEText(content, 'html')

    # add HTML part to MIMEMultipart message
    message.attach(part)

    # create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == '__main__':
    print(get_gameweek())
