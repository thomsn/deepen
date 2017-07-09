import subprocess

def get_latest_version(module):
    child = subprocess.run(['pip','search',module], stdout=subprocess.PIPE)
    response = str(child.stdout)
    for line in response.split('\\n'):
        if '(' in line and ')' in line:
            line = line.split(')')[0]
            version = line.split('(')[1]
            name = line.split('(')[0].strip()
            if name == module:
                return version


def test_module_name(module):
    # preventing a module name from escaping the cmd and messing with crao
    assert(module.isalnum())


def compare_requirements(requirements):
    results = []
    for requirement in requirements:
        if 'version' in requirement:
            current_version = requirement['version']
            latest_version = get_latest_version(requirement['name'])
            requirement['version'] = '{} -> {}'.format(current_version, latest_version)
            results.append(requirement)
        else:
            results.append(requirement)
    return results