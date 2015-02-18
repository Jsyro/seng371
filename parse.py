
import sys
import re



if __name__ == '__main__':
	inputfile = open("./jquery-mobile-log.txt", 'r')
	lines = inputfile.readlines()
	added = 0 
	delete = 0 
	modify = 0 
	commitstring =""
	for line in lines:
		if line.startswith("A"):
			added = added + 1 
		elif line.startswith("D"):
			delete = delete + 1
		elif line.startswith("M"):
			modify = modify + 1
		else:
			
			stats = [added,delete,modify]
			if (added == 0 and delete == 0):
				x = 0
				#print "This commit was an update: " + str(stats)
			if (added > 5 and delete > 5):
				print "This commit might be a refactor: " + str(stats) 
				print commitstring
			
			
				
			commitstring = line
			#print "this commit had: " + str(stats) 
			#print "Added: " + str(added)
			#print "Deleted: " + str(delete)
			#print "Modify: " + str(modify)
			added = 0
			delete = 0
			modify = 0