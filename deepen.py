import sys, os

import logging
from flask import Flask, request, render_template, redirect, flash, url_for

from dependencies import EntryException
from dependencies.deps import get_deps
from pymongo import MongoClient

from dependencies.url import clean_url
from release_notes.scrape import scrape

app = Flask(__name__)
if os.path.isfile('config.py'):
    app.config.from_pyfile('config.py')
    db = MongoClient(app.config['MONGODB_URI']).deepen
else:
    db = MongoClient()

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


def find_number_bugs(updates):
    num_bugs = 0
    for update in updates:
        for note in update['notes']:
            if note['bug']:
                num_bugs += 1
    return num_bugs


def get_dependencies(dependencies):
    full_dependencies = []
    for project_dependency in dependencies:
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
                    'num_bugs': find_number_bugs(updates),
                    'updates': list(reversed(updates))
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
                        'num_updates': 0,
                        'num_bugs': 0,
                        'updates': list(reversed(matching_deps[0]['versions']))
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
        try:
            url = clean_url(url.lower())
        except EntryException as e:
            raise e
        except Exception as e:
            logging.info(e)
            raise EntryException('Unable to access repository')

    # get the project
    matching_projects = list(db.projects.find({'repo_url': url}))

    try:
        if len(matching_projects):
            project = matching_projects[0]
        else:
            project = {
                'repo_url': url,
                'deps': get_deps(url)
            }
            db.projects.insert_one(project)

        # get the dependencies
        project['deps'] = get_dependencies(project['deps'])
        if len(project['deps']) == 0:
            raise EntryException('There where no dependancies in the project')

        return render_template('project_page.html', project=project)

    except EntryException as e:
        return render_template('entry_page.html', error=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0')