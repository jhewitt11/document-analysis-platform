# Document Analysis Platform

## Contents
- [Introduction](#introduction)
- [Summarizer](#summarizer)
- [SearchAndScrape](#searchandscrape)

## Introduction
This is a Flask based web site to gather news stories from the web and analyze them both individually and comparatively. 

The idea is to add features over time to make this a tool for both data visualization and automating ETL processes. 


## Summarizer
Input a URL and read a summary of the text before.

- newspaper3k library handles both scraping and summarization


## SearchAndScrape
Use google search API to return search results for a query, scrape the URLs for text, combine then save the data in a JSON file.

#### Query Result Data
- `totalResults` Total number of search results Google found. The function `searchGoogle` has an argument for the number of pages to be used.
- `searchTime` Google's search time.
- `results` list of `search_result` dictionaries.
- `failedResults` list of `failed_result` dictionaries
```
	query_d = {
	    'query' : query,
	    'date' : DATE,
	    'time' : CURRENT_TIME,
	    'totalResults' : totalResults,
	    'searchTime' : searchTime,
	    'results' : search_results,
	    'failedResults' : failed_extractions
	}
```

#### search_result Data

Each result that was succesfully scraped is stored in this format.

```
	search_result = {
	    "title":        result.get("title"),
	    "link":         result.get("link"),
	    "displayLink" : result.get("displayLink"),
	    "text":         article.text,
	    "snippet":      result.get("snippet"),
	    "index":        start_index + num,
	}
```
#### failed_result Data

Each result that was not able to be scraped is stored here.
```
    failed_result  = {
        "title":        result.get("title"),
        "link":         result.get("link"),
        "displayLink" : result.get("displayLink"),
        "index":        start_index + num,
    }
```

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

