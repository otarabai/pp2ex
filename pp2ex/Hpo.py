import sys
import cPickle as pickle
from Annotation import AnnotationMap
import math

class HpoTree:
    def __init__(self):
        self.root = None
        self.terms = dict()
    
    def __str__(self):
        if not self.root:
            raise Exception("Tree root not defined")
        return self.printterm(self.root, 0)
    
    def printterm(self, term, tabs):
        ret = '\t' * tabs + str(term) + '\n'
        for child in term.children:
            ret += self.printterm(child, tabs + 1)
        return ret
    
    def extractpath(self, termid):
        if termid not in self.terms:
            raise Exception('Term ID %s not found' % termid)
        term = self.terms[termid]
        if term.parent is None:
            return [term]
        else:
            return [term] + self.extractpath(term.parent.id)
    
    def construct(self, filename):
        f = open(filename)
        
        counter = 0
        obselete = 0
        for line in f:
            if line.strip() == '[Term]':
                newterm = self.parseterm(f)
                if newterm.obselete:
                    obselete += 1
                else:
                    self.addterm(newterm)
                    counter += 1
        f.close()
        
        # Validations on constructed tree
        if self.root is None:
            raise Exception('No root node found')
        if counter != len(self.terms):
            raise Exception('Parsed terms count does not match created terms count')
        for key, val in self.terms.items():
            if val.name is None:
                raise Exception('No definition found for %s' % key)
            if val.parent is None and val != self.root:
                raise Exception('No parent defined for %s' % key)
        
        print 'Parsed %d terms, ignored %d obselete terms' % (counter, obselete)
    
    def addterm(self, term):
        # validations on the new term
        if term.id is None:
            raise Exception('ID missing in term')
        if term.name is None:
            raise Exception('Name missing in term')

        # Add term to tree
        if term.id in self.terms: # Term already exists
            existingterm = self.terms[term.id]
            if existingterm.name is not None:
                existingterm.frequency += 1
                return
            existingterm.name = term.name
            existingterm.parentid = term.parentid
            existingterm.extra = term.extra
            term = existingterm
        else:
            self.terms[term.id] = term

        if term.parentid is None and self.root is None:
            self.root = term
        else:
            # Connect to parent
            if term.parentid in self.terms: # parent already in tree
                parent = self.terms[term.parentid]
            else: # if not, create it
                parent = HpoTerm()
                parent.id = term.parentid
                self.terms[parent.id] = parent
            term.parent = parent
            parent.children.append(term)
        
    def addpath(self, path):
        for term in path:
            self.addterm(term.getcopy()) # Use a copy to avoid taking the previous tree links too
    
    def addtree(self, tree):
        for term in tree.terms.itervalues():
            self.addterm(term.getcopy())
    
    def parseterm(self, fileObj):
        term = HpoTerm()

        for line in fileObj:
            if line.strip() == '': # End of HPO term
                break
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            
            if key == 'id':
                term.id = val
            elif key == 'name':
                term.name = val
            elif key == 'is_a':
                if term.parentid is None: # We are using only one parent
                    parentparts = val.split('!', 1)
                    term.parentid = parentparts[0].strip()
            elif key == 'is_obsolete' and val == 'true':
                term.obselete = True
            else:
                term.extra += line
        
        return term

class HpoTerm:
    def __init__(self):
        self.id = None
        self.name = None
        self.parentid = None
        self.extra = '' # Other information not important for us now

        self.frequency = 1
        self.score = 0.0
        self.obselete = False
        self.parent = None
        self.children = list()
    
    def getcopy(self):
        copy = HpoTerm()
        copy.id = self.id
        copy.name = self.name
        copy.parentid = self.parentid
        copy.extra = self.extra
        return copy
    
    def __repr__(self):
        return '<%s : %s, Score: %s>' % (self.id, self.name, self.score)

class HpoTreeCombiner:
    def normalizetermscores(self, tree):
        if tree.root is None:
            return tree
        
        maxscore = tree.root.score
        minscore = tree.root.score
        for term in tree.terms.itervalues():
            maxscore = max(maxscore, term.score)
            minscore = min(minscore, term.score)

        maxscore = float(maxscore)
        minscore = float(minscore)
        for term in tree.terms.itervalues():
            if maxscore == minscore:
                term.score = 1.0
            else:
                term.score = (float(term.score) - minscore) / (maxscore - minscore)
        
        return tree

    """ All functions in this class expect a parameter: list of dictionaries
        
        Each dictonary contains:
        'tree' => instance of HpoTree
        'matchid', 'e-value', 'percentage', 'score'
        
        Returns an instance of HpoTree (prediction)
    """

    def combineNaive(self, hits):
        """Sets all term scores to 1"""
        result = HpoTree()
        for hit in hits:
            for term in hit['tree'].terms.itervalues():
                newTerm = term.getcopy()
                newTerm.score = 1.0
                result.addterm(newTerm)
        return result

    def combineBasedOnFrequency(self, hits):
        result = self.combineNaive(hits)
        maxfreq = float(result.root.frequency)
        for term in result.terms.itervalues():
            term.score = float(term.frequency) / maxfreq
        return result

    def combineBasedOnScore(self, hits):
        result = HpoTree()
        
        if len(hits) == 0:
            return result
        
        for hit in hits:
            hitscore = float(hit['score'])
            for term in hit['tree'].terms.itervalues():
                if term.id in result.terms and result.terms[term.id].name is not None:
                    result.terms[term.id].score += hitscore
                else:
                    newTerm = term.getcopy()
                    result.addterm(newTerm)
                    result.terms[term.id].score += hitscore

        return self.normalizetermscores(result)

    def combineBasedOnPercentage(self, hits):
        result = HpoTree()
        
        if len(hits) == 0:
            return result
        
        for hit in hits:
            if float(hit['percentage']) == 100 or float(hit['e-value']) == 0:
                score = 1.0
            else:
                score = float(hit['percentage']) / 100.0
            
            for term in hit['tree'].terms.itervalues():
                if term.id in result.terms and result.terms[term.id].name is not None:
                    oldscore = result.terms[term.id].score
                    result.terms[term.id].score = oldscore + (1.0 - oldscore) * score
                else:
                    newTerm = term.getcopy()
                    newTerm.score = score
                    result.addterm(newTerm)
            
        return result


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
        self.annotationMap = AnnotationMap()
        self.annotationMap.parse(annotfilename)
        self.annotationMap.loadidmapping(idmappingfilename)
    
    def _createFullHpoMap(self, pathToHpObo):
            # Create Full HPO map    
        hpofilename = pathToHpObo
        self.fullTree = HpoTree()
        self.fullTree.construct(hpofilename)
    
    def constructTreeFromHpoIds(self, hpoids):
        mergedTree = HpoTree()
        for a in hpoids:
            path = self.fullTree.extractpath(a)
            #print path
            mergedTree.addpath(path)
        return mergedTree
    
    def constructTreeForUniprotId(self, uniprotId):
        # Get target annotations
        annotations = self.annotationMap.getbyuniprotid(uniprotId)
        
        #print '\nAnnotations: %s\n\nPaths: ' % annotations
        # Merge and print all paths
        mergedTree = HpoTree()
        for a in annotations:
            path = self.fullTree.extractpath(a)
            #print path
            mergedTree.addpath(path)
        
        #print '\nMerged Tree:'
        #print mergedTree
        return mergedTree
