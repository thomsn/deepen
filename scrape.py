import os
import git
import shutil

dir_name = 'temp_repo'


def scrape_requirement(line):
    if '==' in line:
        spited = line.split('==')
        name = spited[0]
        return {'name': name, 'version': spited[1]}
    elif '>=' in line:
        spited = line.split('>=')
        name = spited[0]
        return {'nme': name, 'version': spited[1]}
    else:
        return {'name': str(line)}

def scrape(url):
    try:
        os.makedirs(dir_name)
        git.Git().clone(url, dir_name)
        with open(os.path.join(dir_name, 'requirements.txt')) as req_file:
            dependancies = []
            for line in req_file.readlines():
                line = line.strip()
                if line[0] != '#' and len(line):
                    req = scrape_requirement(line)
                    dependancies.append(req)
    finally:
        shutil.rmtree(dir_name)
    return dependancies

