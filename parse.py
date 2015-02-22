
import sys
import re
import os


if __name__ == '__main__':
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')
			lines = inputfile.readlines()
			added = 0 
			delete = 0 
			modify = 0 
			diff = 0
			commitstring =""
			for line in lines:
				if line.startswith("A"):
					added = added + 1 
				elif line.startswith("D"):
					delete = delete + 1
				elif line.startswith("M"):
					modify = modify + 1
				else:
					
					diff = abs(added - delete)
					stats = [added,delete,modify, diff]
					if (added == 0 and delete == 0):
						pass
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added > 5 and delete > 5):
						outputfile.write("This commit might be a refactor: Added " + str(stats[0]) + ", Deleted " + str(stats[1]) + ", Modified " + str(stats[2]) + ", Diff " + str(stats[3]))
						outputfile.write(commitstring)

					
						
					commitstring = line
					added = 0
					delete = 0
					modify = 0
					diff = 0		