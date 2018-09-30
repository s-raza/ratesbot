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

**Write your first service**

Inherit the the class *ServiceBase* available in *RatesBot.Services.Service* and override the *__init__()* and *get_rates()* methods to implement the extraction of rates from a web source for something that you need to be tracked. The rates can be taken from any online source like a website or an API that may be available for a service.

Make sure that the *get_rate* method populates the fields - *_rate_morning, _rate_evening, _prices_text* and returns *prices_text*.

Examples of 2 sources of gold rates are available in *RatesBot.Services.Service* - *class GPDRates(ServiceBase)* and *class KTRates(ServiceBase)*

*Starting the Bot*

Time in minutes can be specified when running the bot from the command line. Once the below command is run, the bot will cycle through all the services that were defined as derived classes of the *ServiceBase* class, every number of minutes as specified. If there is a change in the rates a message will be send to the Telegram user of group which was specified in the Config.py file.

.. code:: shell

    $ python start_bot.py -m <time in minutes>

E.g. - To check the rates from the services every 10 minutes

.. code:: shell

    $ python start_bot.py -m 10
    
If the -m switch is not provided as shown below, the default frequency of checking the rates will be 5 minutes.

.. code:: shell

    $ python start_bot.py

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

=====
TO DO
=====
1. Refactor code to comply with Python PEP 8
2. Implement a better method for registering new sources whose rates need to be tracked. This needs to be more efficient, automated and programmer firendly.
3. Add tests for the services.
4. Installation script to implement automated start-up and shut-down of the bot with the OS (systemctl)
5. Log all quries to online sources and their results to file (/var/log/ratesbot)


=======
LICENSE
=======

**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>