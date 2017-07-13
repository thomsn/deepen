import sys
from flask import Flask, request, render_template, redirect, flash
from compare_packages import compare_requirements
from dependancies.deps import get_deps
from pymongo import MongoClient

app = Flask(__name__)

db = MongoClient('localhost:27017').deepen

@app.route('/projects', methods=['GET'])
def new_project():
    return render_template('new.html', api=request.url_root)

@app.route('/projects/<name>')
def show_project(name):
    matching_projects = list(db.projects.find({'name': name}))
    return render_template('project.html', project=matching_projects[0])


@app.route('/projects', methods=['POST'])
def create_project():
    data = dict((key, request.form.getlist(key)) for key in request.form.keys())
    name = data['name'][0]
    url = data['url'][0]
    db.projects.insert_one(
        {
            'name': name,
            'repo_url': url,
            'deps': compare_requirements(get_deps(url))
        }
    )
    return redirect("projects/{}".format(name), code=302)
