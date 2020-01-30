from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.models import Pin



@app.route('/', methods=['GET'])
def index():
    pass


@app.route('/<string:s_n>', methods=['GET'])
@app.route('/<string:pin>', methods=['GET'])
def check(s_n, pin):
    pass



