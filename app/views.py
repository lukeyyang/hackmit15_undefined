# imports
from flask import Flask, request, redirect, render_template, flash, url_for
from app import app, db, models
from .forms import NewPollForm, HelpOthersForm, JoinGroupForm, GroupVoteForm, generate_form, generate_help_others_form
from models import Poll, Choice

from apiclient import discovery
from oauth2client import client

import json
import flask
import httplib2
import random

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

@app.route('/new_poll', methods=['GET', 'POST'])
def new_poll():
    form = NewPollForm()
    form.title(placeholder="Title")
    if form.validate_on_submit():
      newPoll = Poll()
      if form.individual.data == 'yes':
        newPoll.individual = True
      else:
        newPoll.individual = False;
      if form.equality.data == 'yes':
        newPoll.equality = True
      else:
        newPoll.equality = False
      newPoll.title = form.title.data
      newPoll.detail = form.detail.data
      newPoll.deadline = form.deadline.data
      #print("Here")
      #Deal with choices
      choice1 = Choice()
      choice1.content = form.choice.data
      choice1.votes = 0

      if form.choice2.data:
        choice2 = Choice()
        choice2.content = form.choice2.data
        choice2.votes = 0
        newPoll.choices.append(choice2)
        db.session.add(choice2)

      if form.choice3.data:
        choice3 = Choice()
        choice3.content = form.choice3.data
        choice3.votes = 0
        newPoll.choices.append(choice3)
        db.session.add(choice3)

      if form.choice4.data:
        choice4 = Choice()
        choice4.content = form.choice4.data
        choice4.votes = 0
        newPoll.choices.append(choice4)
        db.session.add(choice4)

      if form.choice5.data:
        choice5 = Choice()
        choice5.content = form.choice5.data
        choice5.votes = 0
        newPoll.choices.append(choice5)
        db.session.add(choice5)

      newPoll.choices.append(choice1)
      db.session.add(choice1)
      db.session.add(newPoll)
      db.session.commit()
      flash('New Poll submitted for Title="%s", Detail=%s, Deadline=%s' %
              (form.title.data, str(form.detail.data), str(form.deadline.data)))
      return redirect('/')

    return render_template('new_poll.html', 
                           title='New Poll',
                           form=form)

@app.route('/join', methods=['GET', 'POST'])
def join_group():
  form = JoinGroupForm()
  if form.validate_on_submit():
    postID = form.number.data
    return redirect(url_for('group_vote', poll_id=postID))
  return render_template('join.html', title='Join', form=form)

@app.route('/poll/vote/<int:poll_id>', methods=['GET', 'POST'])
def group_vote(poll_id):
    # show the post with the given id, the id is an integer
    poll = models.Poll.query.get(poll_id)
    form = generate_form(poll)
    if form.is_submitted():
      print("Hereeee")
      val = form.possibilities.data

      choi = models.Choice.query.get(val)
      if choi is not None:
        if choi.votes is None:
          choi.votes = 0
        choi.votes = choi.votes+1
        db.session.commit()
        
      return redirect(url_for('show_vote', poll_id=poll_id))
    return render_template('group_poll.html',title='Group Vote',form=form)

@app.route('/poll/<int:poll_id>', methods=['GET', 'POST'])
def show_vote(poll_id):
    # show the post with the given id, the id is an integer
    poll = models.Poll.query.get(poll_id)
    return render_template('show_poll.html',title='Vote Result',poll=poll)
      
@app.route('/help_others', methods=['GET', 'POST'])
def help_others():
    #choice = Choice.query.filter_by(id=0).first_or_404()

    #polls = Poll.query.filter_by(id=0).first()
    num_poll = random.randint(1, len(models.Poll.query.all()))
    print(num_poll)
    poll = models.Poll.query.get(num_poll)
    form = generate_help_others_form(poll)

    #poll_ptr = num_poll
    #form = HelpOthersForm()
    #form.choice_checked.choices = [(item.id, item.content) for item in poll.choices]    #print (len(form.choice_checked.choices))

    if form.is_submitted():
      #print(poll.title)
      index = form.choice_checked.data
      #print(index)
      choice = models.Choice.query.get(index)
      choice.votes += 1
      db.session.commit()

      #if form.choose_this.data == True:
        #choice.votes+=1
      #flash('Votes made for "%s"="%s"' % (choice.content, choice.votes))
      print(num_poll)
      return redirect(url_for('show_vote', poll_id=choice.poll_id))
    else:
      print 'WRONG!!!'
    return render_template('help_others.html', 
                            title="Help Others", 
                            form=form,
                            poll=poll)

