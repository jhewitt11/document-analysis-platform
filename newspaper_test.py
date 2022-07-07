
from newspaper import Article




inp_file = 'input.txt'

f = open(inp_file, 'r')

url = f.read()

article = Article(url, verbose=True)

try:
    article.download()
    article.parse()
    article.nlp()
    
    title = article.title
    summary = article.summary
except:
    print("error found..")

print("\nTitle is :\n{}\n\nSummary is :\n{}\n".format(title, summary))