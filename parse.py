
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
	print "=============================================================="
	print "	generate"
	print "		--generates git logs and puts them in the ./input folder"
	print "	parse"
	print "		--parses git logs and puts them in the ./output folder"
	print "	graph"
	print "		--outputs a scatter plot of the commits"
	print "	gource"
	print "		--runs gource on each of the found refactors"
	print "	lines"
	print "		--outputs a chart of the added/deleted files against commits"
	print "	clean"
	print "		--deletes contents of ./input and ./output folders"

	s = raw_input('Enter an option: ').lower()

	if s in globals():
		globals()[s]()
	else:
		print "Invalid Option"
	main()

def clean():

	folder = './input'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e

	folder = './output'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e

def generate():
	#Get da logz
	print "=====Generating logs from Git Repos====="
	for item in os.listdir("../"):
		gitDir = item
		print gitDir

		if (os.path.isfile("./input/"+gitDir+"-log.txt") == False): #assume log hasnt changed since last run
			os.chdir("../"+gitDir)
			os.system("git --no-pager log master --name-status --author-date-order --reverse --date=iso > ../seng371/input/"+gitDir+"-log.txt")


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
	s = raw_input('Enter a time delta (days): ')
	outlier = raw_input('Destroy outliers? (y/n): ').lower()
	delta = int(float(s))

	if (outlier == "y") or (outlier == "yes"):
		outlier = True
		percent = raw_input('What Percentile? (0-100): ')
		percent = int(float(percent))

	dosum = raw_input('Percentage? (y/n): ').lower()
	if (dosum == "y" )or (dosum ==  "yes"):
		dosum = True

	justify = raw_input('Justify by average? (y/n): ').lower()
	if (justify == "y" )or (justify ==  "yes"):
		justify = True

	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')

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

					if first:
						olddate = date
						first = False

					if (date > olddate + datetime.timedelta(days=delta)):
						olddate = date
						print date
						print olddate
						added = np.append(added, [a])
						delete = np.append(delete, [d])
						modify = np.append(modify, [commits])
						z = np.append(z, [date])
						a = 0
						d = 0
						m = 0
						commits = 0
			

			with plt.style.context('fivethirtyeight'):
				print "Commits: "
				print modify
				print x

				if outlier == True:
					perAdd = np.percentile(added, percent)
					perRem = np.percentile(delete, percent)
					perMod = np.percentile(modify, percent)

					added = np.clip(added, 0, perAdd)
					delete = np.clip(delete, 0, perRem)
					modify = np.clip(modify, 0, perMod)

				if justify == True:
					avgAdd = np.average(added)
					avgRem = np.average(delete)
					avgMod = np.average(modify)

					added = added - avgAdd
					delete = delete - avgRem
					modify = modify - avgMod

				if dosum == True:
					sumAdd = np.sum(added)
					sumRem = np.sum(delete)
					sumMod = np.sum(modify)

					added = added/sumAdd
					delete = delete/sumRem
					modify = modify/sumMod

				plt.plot(z, added)
				plt.plot(z, delete)
				plt.plot(z, modify)

			plt.title(name[:-8])
			plt.show()
if __name__ == "__main__":
    main()