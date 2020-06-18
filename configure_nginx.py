import re


def remove_server(hostname, config_file):
    f = open(config_file, 'r')
    lines = f.readlines()
    f.close()

    for l in lines:
        if re.search(hostname, l):
            lines.pop(lines.index(l))

    f = open(config_file, 'w+')

    for l in lines:
        f.write(l)

    f.close()


def add_server(hostname, config_file):
    f = open(config_file, 'r')
    lines = f.readlines()
    f.close()

    for l in lines:
        if re.search(r'upstream', l):
            lines.insert(lines.index(l) + 1, '\t\tserver ' + hostname + ';\n')

    f = open(config_file, 'w+')
    for l in lines:
        f.write(l)
    f.close()


# remove_server('192.168.1.1')
# add_server('192.168.1.1')