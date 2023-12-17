from flask import Flask, render_template, request
from dataclasses import asdict
import crawler
from typing import Dict, Any

app = Flask(__name__)



@app.route("/")
def get_index() -> str:
    return render_template('index.html')

@app.route("/tree")
def get_tree() -> Dict[str, Any]:
    tree = crawler.get_article_tree(request.args['search_term'])
    return asdict(tree)