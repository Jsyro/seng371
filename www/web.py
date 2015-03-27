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

@bottle.get('<imgdir:re:.*>/<filename:re:.*\.png>')
def send_image(imgdir, filename):
		print os.getcwd()
		print  "um"  + "imgdir is 	" + imgdir + " filename is 	" + filename 
		return static_file(filename, root='./' + imgdir, mimetype='image/png')

@bottle.get('<filename:re:.*\.png>')
def send_image(filename):
	print "You shouldnt be here"
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

	repoDir = repo.split("/")
	if len(repoDir) == 2:
		repoDir = repoDir[1]

	repoDir = str(repoDir[0])

	if os.path.isfile("./logs/"+repoDir+".txt"):
		pass
	else:
		checkout = os.system("git clone --no-checkout https://github.com/" + repo + " tmp_" + repoDir)
		if checkout != 0:
			return "<h1>Clone failed	<small>	This could be due to your project being too large. Try running the server locally</small></h1>"
		else:
			os.chdir("./"+repoDir)
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

	filename = "./logs/"+logdir+".txt"
	inputfile = open(filename, 'r')

	lines = inputfile.readlines()

	return makeGraph(delta, firstDate, lastDate, lines, logdir, fileid)


@bottle.get("/display/<fileid>")
def openDisplay(fileid):
	with open ("display.html", "r") as output:
		data	=		output.read().replace('\n', '')
		data	= 	data.replace("<<--dir-->>", '/temp/'+fileid)
	return  data

def makeGraph(delta, firstDate, lastDate, lines, logdir, fileid):
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
		filename = './temp/' + fileid+"/-"+str(delta)+'.png'
		plt.savefig(filename)
			
		plt.clf()
		return filename

if __name__ == '__main__':
	if 'PORT' in os.environ:
		bottle.run(host='0.0.0.0', port=os.environ['PORT'])
	else:
		bottle.run(host='localhost', port='8080')
import numpy as np
from random import randint

