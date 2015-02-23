
import sys
import re
import os
import time




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
					command = 'gource --start-date "'+lastdate.strip()+'" --stop-date "'+date.strip()+'" -s .1 -e 0.00000001 --key --title "' +gitDir + "     " + comment.strip() +'" --highlight-dirs'
					print command
					os.system(command)
			os.chdir(sys.path[0])