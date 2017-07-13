import os
import re
from setuptools import setup


class ScrapePySetupDeps():
    @staticmethod
    def check(root):
        return os.path.isfile(os.path.join(root, 'setup.py'))

    def scrape(self, root):
        dependancies = []
        with open(os.path.join(root, 'setup.py')) as req_file:
            text = req_file.read()
            setup_deps = []
            install_requires = re.search(re.compile(r"install_requires\s*=\s*\[([^\]]*)\]"), text)
            if install_requires:
                setup_deps.extend(install_requires.group(1).split(','))

            extras_require = re.search(re.compile(r"extras_require\s*=\s*\{([^\}]*)\}"), text)
            if extras_require:
                for extra in re.compile(r"\[([^\]]*)\]").findall(extras_require.group(1)):
                    setup_deps.extend(extra.split(','))

            for dep in setup_deps:
                for char in ',\'\" ':
                    dep = dep.replace(char, '')
                dep = dep.strip()
                if len(dep):
                    version = None
                    name = dep
                    for comparison in ['<', '>', '=', '<=', '>=', '==', '!=']:
                        if comparison in dep:
                            name = dep.split(comparison)[0].strip()
                            version = dep.split(comparison)[1].strip()
                    if version:
                        dependancies.append({'name': name, 'version': version})
                    else:
                        dependancies.append({'name': name})

        return dependancies

