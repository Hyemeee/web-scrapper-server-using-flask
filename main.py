import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"
new = f"{base_url}/search_by_date?tags=story"
popular = f"{base_url}/search?tags=story"

def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def home():
  order_by=request.args.get('order_by','popular')
  if order_by not in db:
    if order_by == 'popular':
      search=requests.get(popular)
    elif order_by == 'new' :
      search=requests.get(new)
    s=search.json()
    results=s['hits']
    db[order_by] = results
  results=db[order_by]
  return render_template("index.html",order_by=order_by,results=results)


@app.route("/<id>")
def detail(id):
  search = requests.get(make_detail_url(id))
  result= search.json()
  return render_template("detail.html", result= result)

app.run(host="0.0.0.0")


#To access parameters submitted in the URL (?key=value) you can use the args attribute:
#searchword = request.args.get('key', '')