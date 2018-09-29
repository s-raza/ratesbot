#!/usr/bin/python
import argparse
from RatesBot.Main import main

def start(freq_mins=5):
    
    main(freq_mins=freq_mins)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--minutes", help="Frequency of checking rates in minutes")
    args = parser.parse_args()
    
    start(freq_mins=int(args.minutes))