import sys
from pp2ex import Hpo
from pp2ex import Annotation
from pp2ex import AnnotationTree

#def test(amap):
    # Checking that we have annotations for all sequences in db
#    f = open('initial/clean.fasta')
 #   for line in f:
 #       if line[0] == '>':
 #           uid = line[1:].strip()
 #           try:
 #               amap.getbyuniprotid(uid)
 #           except:
 #               print 'Uniprot ID: %s not found' % uid
 #   f.close()
class HpoTreeCreator:
    """docstring for HpoTreeCreator"""
    def __init__(self, pathToHpObo='initial/hp.obo', pathToAnnotations='initial/annotations.txt', pathToIdMapping='initial/idmapping'):
        self.fullTree=None
        self.annotationMap=None
        self._createAnnotationMap(pathToAnnotations, pathToIdMapping)
        self._createFullHpoMap(pathToHpObo)
    
    def _createAnnotationMap(pathToAnnotations, pathToIdMapping):
        # Create annotation map
        annotfilename = pathToAnnotations
        idmappingfilename = pathToIdMapping
        self.annotationMap = Annotation.AnnotationMap()
        self.annotationMap.parse(annotfilename)
        self.annotationMap.loadidmapping(idmappingfilename)
    
    def _createFullHpoMap(pathToHpObo):
            # Create Full HPO map    
        hpofilename = pathToHpObo
        self.fullTree = Hpo.HpoTree()
        self.fullTree.construct(hpofilename)
        
    def constructTreeForUniprotId(uniprotId):
        target = uniprotId

        # Get target annotations
        annotations = self.annotationMap.getbyuniprotid(target)
        
        print '\nAnnotations: %s\n\nPaths: ' % annotations
        # Merge and print all paths
        mergedTree = Hpo.HpoTree()
        for a in annotations:
            path = self.fullTree.extractpath(a)
            print path
            mergedTree.addpath(path)
        
        print '\nMerged Tree:'
        print mergedTree
