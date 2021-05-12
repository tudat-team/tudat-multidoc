import re
import yaml


def yaml2dict(path, definitions=[]):
    regex = re.compile(r".*#\s*\[(.*)\]")
    for d in definitions:
        locals()[d] = True
    with open(path) as file:
        _lines = file.readlines()
        lines = []
        for line in _lines:
            match = regex.match(line)
            if match:
                try:
                    if eval(match.groups(1)[0]):
                        lines += line
                except NameError:
                    pass
            else:
                lines += line
        dict_ = yaml.load("".join(lines), yaml.Loader)
        return dict_


if __name__ == '__main__':
    print(yaml2dict("example.yaml"))
    print(yaml2dict("example.yaml", definitions=["cpp"]))
    print(yaml2dict("example.yaml", definitions=["py"]))
    print(yaml2dict("example.yaml", definitions=["py", "cpp"]))

    # y = yaml2dict("__api__.yaml", definitions=["cpp"])
    # print(y)
    # y = yaml2dict("__api__.yaml", definitions=["cpp", "py"])
    # print(y)
