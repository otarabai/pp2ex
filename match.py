import sys
from pp2ex import blast

def main(argv):
    if len(argv) < 3:
        print "Usage: %s <sequence> <hits>" % argv[0]
        return

    b = blast.Blast('db.fasta')
    print b.run(argv[1], argv[2])

if __name__ == "__main__":
    main(sys.argv)
