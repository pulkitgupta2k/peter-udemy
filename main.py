import requests
from requests.auth import HTTPBasicAuth
from creds import client_secret, client_id
from pprint import pprint

from flask import Flask, request, render_template, redirect

app = Flask(__name__)
endpoint = "https://www.udemy.com/api-2.0/"
NAME = "Peter Alkema"

def get_page(link):
    response = requests.get(link, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()

def search_term(term):
    link_1 = endpoint + "courses/?page="
    link_2 = "&search=" + term
    rank = 1
    for page in range(1, 11):
        link = link_1 + str(page) + link_2
        page = get_page(link)
        for course in page['results']:
            for instructor in course['visible_instructors']:
                if instructor['title'] == NAME:
                    print(rank)
                    return rank
                rank += 1
    return -1

def search_terms(terms):
    terms = [ x.strip() for x in terms.split(",") ]
    res = []
    for term in terms:
        rank = search_term(term)
        res.append({ "name": term, "rank": rank })
    return res

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        resp = request.form.to_dict()
        terms = search_terms(resp['term'])
        return render_template("index.html", terms = terms)


if __name__ == "__main__":
    app.run(debug='true', host='0.0.0.0', port='5000')
    # rank = search_term("cv")
    # rank = search_term("procurement")