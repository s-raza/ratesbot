import schedule
import time
from Rates.GetRates import check_rates

def main(freq_mins=5):

    check_rates()
    schedule.every(freq_mins).minutes.do(check_rates)

    while 1:

        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception, e:
            print("Exception : {}".format(e))
            continue
