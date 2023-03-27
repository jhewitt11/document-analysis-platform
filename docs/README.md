# Document Analysis Platform

## Contents
- [Introduction](#introduction)
- [Summarizer](#summarizer)
- [Seek And Store](#seek and store)

## Introduction
This is a Flask based web site to gather news stories from the web for both individual and comparative  analysis. 

More features will be added over time to make this a tool for both data visualization and automating ETL processes. 


## Summarizer
Input a URL and read a summary of the text before.

- newspaper3k library handles both scraping and summarization


## Seek and Store
Use google search API to return search results for a query, scrape the URLs for text, combine then save the data in a JSON file.

#### Query Result Data
- `totalResults` Total number of search results Google found. The function `searchGoogle` has an argument to set how many pages worth of results  to store.
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

#### search_result

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
#### failed_result

Each result that was not able to be scraped is stored here.
```
    failed_result  = {
        "title":        result.get("title"),
        "link":         result.get("link"),
        "displayLink" : result.get("displayLink"),
        "index":        start_index + num,
    }
```



