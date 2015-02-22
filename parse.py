
import sys
import re
import os


if __name__ == '__main__':
	for item in os.listdir("../"):
		gitDir = item
		os.chdir("../"+gitDir)
		os.system("git --no-pager log --name-status > ../seng371/input/"+gitDir+"-log.txt")

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
					comment = line
				elif line.startswith("commit"):
					commit = line
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					date = line
				else:
					
					diff = abs(added - delete)
					stats = [added,delete,modify, diff]
					if (added == 0 and delete == 0):
						pass
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added > 5 and delete > 5):
						outputfile.write("This commit might be a refactor: Added " + str(stats[0]) + ", Deleted " + str(stats[1]) + ", Modified " + str(stats[2]) + ", Diff " + str(stats[3])+ "\n")
						outputfile.write(commit)
						outputfile.write(date)
						outputfile.write(comment)
						outputfile.write("\n\n")

					added = 0
					delete = 0
					modify = 0
					diff = 0		