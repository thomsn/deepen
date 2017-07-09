from os import abort

import sys
from flask import Flask, request, render_template, redirect
import json

from compare_packages import compare_requirements
from scrape import scrape
app = Flask(__name__)

projects = {
    'test': {
        'depen': [
            {
                'name': 'Hello',
                'version': '123'
            }
        ]
    }
}


@app.route('/projects', methods=['GET'])
def new_project():
    return render_template('new.html', api=request.url_root)

@app.route('/projects/<name>')
def show_project(name):
    return render_template('project.html', deps=projects[name]['depen'])


@app.route('/projects/<name>/depen', methods=['GET'])
def get_dependancies(name):
    return json.dumps(projects[name]['depen'])


@app.route('/projects', methods=['POST'])
def create_project():
    data = dict((key, request.form.getlist(key)) for key in request.form.keys())
    name = data['name'][0]
    url = data['url'][0]
    print(name, url, file=sys.stderr)
    projects[name] = {
        'url': 'url',
        'depen': compare_requirements(scrape(url))
    }
    return redirect("projects/{}".format(name), code=302)


@app.route('/projects/<name>/depen', methods=['UPDATE'])
def update_dependancies(name):
    dependancies = scrape(projects[name]['url'])
    projects[name]['depen'] = dependancies
    return json.dumps(projects[name])


