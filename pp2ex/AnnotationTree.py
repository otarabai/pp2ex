class AnnotationTree:
	"creation of annotation tree of given paths is done here"
	def __init__(self):
		self.paths = list() # empty list
		self.tree = None # using AnnotationNode as root of tree
		self.lastParent = AnnotationNode()		
	
	def createAnnotationTree(self, listOfPaths):
		self.paths = listOfPaths[::-1]
		for term in self.paths:
			# use AnnotationNode.children to add new children
			# HPO-ID is ought to be used as key of dictionary
			# this way we should easily be able to add children
			# without big checking of duplicates?!
			if term.parent is None: # we found a root-node. restart?
				if self.tree is None:
					rootNode = AnnotationNode()
					rootNode.id=term.id
					self.tree = rootNode
					print term
				else:
					self.tree.frequency+=1
				self.lastParent = self.tree
			else:
				if term.id in self.lastParent.children:
					self.lastParent.children[term.id].frequency+=1
				else:	
					childNode = AnnotationNode()
					childNode.id=term.id
					childNode.parent = self.lastParent
					#self.lastParent.children[childNode.id]=childNode
				self.lastParent=term
				
	def printTree(self):
		print self.tree
		self._printChildren(self.tree)
		
		
	def _printChildren(self, parentNode):
		if parentNode.children is None:
			pass
		else:
			for child in parentNode.children:
				print child
				self._printChildren(child)

import Hpo		
class AnnotationNode():
	def __init__(self):
		self.id = None
		self.children = dict() # empty dictionary
		self.frequency = 1
		self.parent = None
		
	def addChild(childNode):
		self.children = self.children+childNode
		
		
        
        