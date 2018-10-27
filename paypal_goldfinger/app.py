
import argparse
import datetime
import dateutil.relativedelta
from dotenv import load_dotenv
import json
import pprint
import logging
import paypalrestsdk
import os
import sys


class PaypalGoldfinger:

    def __init__(self):
        load_dotenv(verbose=True)
        self._the_paypal_mode=os.getenv("PAYPAL_CLIENT_MODE")
        self._the_paypal_id=os.getenv("PAYPAL_CLIENT_ID")
        self._the_paypal_secret=os.getenv("PAYPAL_CLIENT_SECRET")

        self._pp_api = paypalrestsdk.configure(
            {
                "mode": self._the_paypal_mode,
                "client_id": self._the_paypal_id,
                "client_secret": self._the_paypal_secret
            }
        )
        logging.basicConfig(level=logging.INFO)


    def nonce(self):
        return True

    def print_payment_info(self,p):
        """Print details of single payment."""
        print('ID: {0}'.format(p.id))
        print('create_time: {0}'.format(p.create_time))
        print(
            'payer name: {0} {1}'.format(
                p.payer.payer_info.first_name,
                p.payer.payer_info.last_name
            )
        )
        print('payer email: {0}'.format(p.payer.payer_info.email))
        print('state: {0}'.format(p.state))
        for txn in p.transactions:
            print('* Invoice: {0}'.format(txn.invoice_number))
            print('  Description: {0}'.format(txn.description))
            print('  Amount: {0}'.format(txn.amount))

    def find_payment(self):
        """Simple payment query from API docs example."""
        payment_history = paypalrestsdk.Payment.all({"count": 10})
        for pmt in payment_history.payments:
            self.print_payment_info(pmt)

    def eval_min_datetime(self,max_datetime,n_months):
        """Find min time n_months before max"""
        interval = dateutil.relativedelta.relativedelta(
            months=n_months
        )
        return max_datetime - interval

    def get_utc_now(self):
        """return current time in UTC"""
        return datetime.datetime.utcnow()

    def format_timestamp(self,timeval):
        return timeval.strftime('%Y-%m-%dT%H:%M:%SZ')

    def troll_payments(self,start_dt,end_dt,showprogress=False):
        n_pmts = 0
        payment_dict = {}
        cur_end_time = end_dt
        cur_start_tstamp = self.format_timestamp(start_dt)
        cur_end_tstamp = self.format_timestamp(end_dt)
        print('Starting from: {0!r} {1!r}'.format(start_dt,cur_start_tstamp))
        print('Ending at: {0!r} {1!r}'.format(end_dt,cur_end_tstamp))
        qterm = {
            'count': 10,
            'sort_by': 'create_time',
            'sort_order': 'desc',
            'end_time': '2018-07-07T14:13:41Z',
            'start_time': '2018-06-04T14:13:41Z'
            # 'start_time': cur_start_tstamp,
            # 'end_time': cur_end_tstamp
        }
        while cur_end_time > start_dt:
            print(repr(qterm))
            cur_pmts_retval = paypalrestsdk.Payment.all(qterm)
            new_end_tstamp = cur_end_tstamp
            for p in cur_pmts_retval.payments:
                if p.id not in payment_dict:
                    payment_dict[p.id] = p
                    if new_end_tstamp > p.create_time:
                        new_end_tstamp = p.create_time
                    n_pmts += 1
                if showprogress:
                    print('Payments Collected: {0} Time: {1}'.format(
                        n_pmts,new_end_tstamp
                    ))
            cur_end_tstamp = new_end_tstamp
            qterm['start_time'] = cur_end_tstamp
            cur_end_time = datetime.datetime.strptime(
                cur_end_tstamp,
                '%Y-%m-%dT%H:%M:%SZ'
            )
        return payment_dict

    def run_main(self,runmain_arglist=None):
        prsr = argparse.ArgumentParser()
        prsr.add_argument('--find_payment',default=False,action='store_true')
        opts = prsr.parse_args(runmain_arglist)
        endtime = self.get_utc_now()
        starttime = self.eval_min_datetime(endtime,1)
        got_pmts = self.troll_payments(starttime,endtime,showprogress=True)
        return 1

def main(main_arglist=None):
    ap = PaypalGoldfinger()
    return ap.run_main(runmain_arglist=main_arglist)

if __name__ == '__main__':
    sys.exit(main())
