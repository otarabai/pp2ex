import sys
from pp2ex import Hpo
from pp2ex import Annotation

def test(amap):
    # Checking that we have annotations for all sequences in db
    f = open('initial/clean.fasta')
    for line in f:
        if line[0] == '>':
            uid = line[1:].strip()
            try:
                amap.getbyuniprotid(uid)
            except:
                print 'Uniprot ID: %s not found' % uid
    f.close()

def main(argv):
    if len(argv) < 2:
        print "Usage: %s <uniprot-id>" % argv[0]
        return

    target = argv[1]

    # Create annotation map
    annotfilename = 'initial/annotations.txt'
    idmappingfilename = 'initial/idmapping'
    amap = Annotation.AnnotationMap()
    amap.parse(annotfilename)
    amap.loadidmapping(idmappingfilename)
    
    # Create Full HPO map    
    hpofilename = 'initial/hp.obo'
    tree = Hpo.HpoTree()
    tree.construct(hpofilename)
    
    # Get target annotations
    annotations = amap.getbyuniprotid(target)
    
    print 'Annotations: %s' % annotations
    # Print all paths
    for a in annotations:
        print tree.extractpath(a)
    
    #test(amap)

if __name__ == "__main__":
    main(sys.argv)
