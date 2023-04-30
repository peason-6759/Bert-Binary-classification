import requests 
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
page = 0
num = 0
while True:
  try:
    page+=1
    res = requests.get(f"https://api-fact-checker.line-apps.com/pub/v1/zhtw/articles/verified?size=12&sort=updatedAt,desc&page={page}&", headers=headers)
    site_json = json.loads(res.text)

    if site_json['content'] == []:
      raise Exception()
    
    for content_json in site_json['content']:
      if content_json['comments'] != []:
        num+=1
        print(content_json['content'])
        print(content_json['comments'][0]['judgement']['en'])

  except:
    print(num)
    break
