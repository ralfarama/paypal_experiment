
from dotenv import load_dotenv
import paypalrestsdk
import logging
import os

logging.basicConfig(level=logging.INFO)

load_dotenv(verbose=True)
the_paypal_mode=os.getenv("PAYPAL_CLIENT_MODE")
the_paypal_id=os.getenv("PAYPAL_CLIENT_ID")
the_paypal_secret=os.getenv("PAYPAL_CLIENT_SECRET")

pp_api = paypalrestsdk.configure(
    {
        "mode": the_paypal_mode,
        "client_id": the_paypal_id,
        "client_secret": the_paypal_secret
    }
)

history = paypalrestsdk.Invoice.all({"page_size": 2})

print("List Invoice:")
for invoice in history.invoices:
    print("  -> Invoice[%s]" % (invoice.id))
