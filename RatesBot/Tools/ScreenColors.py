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

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'
    
    def blue(self,txt):
        return self.BLUE + txt + self.ENDC

    def green(self,txt):
        return self.GREEN + txt + self.ENDC
        
    def red(self,txt):
        return self.RED + txt + self.ENDC
        
    def yellow(self,txt):
        return self.YELLOW + txt + self.ENDC
        
    def fail(self,txt):
        return self.FAIL + txt + self.ENDC
        
    def bold(self,txt):
        return self.BOLD + txt + self.ENDC
        
    def bgred(self,txt):
        return self.BGRED + txt + self.ENDC
        
    def white(self,txt):
        return self.WHITE + txt + self.ENDC
        
       
clr = bcolors()