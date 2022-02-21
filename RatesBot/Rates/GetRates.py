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

from RatesBot.Services.Service import *
from RatesBot.Tools.LoggerLib import *
from RatesBot.Tools.Kwargs import Kwargs
import telegram
import RatesBot.Config as cfg

class RateChecker(Logger, Kwargs):

    def __init__(self, *args, **kwargs):
        super(RateChecker, self).__init__(*args, **kwargs)

        self.bot = telegram.Bot(token=cfg.telegram['bot_token'])
        self.chat_id = cfg.telegram['chat_id']

    def check_rates(self):
        '''
        Execute scraping and parsing of each service. If rates have changed since last checking, send a telegram message.
        This is done for each of the services implemented as a dervied class of the ServiceBase class.
        '''

        cfg.load_config()
            
        for service in ServiceBase.__subclasses__():
            
            try:
                srv = service(total_units = cfg.total_units, debug_level=self.debug_level)
                srv.get_rates()
                
                if srv.rates_changed():
                    self.logger.info("Rates changed: {}".format(srv.service_name))
                    self.logger.info("Sending Message: {}".format(srv.prices_text))
                    self.bot.send_message(chat_id=self.chat_id, text=srv.prices_text)
                else:
                    self.logger.info("Rates not Changed ({})".format(srv.service_name))

            except Exception as e:

                error = '\n\n'.join(e.args)
                msg = f"Error ({srv.service_name}):\n\n{error}"
                
                self.logger.error(msg)
                self.bot.send_message(chat_id=self.chat_id, text=msg)
            
            
                
           