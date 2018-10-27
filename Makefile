
default: py2_venv/bin/activate Makefile

default3: py3_venv/bin/activate Makefile

py2_venv/bin/activate: Makefile
	virtualenv py2_venv
	. py2_venv/bin/activate && pip install -r requirements/python2.txt

py3_venv/bin/activate: Makefile
	virtualenv -p /usr/local/bin/python3 py3_venv
	. py3_venv/bin/activate && pip install -r requirements/python3.txt
