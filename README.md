# Document Analysis Platform
This Flask based platform provides an alternative to website hopping for those researching current events.

My daily routine is to use Seek and Store to pull articles about a handful of news stories I'm interested in. Then I ask questions to the bot about what I want to know. This is an extremely fast way to find objective information while avoiding ads, SEO optimized filler content, and alarmist language.

## Contents
- [Structure](#structure)
- [GettingStarted](#gettingstarted)
- [SeekAndStore](#seekandstore)
- [Q&A](#q&a)
- [NER](#NER)
- [Summarizer](#summarizer)


##  Structure

#### File Structure
app &emsp;&emsp;&emsp;&emsp;- Flask application engine, routing via routes<span>.py, and HTML/CSS
instance  &emsp; - SQLite database location
models &emsp;&emsp;- the model classes used by SQLAlchemy to define table schema.
tools/&emsp;&emsp;&emsp;- functions primarily called in routes<span>.py
&emsp;--  clean<span>.py
&emsp;--  general<span>.py
&emsp;-- ner<span>.py
&emsp;-- search<span>.py
&emsp;-- sql_utils.py
&emsp;-- summary<span>.py
&emsp;-- vdb_utils.py
gitignore
settings.json&emsp;- holds YOUR keys for Flask Security, Google Search, OpenAI
README<span>.md
requirements.txt

## GettingStarted
Before this app is functional both databases need to be initialized.

#### SQLite
- create database instance
- create tables referenced in model classes. This is how the **flasksqlalchemy** library defines schema.

#### Weaviate
- Run Weaviate database from docker.
- Connect via client and create 'Text_chunk' schema
     
## SeekAndStore
The Seek and Store page connects Google Search API to SQLite and Weaviate databases. Users enter queries into a search box and results are returned, the articles are then retrieved and stored for later analysis.

## Q&A
The Q&A page allows users to ask questions to an OpenAI chatbot that can reference text retrieved from searches. The user input is embedded, a vector search for relevant text performed and the most relevant context is provided to the chatbot for a response. The context used is provided to the user (along with a few other metrics) for transparency.

## NER
The NER page provides a visualization of who an article names along with a frequency count. Very often articles about the same topic contain entirely different (not contradictory) information. A measurement of who is named provides a quick insight into the information contained in an article.

For now this a visualization - eventually I see this data being used in a similarity metric at the document and source level.

## Summarizer
Input a URL and read a summary of the text  in the article.

- newspaper3k library handles both scraping and summarization for now.






