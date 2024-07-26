#!/usr/bin/env python3
from flask import Flask, Response, render_template
from textwrap import shorten
import requests
import logging
from fedi import User, Post

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/')
def hello():
    return 'Hello, world!'

@app.route('/@<string:handle>')
def fetch_user(handle: str):
    if len(handle.split('@')) != 2:
        return 'AP Handle is not valid, make sure the handle is in format of @username@host', 500

    username, host = handle.split('@')
    
    res = requests.get(
        f'https://{host}/@{username}',
        headers={
            'Accept': 'application/activity+json'
        }
    )
    if not res.ok:
        if res.status_code == 401:
            # The server requires authorization to fetch AP object
            return 'This user is unavailable because the user or host does not accept anonymous fetching', 401
        
        return res.reason, res.status_code
    
    user = User.parse(username, host, res.json())
    posts = user.fetch_outbox_post()
    return Response(
        render_template('apuser.rss', user=user, posts=posts, shorten=shorten),
        mimetype='application/atom+xml; charset=utf-8'
    )
    
    # return 'Test OK, but not implemented yet', 200


# for when this file is executed directly
if __name__ == '__main__':
    logger.info('Service started')
    app.run()
    