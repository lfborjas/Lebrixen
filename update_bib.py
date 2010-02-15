#!/usr/bin/env python
import os

temp_file='temp.bib'
thesis_file='avance1.bib'
open_temp=open(temp_file, 'r')
open_thesis=open(thesis_file, 'r')
temp = open_temp.read()
thesis = open_thesis.read()
open_temp.close()
open_thesis.close()

if  temp.strip() != 'NULL' and temp not in thesis: 
	#update the thesis file
	os.system('cat %s >> %s'%(temp_file, thesis_file))
	#leave the temp file blank:
	os.system('echo "NULL" > %s'%temp_file)
else:
	print "Nothing to update"
	


