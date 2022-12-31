# PAXG Price logger | Sam Greydanus | December 2022 | MIT License
import pandas as pd
import matplotlib.pyplot as plt
import time, random, requests, re, os, datetime, argparse

def get_args():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--logfile', default='paxg.csv', type=str, help='file where price data is written')
    parser.add_argument('--interval', default=10, type=int, help='logging interval (seconds)')
    parser.add_argument('--verbose', default=False, type=bool, help='print to terminal while running?')
    return parser.parse_args()


def innocent_request(url):
    n = random.randint(0,999)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'\
           f'(KHTML, like Gecko) Chrome/75.0.3770.{n:03d} Safari/537.36', 'Cache-Control': 'no-cache'}
    return requests.get(url, headers=headers).text

def try_str2float(s):
    try:
        return float(s)
    except:
        raise ValueError('This string should be convertible to a float: "{}"'.format(s))

def get_paxg_price():
    text = innocent_request("https://coinmarketcap.com/currencies/pax-gold/")
    gold_section_ix = text.find('<strong>PAX Gold Price</strong>')
    paxg_price = re.split('<td>|</td>', text[gold_section_ix:gold_section_ix+100])[1]
    paxg_price = paxg_price.replace('$', '').replace(',', '')
    return try_str2float(paxg_price)

def get_xau_price():
    text = innocent_request("https://tradingeconomics.com/")
    gold_section_ix = text.find('<a href="/commodity/gold">')
    xau_price = text[gold_section_ix:gold_section_ix+600].replace(' ', '').split('\r\n')[4]
    return try_str2float(xau_price)

def get_crdoil_price():
    text = innocent_request("https://tradingeconomics.com/")
    crdoil_section_ix = text.find('<a href="/commodity/crude-oil">')
    crdoil_price = text[crdoil_section_ix:crdoil_section_ix+600].replace(' ', '').split('\r\n')[4]
    return try_str2float(crdoil_price)

def get_2yr_rate():
    text = innocent_request("https://tradingeconomics.com/united-states/2-year-note-yield")
    latest_2yr_ix = text.find('"last":')
    rate = text[latest_2yr_ix:latest_2yr_ix+15].split(':')[1]
    return try_str2float(rate)

def logging_loop(args):
    if not os.path.isfile(args.logfile):
        with open(args.logfile, 'w') as f:
            f.write('time,paxg,xau,crudeoil,us2yr\n')
    
    while True:
        try:
            dt = datetime.datetime.now().replace(microsecond=0).isoformat()
            paxg, xau, crdoil, us2yr = get_paxg_price(), get_xau_price(), get_crdoil_price(), get_2yr_rate()
            with open(args.logfile,'a') as f:
                row = '{},{},{},{},{}\n'.format(dt,paxg,xau,crdoil,us2yr)
                if args.verbose: print(row, end='')
                f.write(row)
        except:
            if args.verbose:
                print('Price logging failed for some reason (check internet)')
        time.sleep(args.interval)


if __name__ == "__main__":
    args = get_args()
    logging_loop(args)
