import requests
import os


resp = requests.post("http://localhost:5000/summarize",
                     files={"file": open('input.txt')})
                     

print("Response is : \n", resp.json())