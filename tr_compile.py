import os
import sys

if sys.platform == 'win32':
	pybabel = 'venv\\scripts\\pybabel'
else:
	pybabel = 'venv/bin/pybabel'

if len(sys.argv) != 2:
	print "usage tr_init <language-code>"
	sys.exit(1)

os.system(pybabel + ' compile -d app/translations')


