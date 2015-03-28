import bottle 
import os
from bottle import static_file
import sys
import re
import os.path
import time
import shutil
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand
import bottle 
import os
from bottle import static_file
import sys
import re
import os.path
import time
import shutil
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np
from random import randint

@bottle.get('<imgdir:re:.*>/<filename:re:.*\.svg>')
def send_image(imgdir, filename):
		return static_file(filename, root='./' + imgdir, mimetype='image/svg+xml')

@bottle.get('<imgdir:re:.*>/<filename:re:.*\.png>')
def send_image(imgdir, filename):
		return static_file(filename, root='./' + imgdir, mimetype='image/png')

@bottle.get('<filename:re:.*\.png>')
def send_image(filename):
	return static_file(filename, root='./', mimetype='image/png')

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
	options = ""
	for name in os.listdir("./logs"):
		if name.endswith(".txt"):
			options = options + "<option value='"+str(name)[:-4]+"''>" + str(name)[:-4] + "</option>\n"

	with open ("index.html", "r") as output:
		data=output.read().replace('\n', '')
		data = data.replace("<<--OPTIONS-->>", options)

	return  data

@bottle.post('/repo')
def clone():
	repo = bottle.request.forms.get("repo")

	if '/' in repo:
		repoDir = repo.split("/")
		repoDir = repoDir[1]
	else:
		repoDir = repo

	repoDir = str(repoDir)

	if os.path.isfile("./logs/"+repoDir+".txt"):
		pass
	else:
		checkout = os.system("git clone --no-checkout https://github.com/" + repo + " tmp_" + repoDir)
		if checkout != 0:
			return "<h1>Clone failed	<small>	This could be due to your project being too large. Try running the server locally</small></h1>"
		else:
			os.chdir("./tmp_"+repoDir)
			gitlog = os.system("git --no-pager log --name-status --author-date-order --reverse --date=iso > ../logs/"+repoDir+".txt")
			os.chdir("../")

	with open ("middle.html", "r") as output:
		data=output.read()
		data = data.replace("<<--REPO-->>", repoDir)

	return  data

@bottle.get('/options/<logdir>')
def lines(logdir):
	
	filename = "./logs/"+logdir+".txt"
	inputfile = open(filename, 'r')

	lines = inputfile.readlines()

	fileid = str(randint(10000, 99999))
	os.chdir('./temp/')
	os.mkdir('./'+fileid)
	os.chdir('../')

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

	return {'firstDate' : str(firstDate), 'lastDate' : str(lastDate), 'fileid' : fileid}

@bottle.post('/graph')
def spans():

	delta = int(bottle.request.forms.get("delta"))

	firstDate = dateutil.parser.parse(bottle.request.forms.get("firstDate"))
	lastDate = dateutil.parser.parse(bottle.request.forms.get("lastDate"))

	logdir = bottle.request.forms.get("logdir")
	fileid = bottle.request.forms.get("fileid")

	af = (bottle.request.forms.get("af") == 'true')
	cf = (bottle.request.forms.get("cf") == 'true')
	df = (bottle.request.forms.get("df") == 'true')
	mf = (bottle.request.forms.get("mf") == 'true')
	uf = (bottle.request.forms.get("uf") == 'true')


	filename = "./logs/"+logdir+".txt"
	inputfile = open(filename, 'r')

	lines = inputfile.readlines()

	return makeGraph(delta, firstDate, lastDate, lines, logdir, fileid,  af, cf, df, mf, uf)


@bottle.get("/display/<fileid>/<logdir>")
def openDisplay(fileid, logdir):

	with open ("display.html", "r") as output:
		data	=	output.read().replace('\n', '')
		data	=	data.replace("<<--dir-->>", '/temp/'+fileid)
		data	=	data.replace("<<--REPO-->>", logdir)

	return  data

def makeGraph(delta, firstDate, lastDate, lines, logdir, fileid, af, cf, df, mf, uf):

		time = np.array([lastDate])
		date = lastDate

		while date > firstDate:
			date = date - datetime.timedelta(days=delta)
			time = np.append([date], time)
					
		length = time.size

		added= np.zeros(length)
		delete = np.zeros(length)
		modify = np.zeros(length)
		commits = np.zeros(length)
		unique = np.zeros(length)
		authors = [""] * length

		a = 0
		d = 0
		m = 0
		c = 0
		position = 0
			
		commit	= ""
		date	= ""
		comment	= ""
		author	= ""

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
				author = line[8:]
				author = author.split("<")[0]

			elif line.startswith("Date:"):
				c = c + 1
				tempdate = date
				date = line[8:30] + "\n"
				date = dateutil.parser.parse(date)
				position = np.searchsorted(time, date)

				if (position != 0) and (position != length):
					added[position] = added[position] + a
					delete[position] = delete[position] + d
					modify[position] = modify[position] + m
					commits[position] = commits[position] + c

					if authors[position] == 0:
						authors[position] = author

					if author in authors[position]:
						pass
					else:
						authors[position] = author + "," + authors[position]
						unique[position] = unique[position] + 1

				a = 0
				d = 0
				m = 0
				c = 0
				position = 0

		with plt.style.context('fivethirtyeight'):

			if af:
				plt.plot(time, added, label="Added")

			if df:
				plt.plot(time, delete, label="Deleted")

			if mf:
				plt.plot(time, modify, label="Modified")

			if cf:
				plt.plot(time, commits, label="Commits")

			if uf:
				plt.plot(time, unique, label="Contributors")
		
		plt.legend(loc=2)
		plt.title(logdir)
		plt.xlabel("Time")
		filename = './temp/' + fileid+"/-"+str(delta)+'.svg'
		plt.savefig(filename, format="svg")
			
		plt.clf()
		return filename

if __name__ == '__main__':
	if 'PORT' in os.environ:
		bottle.run(host='0.0.0.0', port=os.environ['PORT'])
	else:
		bottle.run(host='localhost', port='8080')
import numpy as np
from random import randint

