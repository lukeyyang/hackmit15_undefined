# imports
from flask import Flask, request, redirect, render_template
from app import app, db, models

from apiclient import discovery
from oauth2client import client

import json
import flask
import httplib2

# HTML - static HTML
@app.route('/')
def landing_page():
  return render_template('index.html')

# Google Login Test
# code from https://developers.google.com/identity/protocols/OAuth2WebServer
@app.route('/google_login')
def google_login():
  if 'credentials' not in flask.session:
    return redirect(flask.url_for('oauth2callback'))
  credentials \
    = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())

    people_service = discovery.build('plus', 'v1', http_auth)
    #print dir(people_service)
    people_resource = people_service.people()
    people_document = people_resource.get(userId='me').execute()
    print "DEBUG: authenticated Google ID: " + people_document['id']
    db.session.add(models.User(google_id = people_document['id']))
    db.session.commit()
    uid = models.User.query.filter_by(\
        google_id = people_document['id']).first().id
    print "DEBUG: User with uid = " + str(uid) + " created"
    return welcome_page(uid = uid) 


@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'app/static/json/client_secret.json',
      scope = 'https://www.googleapis.com/auth/plus.me',
      redirect_uri= flask.url_for('oauth2callback', _external = True))
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('google_login'))

@app.route('/welcome/<uid>')
def welcome_page(uid = None):
  return render_template('welcome.html', uid = uid)
      


