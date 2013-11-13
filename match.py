import sys
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits

def main(argv):
    if len(argv) < 3:
        print "Usage: %s <sequence> <hits>" % argv[0]
        return

    b = Blast('blastdb/db.fasta')
    blastdata = b.run(argv[1], argv[2])
    print 'Blast results:\n'
    for b in blastdata:
        print '%s\t%s\t%s' % (b['matchid'], b['percentage'], b['e-value'])

    h = Hhblits('dummy')
    hhblitsdata = h.run(argv[1], argv[2])
    print '\nHHBlits results:\n'
    for h in hhblitsdata:
        print '%s\t%s\t%s' % (h['matchid'], h['percentage'], h['e-value'])

if __name__ == "__main__":
    main(sys.argv)
