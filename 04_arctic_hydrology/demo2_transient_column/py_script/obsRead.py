import linecache

def read_file(filename):
    with open(filename, 'r') as f:
        count = 0
        for line in f:
            if line[0] == '#':
                count += 1
        count += 1

    headerline = linecache.getline(filename, count)
    headerlist = headerline.split('"')
    for i in range(len(headerlist)):
        if len(headerlist[i]) == 1:
            headerlist[i] = ''
    header = list(filter(None, headerlist))
    return count, header

