# webSummarizer
Initial Flask project to deploy model/inference from webserver

FILES 
	app.py - server application
		Purpose : Receive POST request with location of txt input file
					- read website from input file
					- summarize input using the library Newspaper's .NLP() method
					- output article title and summary

	posts.py - 
		Purpose : sends POST request / receives response
		
	input.txt - 
		Purpose : txt file with web address of article to be summarized

To use :
	1. confirm dependencies
	
	2. open CMD prompt in local directory
	
	3. start Flask server
		- in CMD prompt, "flask run"
	
	4. run posts.py to send POST request

