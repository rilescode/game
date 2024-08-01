import requests

cur_url = "http://www.google.com"
for i in range(10):
    response = requests.get(cur_url)
    print("headers", response.headers)
    print("body", response.text)
