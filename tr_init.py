import os
import sys

if sys.platform == 'win32':
	pybabel = 'venv\\scripts\\pybabel'
else:
	pybabel = 'venv/bin/pybabel'

if len(sys.argv) != 2:
	print "usage tr_init <language-code>"
	sys.exit(1)

os.system(pybabel + ' extract -F babel.cfg -k lazy_gettext -o messages.pot app')
os.system(pybabel + ' init -i messages.pot -f -d app/translations -l ' + sys.argv[1])
os.unlink('messages.pot')


