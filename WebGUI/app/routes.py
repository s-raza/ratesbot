from flask import render_template, flash, redirect, url_for, request
from WebGUI.app import app
from WebGUI.app.forms import RatesForm
from werkzeug.urls import url_parse
import RatesBot.Config as cfg
from RatesBot.DB.RatesDB import RatesDB
from RatesBot.Services.Service import *


def get_rates(for_date):

    db = RatesDB(conn_string=cfg.db['conn_string'])

    services = {}

    for service in ServiceBase.__subclasses__():
            
        srv = service()
        rates = db.get_rates_on_date(srv, for_date)
        # rates = db.get_rates_between_dates(srv, from_date, to_date)
        services[srv.service_name] = rates

    db.session.close()
    db.session.remove()

    return services

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RatesForm()

    if form.validate_on_submit():
        for_date = form.for_date.data
        return render_template('graph.html',
                                services=get_rates(for_date.strftime('%Y-%m-%d')),
                                for_date=for_date.strftime('%A %d/%m/%Y'),
                                form=form)
    else:
        # flash('Error')
        return render_template('index.html', form=form)

