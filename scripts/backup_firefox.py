#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite
import os
from datetime import datetime
#TO GET THE TABLES IN THE SQLITE FILE: SELECT * FROM sqlite_master WHERE type='table (when already connected)
FIELD_MAX_WIDTH = 50
#read the firefox download database and print it to a file:
home=os.environ['HOME']
downloads_file=os.path.join(home, '.mozilla','firefox','uqzxwi9f.default', "downloads.sqlite")
if os.path.exists(downloads_file):
	con=sqlite.connect(downloads_file)
	cur=con.cursor()
	cur.execute("SELECT * FROM moz_downloads")
	destination=open('downloads_backup', 'w')
#	for row in cur:
#		destination.write(repr(row)+'\n')
#	destination.close()

	# Print a header.
	destination.write("Backup made on %s \n\n"%datetime.now().strftime('%A %B %d %Y, %H:%M'))
	for fieldDesc in cur.description[1:3]:
		destination.write(fieldDesc[0].ljust(FIELD_MAX_WIDTH))
	destination.write( '\n'+('-' * 100)+'\n')

	# For each row, print the value of each field left-justified within
	# the maximum possible width of that field.
	fieldIndices = [1,2]
	for row in cur:
		for fieldIndex in fieldIndices:
			fieldValue = str(row[fieldIndex])
			destination.write(fieldValue.ljust(FIELD_MAX_WIDTH)) 
		destination.write('\n')
	
	destination.write('\n')
	destination.close()


