import sys
from pp2ex import Hpo
from pp2ex import Annotation
from pp2ex import AnnotationTree

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
    fullTree = Hpo.HpoTree()
    fullTree.construct(hpofilename)
    
    # Get target annotations
    annotations = amap.getbyuniprotid(target)
    
    # Create Tree for paths
    #pathList = list()
    #for a in annotations:
    #    print tree.extractpath(a)
    #    pathList = pathList + tree.extractpath(a)
    
    #aTree = AnnotationTree.AnnotationTree()
    #aTree.createAnnotationTree(pathList)
    #aTree.printTree()
    #print 'Hello World'
    
    print '\nAnnotations: %s\n\nPaths:' % annotations
    # Merge and print all paths
    mergedTree = Hpo.HpoTree()
    for a in annotations:
        path = fullTree.extractpath(a)
        print path
        mergedTree.addpath(path)
    
    print '\nMerged Tree:'
    print mergedTree
    
    #test(amap)

if __name__ == "__main__":
    main(sys.argv)
