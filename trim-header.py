import sys

if len(sys.argv) < 2:
    print 'Usage: %s <input-file>' % sys.argv[0]
    sys.exit(0)

fi = open(sys.argv[1])
fo = open('db.fasta', 'w')

for line in fi:
    tmpline = line
    if tmpline[0] == '>':
        tmpline = '>' + tmpline.split('|')[1] + '\n'
    fo.write(tmpline)

fi.close()
fo.close()
