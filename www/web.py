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
import urllib2
import json
import base64
import markdown

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
	for name in sorted(os.listdir("./logs")):
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
		repoDir = repo.replace("/", "_")
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
			gitlog = os.system("git --no-pager log --name-status --no-merges --pretty=format:%h%x09%an%x09%ad%x09%s%x09{LINE} --date=iso > ../logs/"+repoDir+".txt")
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
		if "{LINE}" in line:
			date = line.split("\t")[2][:25]
			if date[22] > 1:
				date = date[:20] + "+0000"

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

	res = (bottle.request.forms.get("res") == 'true')
	print res

	mod = bottle.request.forms.get("mod")


	filename = "./logs/"+logdir+".txt"
	inputfile = open(filename, 'r')

	lines = inputfile.readlines()

	return makeGraph(delta, firstDate, lastDate, lines, logdir, fileid,  af, cf, df, mf, uf, mod, res)


@bottle.get("/display/<fileid>/<logdir>")
def openDisplay(fileid, logdir):

	images = ""
	temp = sorted(os.listdir("./temp/" + fileid))
	first = '/temp/'+ fileid + "/" + temp[1]
	for name in temp:
		if name.endswith(".png"):
			name = name.split('/')[-1]
			images = images + '\n<div class="col-sm-3 col-xs-6 graph-small">\n <img class="img-responsive portfolio-item" src="/temp/'+ fileid + "/" + name + '" ></div>\n'
	repo = logdir.replace("_", "/")
	readme = markdown.markdown(unicode(base64.b64decode(json.loads(urllib2.urlopen("https://api.github.com/repos/" + repo + "/readme").read())["content"]), errors='ignore'))
	with open ("display.html", "r") as output:

		data	=	output.read()
		data	=	data.replace("<<--IMG-->>", images)
		data	=	data.replace("<<--FIRST-->>", first)
		data	=	data.replace("<<--REPO-->>", logdir)
		data	=	data.replace("<<--README-->>", readme)

	return  data

def makeGraph(delta, firstDate, lastDate, lines, logdir, fileid, af, cf, df, mf, uf, mod, res):

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
			if line.startswith("M	"):
				m = m + 1
			elif line.startswith("D	"):
				d = d + 1
			elif line.startswith("A	"):
				a = a + 1
			elif "{LINE}" in line:
				values = line.split("\t")
				sha = values[0]
				author = values[1]
				date = values[2][:25]
				if date[22] > 1:
					date = date[:20] + "+0000"

				comment = values[3]
				date = dateutil.parser.parse(date)

			else:

				position = np.searchsorted(time, date)

				if (position != 0) and (position != length):
					added[position] = added[position] + a
					delete[position] = delete[position] + d
					modify[position] = modify[position] + m
					commits[position] = commits[position] + 1

					if authors[position] == 0:
						authors[position] = author

					if author in authors[position]:
						pass
					else:
						authors[position] = author + "," + authors[position]
						unique[position] = unique[position] + 1

					if res:
						if (a > 10) and (d > 10):
							plt.scatter(date, -20, c='Black', s=a+d, alpha=1, edgecolors='none')

				a = 0
				d = 0
				m = 0
				c = 0
				position = 0


		if mod == "none":
			pass
		elif mod == "avg":
			added = added - np.average(added)
			delete = delete - np.average(delete)
			modify = modify - np.average(modify)
			commits = commits - np.average(commits)
			unique = unique - np.average(unique)
		elif mod == "avgp":
			added = 100 * added / np.average(added)
			delete = 100* delete / np.average(delete)
			modify = 100* modify / np.average(modify)
			commits = 100* commits / np.average(commits)
			unique = 100* unique / np.average(unique)
		elif mod == "maxp":
			added = 100* added / np.amax(added)
			delete = 100* delete / np.amax(delete)
			modify = 100* modify / np.amax(modify)
			commits = 100* commits / np.amax(commits)
			unique = 100* unique / np.amax(unique)


		with plt.style.context('fivethirtyeight'):
			if (mod == "maxp") or (mod == "avgp"):
				plt.ylabel("percentage")
			else:
				plt.ylabel("number")
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

		deltaName = '0'*(5 - len(str(delta))) + str(delta)

		filename = './temp/' + fileid+"/" + logdir + "-"+deltaName+'.png'
		plt.savefig(filename, format="png")
			
		plt.clf()
		return filename

if __name__ == '__main__':
	if 'PORT' in os.environ:
		bottle.run(host='0.0.0.0', port=os.environ['PORT'])
	else:
		bottle.run(host='localhost', port='8080')


