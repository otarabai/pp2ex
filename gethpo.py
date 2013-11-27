import sys
import cPickle as pickle
from pp2ex import Hpo
from pp2ex import Annotation

class HpoTreeCreator:
    """docstring for HpoTreeCreator"""
    def __init__(self, pathToHpObo='initial/hp.obo', pathToAnnotations='initial/annotations.txt', pathToIdMapping='initial/idmapping'):
        self.fullTree=None
        self.annotationMap=None
        self._loadTree(pathToAnnotations, pathToIdMapping, pathToHpObo)

    def _loadTree(self, pathToAnnotations, pathToIdMapping, pathToHpObo):
        try:
            treeFromFile = pickle.load(open("fullTree.p","rb"))
            annotationFromFile = pickle.load(open("annotationMap.p","rb"))
            self.fullTree = treeFromFile
            self.annotationMap = annotationFromFile
        except IOError:
            self._createAnnotationMap(pathToAnnotations, pathToIdMapping)
            self._createFullHpoMap(pathToHpObo)
            pickle.dump(self.fullTree, open("fullTree.p","wb"), pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.annotationMap, open("annotationMap.p","wb"), pickle.HIGHEST_PROTOCOL)
    
    def _createAnnotationMap(self, pathToAnnotations, pathToIdMapping):
        # Create annotation map
        annotfilename = pathToAnnotations
        idmappingfilename = pathToIdMapping
        self.annotationMap = Annotation.AnnotationMap()
        self.annotationMap.parse(annotfilename)
        self.annotationMap.loadidmapping(idmappingfilename)
    
    def _createFullHpoMap(self, pathToHpObo):
            # Create Full HPO map    
        hpofilename = pathToHpObo
        self.fullTree = Hpo.HpoTree()
        self.fullTree.construct(hpofilename)
        
    def constructTreeForUniprotId(self, uniprotId):
        target = uniprotId

        # Get target annotations
        annotations = self.annotationMap.getbyuniprotid(target)
        
        #print '\nAnnotations: %s\n\nPaths: ' % annotations
        # Merge and print all paths
        mergedTree = Hpo.HpoTree()
        for a in annotations:
            path = self.fullTree.extractpath(a)
            #print path
            mergedTree.addpath(path)
        
        #print '\nMerged Tree:'
        #print mergedTree
        return mergedTree
