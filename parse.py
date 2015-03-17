
import sys
import re
import os
import os.path
import time
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np




def main():
	os.system('cls')
	print "Options:"
	print "		generate"
	print "		parse"
	print "		graph"
	print "		gource"
	s = raw_input('Enter an option: ')

	if s in globals():
		globals()[s]()
	else:
		print "Invalid Option"
	main()

def generate():
	#Get da logz
	print "=====Generating logs from Git Repos====="
	for item in os.listdir("../"):
		gitDir = item
		print gitDir

		if (os.path.isfile("./input/"+gitDir+"-log.txt") == False): #assume log hasnt changed since last run
			os.chdir("../"+gitDir)
			os.system("git --no-pager log --name-status --date=iso --reverse> ../seng371/input/"+gitDir+"-log.txt")

def parse():
	#Parse dem logs
	print "=====Parse the logs and look for Refactors====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')
			lines = inputfile.readlines()
			added = 0 
			delete = 0 
			modify = 0 
			diff = 0
			
			commit = ""
			date = ""
			comment = ""

			for line in lines:

				if line.startswith("A	"):
					added = added + 1 
				elif line.startswith("D	"):
					delete = delete + 1
				elif line.startswith("M	"):
					modify = modify + 1
				elif line.startswith("    "):
					comment = line[4:]
				elif line.startswith("commit"):
					commit = line[7:]
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					tempdate = date
					date = line[8:-3] + "\n"
					if tempdate[:12] != date[:12]:
						lastdate = tempdate

				else:
					
					diff = abs(added - delete)
					stats = [added,delete,modify, diff]
					if (added == 0 and delete == 0):
						pass
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added > 5 and delete > 5):
						outputfile.write("0-- This commit might be a refactor: Added " + str(stats[0]) + ", Deleted " + str(stats[1]) + ", Modified " + str(stats[2]) + ", Diff " + str(stats[3])+ "\n")
						outputfile.write("1-- " + lastdate)
						outputfile.write("2-- " + date)
						outputfile.write("3-- " + comment)
						outputfile.write("\n\n")

					added = 0
					delete = 0
					modify = 0
					diff = 0

def gource():
	print "=====Grab the refactors and them through gource====="
	for name in os.listdir("./output"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./output/"+name, 'r')
			lines = inputfile.readlines()

			gitDir = name[:-8]
			print gitDir
			os.chdir("../"+gitDir)

			for line in lines:
				if line.startswith("0-- "):
					pass
				elif line.startswith("1-- "):
					lastdate = line[4:]
				elif line.startswith("2-- "):
					date = line[4:]
				elif line.startswith("3-- "):
					comment = line[4:]
					command = 'gource --start-date "'+lastdate.strip()+'" --stop-date "'+date.strip()+'" -s 1 --key --title "' +gitDir + "     " + comment.strip() +'" --highlight-dirs'
					print command
					os.system(command)
			os.chdir(sys.path[0])

def graph():
		#Parse dem logs
	print "=====Parse the logs Graph====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')
			lines = inputfile.readlines()
			added = 0 
			delete = 0 
			modify = 0 
			diff = 0
			alpha = 0
			
			commit = ""
			date = ""
			comment = ""

			for line in lines:

				if line.startswith("A	"):
					added = added + 1 
				elif line.startswith("D	"):
					delete = delete + 1
				elif line.startswith("M	"):
					modify = modify + 1
				elif line.startswith("    "):
					comment = line[4:]
				elif line.startswith("commit"):
					commit = line[7:]
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					tempdate = date
					date = line[8:-3] + "\n"
					

				else:
					
					diff = abs(added - delete)
					stats = [added,delete,modify, diff]
					if (modify > 3):
						scale = modify
						color = "purple"
						alpha = .3
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added > 1 and delete > 1):
						scale = added+delete
						if (added/delete) < 0.9:
							color = "red"
							alpha = .3
						elif (added/delete) < 1.1:
							color = "green"
							alpha = .7
						else:
							color = "blue"
							alpha = .3

					if alpha != 0:
						date = dateutil.parser.parse(date)
						plt.scatter(date, scale, c=color, s=scale, label=color,
                alpha=alpha, edgecolors='none')
						

					added = 0
					delete = 0
					modify = 0
					diff = 0
					alpha = 0


			plt.grid(True)
			plt.show()

def lines():
		#Parse dem logs
	print "=====Parse the logs Graph====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')

			x = 0
			lines = inputfile.readlines()
			added= np.array([])
			delete = np.array([])
			modify = np.array([])
			z = np.array([])
			a = 0
			d = 0
			m = 0
			commits = 0
			olddate = dateutil.parser.parse("1990-01-01 13:53:51 -0700")

			
			commit = ""
			date = ""
			comment = ""

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

					
					

				else:
					if (date > olddate + (datetime.timedelta(days=30))):
						olddate = date
						x = x + 1
						added = np.append(added, [a])
						delete = np.append(delete, [d])
						modify = np.append(modify, [commits])
						z = np.append(z, [x])
						a = 0
						d = 0
						m = 0
						commits = 0
			

			with plt.style.context('fivethirtyeight'):
				print added
				print x
				avgAdd = np.median(added)
				avgRem = np.median(delete)
				avgMod = np.median(modify)
				plt.plot(z, added - avgAdd)
				plt.plot(z, delete - avgRem)
				plt.plot(z, modify - avgMod)

			plt.show()
if __name__ == "__main__":
    main()