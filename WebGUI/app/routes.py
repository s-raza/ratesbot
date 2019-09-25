from flask import render_template, flash, redirect, url_for, request
from WebGUI.app import app
from WebGUI.app.forms import RatesForm
from werkzeug.urls import url_parse
import RatesBot.Config as cfg
from RatesBot.DB.RatesDB import RatesDB
from RatesBot.Services.Service import *
from datetime import timedelta
import random


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


def get_plot_data(services):

    plot = {}
    colors = ['red','blue']
    color_used = []
    js_datasets = []

    for service,rates in services.items():
        lst = []
        for rate in rates:
            lst.append("{{x:'{}', y:{} }}".format(rate.rate_date.strftime('%Y-%m-%d %H:%M:%S'),rate.rate_morning))
        plot[service] = {}

        # Ensure that the color of lines representing a service do not have the same color
        while True:
            selected_color = random.choice(colors)

            if selected_color not in color_used:
                plot[service]['color'] = selected_color
                color_used.append(selected_color)
                break

        plot[service]['data'] = "[" + ",".join(lst) + "]"
        jsvar = service.replace(" ","")
        plot[service]['jsvar'] = jsvar
        js_datasets.append(jsvar)

    retval = {'services': plot, 'datasets': "[" + ",".join(js_datasets) + "]"}

    return retval


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RatesForm()

    if form.validate_on_submit():
        for_date = form.for_date.data
        to_date = form.to_date.data

        if for_date > to_date:
            flash("'From date' cannot be greater than 'To date'")
            return render_template('index.html', form=form)

    
        rates_for_services = get_rates(for_date,to_date)
        plot_data = get_plot_data(rates_for_services)

    else:
        for_date = form.for_date.default
        to_date = form.to_date.default
        rates_for_services = get_rates(for_date, to_date)
        plot_data = get_plot_data(rates_for_services)
    
    return render_template('graph.html',
                            services=plot_data,
                            form=form)

