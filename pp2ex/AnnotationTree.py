class AnnotationTree:
	"creation of annotation tree of given paths is done here"
	def __init__(self):
		self.paths = list() # empty list
		
	
	def createAnnotationTree(self, listOfPaths):
		self.paths = listOfPaths[::-1]
		for term in self.paths:
			
			if term.parent is None:
				print term
				

import Hpo		
class AnnotationNode(Hpo.HpoTerm):
	def __init__(self):
		self.children = dict() # empty dictionary
		self.frequency = 0
		
	def addChild(childNode):
		self.children = self.children+childNode
		
		
        
        