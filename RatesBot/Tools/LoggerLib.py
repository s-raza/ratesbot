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

import colorlog
import logging

from RatesBot.Tools.Kwargs import Kwargs

debug_levels = {"d":logging.DEBUG,
                "i":logging.INFO,
                "w":logging.WARNING,
                "e":logging.ERROR,
                "c":logging.CRITICAL}

formatter = colorlog.ColoredFormatter(
    "%(asctime)s %(log_color)s%(levelname)-2s %(name)s-%(lineno)s: %(message)s",
    datefmt='%d%b%y %I:%M:%S%p',
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'white,bg_red',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

logger = colorlog.getLogger()

handler = colorlog.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


##Root logger logging level
logger.setLevel(logging.INFO)

def get_debug_level(level):

    retval = None

    if level is None:
        pass
    elif level in debug_levels:
        retval = debug_levels[level]
    else:
        pass

    return retval

class Logger(Kwargs):

    def __init__(self,*args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)

        self.logger = colorlog.getLogger('.'.join([self.__module__,self.__class__.__name__]))
        self.logger.disabled = True
        self.debug_level = self.init_kwarg('debug_level')
        self.debug_levels = debug_levels
                            
        if self.debug_level:
            self.logger.setLevel(get_debug_level(self.debug_level))
            self.logger.disabled = False
            
    def get_debug_level(self,level):
        
        retval = None

        if level is None:
            pass
        elif level in self.debug_levels:
            retval = self.debug_levels[level]
        else:
            pass

        return retval      


