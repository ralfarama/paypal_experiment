
import argparse
from dotenv import load_dotenv
import json
import pprint
import logging
import paypalrestsdk
import os
import sys


class PaypalFirstTest:

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

    def create_payment(self):
        if self._the_paypal_mode != 'sandbox':
            raise Exception('no payment creation in live mode!')
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")
            for lnk in payment.links:
                print(repr(lnk))
        else:
            print(payment.error)

    def find_payment(self):
        payment_history = paypalrestsdk.Payment.all({"count": 10})
        pp = pprint.PrettyPrinter(indent=2)
        pmt_dict = payment_history.to_dict()
        pp.pprint(pmt_dict)
        fh = open('dump.json','w')
        fh.write(json.dumps(pmt_dict))
        fh.close()

    def run_main(self,runmain_arglist=None):
        did_something = False
        prsr = argparse.ArgumentParser()
        prsr.add_argument('--create_payment',default=False,action='store_true')
        prsr.add_argument('--find_payment',default=False,action='store_true')
        opts = prsr.parse_args(runmain_arglist)
        if opts.create_payment:
            did_something = True
            print('Creating payment...')
            self.create_payment()
        if opts.find_payment:
            did_something = True
            self.find_payment()
        if not did_something:
            print('Nothing to do...')
        return 1

def main(main_arglist=None):
    ap = PaypalFirstTest()
    return ap.run_main(runmain_arglist=main_arglist)

if __name__ == '__main__':
    sys.exit(main())
