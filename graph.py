
import sys
import re
import os
import time
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand





if __name__ == '__main__':

	#Get da logz
	print "=====Generating logs from Git Repos====="
	for item in os.listdir("../"):
		gitDir = item
		print gitDir

		os.chdir("../"+gitDir)
		os.system("git --no-pager log --name-status --date=iso --reverse> ../seng371/input/"+gitDir+"-log.txt")

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
					

				else:
					
					diff = abs(added - delete)
					stats = [added,delete,modify, diff]
					if (added == 0 and delete == 0):
						pass
		
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
						date = dateutil.parser.parse(date)
						print date
						plt.scatter(date, scale, c=color, s=scale, label=color,
                alpha=alpha, edgecolors='none')
						

					added = 0
					delete = 0
					modify = 0
					diff = 0


			plt.grid(True)
			plt.show()