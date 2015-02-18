
import sys
import re



if __name__ == '__main__':
	inputfile = open("./jquery-mobile-log.txt", 'r')
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

				#print "This commit was an update: " + str(stats)
			if (added > 5 and delete > 5):
				print "This commit might be a refactor: Added " + str(stats[0]) + ", Deleted " + str(stats[1]) + ", Modified " + str(stats[2]) + ", Diff " + str(stats[3])
				print commitstring
			
			
				
			commitstring = line
			added = 0
			delete = 0
			modify = 0
			diff = 0