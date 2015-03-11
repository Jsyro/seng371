Jason Syrotuck, Evan Hildebrandt, Keith Rollans

# SENG 371 Group Project 1 

##1 The question you are setting out to answer
	Does the file structure of the source code affect the ability for the project to evolve? 
	
##2 The methodology you are using to answer the question
	Anaylze release and tag them based on, Security Update, Bug fixes, feature releases, preformance improvements, refactors.
	Use some statistics on these to understand the frequency of these types of updates. Visually inspect the codebase using
	dependancy visualization tools (Gource) to gain details of the nature of these changes. 

####2.1 Any tools you are using 
		1. Python
		2. Gource
		3. Git
		
####2.2 A copy of your source code, and instructions on how people can compile / run your code
		1. Make sure Git and Gource are installed and avaliable from cmd
		2. Download/Clone this project into the directory with other Git projects 
		3. Run parse.py		
		
####2.3 A list of the data sources (repos, posts, etc) you are using for your experiment
		1. JQuery Mobile
		2. JQuery
		3. Bootstrap	
		4. Rails
		
####2.4 A list of the metrics you are collecting, justifying their use in answering your question
		1. Number of files added, removed, and modified. 
		2. Commit message string
	
##3 The results of your experiment
		We found that refactors typically show two different results of a refactors
			1. New divisions by modules <picture> 
			2. New tree structure to show functionality (more reference errors, bigger follow up fix) 
			
<picture>![Ring](https://raw.githubusercontent.com/Jsyro/seng371/master/ring.png)

<picture>![Tree](https://raw.githubusercontent.com/Jsyro/seng371/master/tree.png)

##4 An analysis of these results

####4.1 An answer to your original question based on these data sources and your methodology
Projects in early life tend to end up with ring formations, and as the project evolves, more tree like structures (based around functionality) appear. Rails however, had more refactors early on to maintain a tree structure and not letting large folders (25 source code files in a single folder is usually broken down quickly, assets folders and testing models tended to stay large but eventaully did get broken down.) Rails last major refactor is in 2013, but has a very active base of collaborators with contiuous commits and additions.   
####4.2 Threats to validity
Because the observations are qualitative rather than quantitative there could be some discrepency between how people chose to interpret the outputs.
####4.3 Future work
Change gource to show only the changes of the committer or the refactor and change the start-end date to be their last commit (if available)
	
##5 Project management information
####5.1 Milestones and timelines
		1. Downloading the repositories for inspection.
		2. Producing a filtered gitlog containing only refactors (Python program).
		3. Running Gource to get a visual representation of the change to the file structure.
		
####5.2 Roles of team members
		Jason Syrotuck: 
			Algorithm Writer
		
		Evan Hildebrandt: 
			Programmer
		
		Keith Rollans:	
			Support

	
	
