Jason Syrotuck, Evan Hildebrandt, Keith Rollans

# SENG 371 Group Project 2 

##1 The question you are setting out to answer
How does the file structure of the source code files affect the ability for the software project to evolve. More specifically, do deeper, functionality divided folders create a healthier software project than one where there are folders which contain large numbers of source code file? 
	
##2 The methodology you are using to answer the question
1) 	First step is measuring the health of the project	
	i.  Number of commits
	ii. Unique contributors
				
2) 	Mark every commit which involves the addition AND deletion of more than 5 files. These commits may be refactors and will be analysed later.
	
3) 	The application then reads all of the commits and counts the number of files that are updated, added, and deleted and graphs them over time (daily, weekly, monthly, and yearly)
	
4) You will then be provided a list of links to each commit on GitGHub 
	

####2.1 Any tools you are using 
1) Python

2) Gource

3) Git

4) MatPlotLib

5) Heroku
		
####2.2 How to run
1) Make sure Git and Gource are installed and avaliable from cmd
2) Download/Clone this project into the directory with other Git projects 
4) Open requirements.txt and ensure you have all the libraries listed installed on your local machine
3) Run web.py	
		
		
####2.3 Repositories of Interest
1) JQuery Mobile

2) JQuery

3) Bootstrap	

4) Rails
		
##3 The results of your experiment
Rails was found to have a significant and steady number of restructure, most of which featured a transition from a ring structure to a deeper, more functionality driven tree structure. JQuery Mobile however was found to have a very few restructures during it's elaboration. As JQuery Mobile grew larger though, there was an attempt to restructure the code and filesystem into a more maintainable state, but the frequency of revisions continued to dwindle. 


##4 An analysis of these results
With the sample set we used, we found that that almost all major changes to the file system were ones that minimized large collections of files within a single folder, and maximized the logical and functionally division of the modules of the software. Restructures to the code early and often did foster a project that was able to evolve for a longer period of time.

####4.1 An answer to your original question based on these data sources and your methodology
Source code files which tree-like are more conducive to a healthy software project. However, a project that is too mature where familiarity has taken hold will not respond positively to a major restructure. Restructures early and often, pushing for deeper and more segregated tree-like structures driven by functionality create a longer lasting project. 

####4.2 Threats to validity
 - Impact of a file being modified
 - Subjective analysis from quantitative data

####4.3 Future work
 - Recently found that git can show us the file structure, so integrate a visual representation

	
##5 Project management information
####5.1 Milestones and timelines
### Week 0

+ Finish the plan

### Week 1

+ Edit Gource to only show edits from specified user
+ Implement multi-function choice
+ Create algorithms/methods for additional graphs

### Week 2

+ Implement GIT api
+ Modify re-factor time stamp

### Week 3

+ Push all data to HTML page

## Changed/Added Features
1. **Git API** Use git api instead of local clones #5 
2. **Multi Function** Let User select which functions to run (Gource vs Chart) #6 
3. **HTML Output** Output info in an html page #7 
4. **Time Stamp** Modify "refactors" to be time between the users last commit #8 
5. **Specific Users** Display only the actions of users associated with the commit #9 
6. **Additional graphs** Additional graphs comparing different information #10 
7. **Automated Analysis** Write code to automatically analyze the Gource results #11 

####5.2 Roles of team members
		Jason Syrotuck: 
			Algorithm Writer / Documentation
		
		Evan Hildebrandt: 
			Application Programmer
		
		Keith Rollans:	
			Web Programmer / QA

	
	
