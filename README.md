# paypal_experiment
Trying out PayPal API

First, you'll want to create a virtualenv environment.  The Makefile allows you to do:
```
    # for Python 2
    make default
    . py2_venv/bin/activate

    # for Python 3
    make default3
    . py3_venv/bin/activate
```

scripts to try

```
    # meant to be used with sandbox credentials
    python first_test_script.py --find_payment
    # ...or...
    python first_test_script.py --create_payment

    # tries to find payments, should be used with live credentials
    python paypal_goldfinger/app.py

    python try_invoice.py
```

