from flask import render_template, flash, redirect, url_for, request
from WebGUI.app import app
from WebGUI.app.forms import RatesForm
from werkzeug.urls import url_parse
import RatesBot.Config as cfg
from RatesBot.DB.RatesDB import RatesDB
from RatesBot.Services.Service import *
from datetime import timedelta


def get_rates(for_date, to_date):

    for_date = for_date.strftime('%Y-%m-%d')
    to_date = to_date+timedelta(days=1)
    to_date = to_date.strftime('%Y-%m-%d')
    
    db = RatesDB(conn_string=cfg.db['conn_string'])

    services = {}

    for service in ServiceBase.__subclasses__():
            
        srv = service()
        rates = db.get_rates_between_dates(srv, for_date, to_date)
        services[srv.service_name] = rates

    db.session.close()
    db.session.remove()

    return services

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RatesForm()

    for_date = form.for_date.data
    to_date = form.to_date.data

    if for_date > to_date:
        flash("'From date' cannot be greater than 'To date'")
        return render_template('index.html', form=form)

    if form.validate_on_submit():
        return render_template('graph.html',
                                services=get_rates(for_date,to_date),
                                for_dates=[for_date.strftime('%A %d/%m/%Y'),to_date.strftime('%A %d/%m/%Y')],
                                form=form)
    else:
        return render_template('index.html', form=form)

