import sys
from flask import Flask, request, render_template, redirect, flash, url_for
from dependancies.deps import get_deps
from pymongo import MongoClient

from release_notes.scrape import scrape

app = Flask(__name__)
db = MongoClient('localhost:27017').deepen


def find_updates(version, all_versions):
    updates = []
    for ver in all_versions:
        if ver['name'] == version:
            break
        updates.append(ver)
    if len(updates) == len(all_versions): # if the version is not in versions
        return []
    else:
        return updates


def find_number_bugs(version, updates):
    num_bugs = 0
    for update in updates:
        for note in update['notes']:
            if note['bug']:
                num_bugs += 1
    return num_bugs

def get_dependencies(dependancies):
    full_dependencies = []
    for project_dependency in dependancies:
        matching_deps = list(db.dependencies.find({'name': project_dependency['name']}))
        if len(matching_deps) and 'version' in project_dependency:
            dependency = matching_deps[0]
            updates = find_updates(project_dependency['version'], dependency['versions'])
            full_dependencies.append({
                'name': dependency['name'],
                'page_url': url_for('get_dependency', name=dependency['name']),
                'info': {
                    'current_version': project_dependency['version'],
                    'latest_version': dependency['versions'][0]['name'],
                    'num_updates': len(updates),
                    'num_bugs': find_number_bugs(project_dependency['version'], updates),
                    'updates': updates # must make only updates
                }
            })
        elif len(matching_deps):
            full_dependencies.append(
                {
                    'name': project_dependency['name'],
                    'page_url': url_for('get_dependency', name=project_dependency['name']),
                    'info': {
                        'current_version': dependency['versions'][0]['name'],
                        'latest_version': dependency['versions'][0]['name'],
                        'num_updates': '0',
                        'num_bugs': '0',
                        'updates': matching_deps[0]['versions']
                    }
                }
            )
        else:
            full_dependencies.append(
                {
                    'name': project_dependency['name'],
                    'page_url': url_for('get_dependency', name=project_dependency['name'])
                }
            )
    return full_dependencies


@app.route('/dependency/<name>', methods=['GET'])
def get_dependency(name):
    matching_deps = list(db.dependencies.find({'name': name}))
    if len(matching_deps):
        dependency = matching_deps[0]
        return render_template('dependency_page.html', dependency=dependency)
    else:
        return render_template('dependency_page.html', dependency={
                'name': name
            }
        )


@app.route('/dependency/<name>', methods=['POST'])
def create_dependency(name):
    data = dict((key, request.form.getlist(key)) for key in request.form.keys())
    url = data['url'][0]
    new_dep = {
        'name': name,
        'release_note_url': url,
        'versions': scrape(url),
    }
    matching_deps = list(db.dependencies.find({'name': name}))
    if len(matching_deps):
        db.dependencies.replace_one({'name': name}, new_dep)
    db.dependencies.insert_one(new_dep)
    return render_template('dependency_page.html', dependency=new_dep)


@app.route('/', methods=['GET'])
def get_project():
    # get the url
    url = request.args.get('url')
    if not url:
        return render_template('entry_page.html')
    else:
        url = url.lower()

    # get the project
    matching_projects = list(db.projects.find({'repo_url': url}))
    if len(matching_projects):
        project = matching_projects[0]
    else:
        project = {
            'repo_url': url,
            'deps': get_deps(url)
        }
        db.projects.insert_one(project)

    # get the dependancies
    project['deps'] = get_dependencies(project['deps'])

    return render_template('project_page.html', project=project)

