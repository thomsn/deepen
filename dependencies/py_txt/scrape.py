import os


class ScrapePyTxtDeps():
    @staticmethod
    def check(root):
        return os.path.isfile(os.path.join(root, 'requirements.txt'))

    def scrape_dependency(self, line):
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

    def scrape(self, root):
        with open(os.path.join(root, 'requirements.txt')) as req_file:
            dependancies = []
            for line in req_file.readlines():
                line = line.strip()
                if line[0] != '#' and len(line):
                    req = self.scrape_dependency(line)
                    dependancies.append(req)
        return dependancies

