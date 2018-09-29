from RatesBot.Services.Service import *
import telegram
import RatesBot.Config as cfg

bot = telegram.Bot(token=cfg.bot_token)
chat_id = cfg.chat_id


def check_rates():
    '''
    Execute scraping and parsing of each service. If rates have changed since last checking, send a telegram message.
    This is done for each of the services implemented as a dervied class of the ServiceBase class.
    '''
        
    for service in ServiceBase.__subclasses__():
        
        srv = service(total_units = cfg.total_units)
        
        srv.get_rates()
        
        if srv.rates_changed():
            print clr.red("Rates changed: ") + clr.yellow(srv.service_name + " Sending Message...\n") + srv.prices_text
            bot.send_message(chat_id=chat_id, text=srv.prices_text)
        else:
            print clr.blue("Rates not Changed ({}), ".format(srv.service_name)) + clr.yellow(srv.value_text)
                
           