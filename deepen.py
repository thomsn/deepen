import sys
from flask import Flask, request, render_template, redirect, flash
from compare_packages import compare_requirements
from dependancies.deps import get_deps
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient('localhost:27017').deepen

@app.route('/', methods=['GET'])
def get_depend():
    url = request.args.get('url')
    print(url, file=sys.stderr)
    if not url:
        return render_template('new.html', api=request.url_root)

    new_project = {
        'repo_url': url,
        'deps': compare_requirements(get_deps(url))
    }
    db.projects.insert_one(new_project)
    return render_template('project.html', project=new_project)


