## INTRODUCTION

This python program implements a simple and basic framework for periodically checking rates of any tradeables which are available on the web (e.g. Rates of gold, silver, stocks etc.), and sending a Telegram message to a user or group if there is any change in the rates from the last check.

For demonstration, the program currently scrapes 2 websites - www.khaleejtimes.com and www.goldpricesdubai.com to retrieve the gold rates, and sends a Telegram message if the rates have changed.

## FEATURES

1. The frequency of checking rates from a website can be configured.
2. Rates are logged to a MySQL database everytime they change (SQLAlchemy). This can be used for statistical analysis later.
3. Extensible. New source websites for tradeable can be added by extending the RatesBot.Services.Service.ServiceBase base class.
4. Basic testing using pytest.
5. Configuration file for specifying :
   - Token for Telegram bot
   - Id of the chat(user or group) where the notification of a rate change will be sent
   - Database details for connecting to a MySQL database


## GETTING STARTED

Rename the Config_sample.py file to Config.py and edit it with the required details.

**Generate an authorization token for telegram bot**

After installing the Telegram app on your mobile follow instructions [here](<https://core.telegram.org/bots#6-botfather>) to generate an authorization token that is required to send requests to the Telegram bot API.

Once you have the token, update the Config.py file with it.


**Install dependencies using pip**

```
    $ pip install python-telegram-bot sqlalchemy schedule bs4 requests mysql-python urllib2 colorlog
```

**Write Your First Service**

Inherit the class *ServiceBase* which is available in *RatesBot.Services.Service* and override the *__init__()* and *get_rates()* methods to implement the extraction of rates from a web source for something that needs to be tracked. The rates can be taken from any online source like a website or an API that may be available for a service.

Make sure that the *get_rate* method populates the fields - *_rate_morning, _rate_evening, _prices_text* and returns *prices_text*.

Examples of 2 sources that provide gold rates are available in *RatesBot.Services.Service* - *class GPDRates(ServiceBase)* and *class KTRates(ServiceBase)*

**Starting the Bot**

Time in minutes can be specified when running the bot from the command line. Once the below command is run, the bot will cycle through all the services that were defined as derived classes of the *ServiceBase* class, every number of minutes as specified. If there is a change in the rates a message will be sent to the Telegram user or group which was specified in the Config.py file.

```
    $ python start_bot.py -m <time in minutes>
```

E.g. - To check the rates from the services every 10 minutes

```
    $ python start_bot.py -m 10
```
  
If the -m switch is not provided as shown below, the default frequency of checking the rates will be 5 minutes.

```
    $ python start_bot.py
```

## TO DO

1. Refactor code to comply with Python PEP 8
2. Implement a better method for registering new sources whose rates need to be tracked. This needs to be more efficient, automated and programmer friendly.
3. Add tests for the services.
4. Installation script to implement automated start-up and shut-down of the bot with the OS (systemctl)
5. Log all quries to online sources and their results to file (/var/log/ratesbot)
6. Web interface for analysing the rates stored in the MySQL database (flask, matplotlib)


## CONTRIBUTING

Contributions in any form are welcome. It can be anything from correcting grammer or spellings in the documentation to adding a new service or tests. Our goal here is to make something robust and useful.


## LICENSE


**GNU General Public License v3.0**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>