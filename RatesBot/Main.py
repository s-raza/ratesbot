#!/usr/bin/python
# 
# Simple telegram bot to track the rates of tradeables available on the web (e.g. Gold),
# and send notifications on Telegram if the rate of a tradeable changes.
# Copyright (C) 2018
# Salman Raza <raza.salman@gmail.com>
#
# GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>

import schedule
import time
from RatesBot.Rates.GetRates import RateChecker

def main(freq_mins=5):

    rates = RateChecker(debug_level='d')
    rates.check_rates()
    schedule.every(freq_mins).minutes.do(rates.check_rates)

    while 1:

        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception(e):
            print("Exception : {}".format(e))
            continue
