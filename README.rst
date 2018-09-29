============
INTRODUCTION
============
This python program implements a simple and basic framework for periodically checking rates of any tradeables which are available on the web (e.g. Rates of gold, silver, stocks etc.), and sending a Telegram message to a user or group if there is any change in rates.

For demonstration, the program currently scrapes 2 websites - www.khaleejtimes.com and www.goldpricesdubai.com to retrieve the gold rates, and sends a Telegram message if the rate changes.

===============
GETTING STARTED
===============
Rename the Config_sample.py file to Config.py and edit it with required details.

**Install dependencies**

.. code:: shell

    $ pip install python-telegram-bot sqlalchemy schedule bs4 requests mysql-python urllib2 colorlog

========
FEATURES
========
1. The frequency of checking rates from a website can be configured.
2. Rates are logged to a MySQL database everytime they change (SQLAlchemy).
3. Extensible. New source websites for tradeable can be added by extending the RatesBot.Services.Service.ServiceBase base class.
4. Basic testing using pytest.
5. Configuration file for specifying :
 - Token for Telegram bot
 - Id of the chat(user or group) where the notification of a rate change will be sent
 - Database details for connecting to a MySQL database
 
=======
LICENSE
=======

**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>