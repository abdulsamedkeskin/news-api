from flask import Blueprint, request
import feedparser
from ..constants import src
from dateutil import parser
from dateutil.tz import gettz
from datetime import datetime, time

news = Blueprint("news", __name__, url_prefix="/news")

@news.route("/<news_site>", methods=['GET'])
def index(news_site):
    sites = src.keys()
    if not news_site in sites:
        return {"status": 400, "message": "wrong site"}, 400
    news = feedparser.parse(src[news_site])
    items = ['title', 'link', 'published', 'summary', 'author','media_content']
    results = []
    for i in news.entries:
        res = {}
        for _ in i.keys():
            if _ in items:
                res.update({f"{_}": i[_]})
        results.append(res)
    return results

@news.route("/all", methods=['GET'])
def all():
    results = []
    for k,v in src.items():
        results_ = []
        news = feedparser.parse(v)
        items = ['title', 'link', 'published', 'summary', 'author','media_content']
        for i in news.entries:
            res = {}
            for _ in i.keys():
                if _ in items:
                    res.update({f"{_}": i[_]})
            results_.append(res)
        results.append({"source": k, "results": results_})
    return results

@news.route("/latest_news", methods=['GET'])
def latest_news():
    default_date = datetime.combine(datetime.now(),time(0, tzinfo=gettz("Europe/Istanbul")))
    results = []
    for k,v in src.items():
        news = feedparser.parse(v)
        items = ['title', 'link', 'published', 'summary', 'author','media_content']
        total = 0
        for i in news.entries[:2]:
            res = {}
            for _ in i.keys():
                if _ in items:
                    if _ == "published":
                        print(i[_])
                        i[_] = parser.parse(i[_], default=default_date)
                    res.update({f"{_}": i[_]})
            results.append(res)
    return sorted(results, key= lambda x: x['published'], reverse=True)