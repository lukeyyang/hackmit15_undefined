# imports
from flask import Flask, request, redirect, render_template
from app import app#, db, models


# HTML - static HTML
@app.route('/')
def landing_page():
  return render_template('main.html')

