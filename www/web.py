import bottle 
import os
from bottle import static_file
import sys
import re
import os.path
import time
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
from random import randint

@bottle.get('<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='./', mimetype='image/png')

@bottle.get('<imgdir>/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='./'+imgdir, mimetype='image/png')

@bottle.get('<filename>')
def server_static(filename):
    return static_file(filename, root='./')


@bottle.get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='./css')

@bottle.get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='./images')

@bottle.get('/js/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='./js')

@bottle.get('/')
def index():
    return static_file('index.html', root='./')

@bottle.post('/repo')
def clone():
	repo = bottle.request.forms.get("repo")
	repoDir = str(randint(1000,9999)) + repo.split("/")[1]
	checkout = os.system("git clone --no-checkout https://github.com/" + repo + " " + repoDir)
	if checkout == 0:
		os.chdir("./"+repoDir)
		gitlog = os.system("git --no-pager log master --name-status --author-date-order --reverse --date=iso > log.txt")
		os.chdir("../")
		return "<a href='/"+ repoDir + "''> Click here to generate Graphs </a>"
	else:
		return "<h1>Clone failed	<small>	This could be due to your project being too large. Try running the server locally</small></h1>"

@bottle.get('/<logdir>')
def lines(logdir):
	filename = "./"+logdir+"/log.txt"
	inputfile = open(filename, 'r')

	lines = inputfile.readlines()

	firstDate = ""
	lastDate = ""
	first = True
	for line in lines:
		if line.startswith("Date:"):
			date = line[8:30] + "\n"
			date = dateutil.parser.parse(date)
			if first:
				firstDate = date
				lastDate = date
				first = False
			else:
				if date < firstDate:
					firstDate = date
				if date > lastDate:
					lastDate = date

	spans = [1,7,30,180,365]
	for delta in spans:
		time = np.array([lastDate])
		date = lastDate

		while date > firstDate:
			date = date - datetime.timedelta(days=delta)
			time = np.append([date], time)
					
		length = time.size
		print length
		added= np.zeros(length)
		delete = np.zeros(length)
		modify = np.zeros(length)
		a = 0
		d = 0
		m = 0
		commits = 0
		position = 0
			
		commit = ""
		date = ""
		comment = ""
	
		first = True
	
		for line in lines:
			if line.startswith("A	"):
				a = a + 1 
			elif line.startswith("D	"):
				d = d + 1
			elif line.startswith("M	"):
				m = m + 1
			elif line.startswith("    "):
				comment = line[4:]
			elif line.startswith("commit"):
				commit = line[7:]
			elif line.startswith("Author:"):
				pass
			elif line.startswith("Date:"):
				commits = commits + 1
				tempdate = date
				date = line[8:30] + "\n"
				date = dateutil.parser.parse(date)
				position = np.searchsorted(time, date)
				added[position] = added[position] + a
				delete[position] = delete[position] + d
				modify[position] = modify[position] + commits
				a = 0
				d = 0
				m = 0
				commits = 0
				position = 0
		
	 
		with plt.style.context('fivethirtyeight'):
	
			plt.plot(time, added)
			plt.plot(time, delete)
			plt.plot(time, modify)
	
		plt.title(logdir[4:])
		plt.savefig('./' + logdir+"/-"+str(delta)+'.png')
			
		plt.clf()


		with open ("display.html", "r") as output:
			data=output.read().replace('\n', '')
			data = data.replace("<<--dir-->>", logdir)

	return  data


if __name__ == '__main__':
    if 'PORT' in os.environ:
        bottle.run(host='0.0.0.0', port=os.environ['PORT'])
    else:
        bottle.run(host='localhost', port='8080')