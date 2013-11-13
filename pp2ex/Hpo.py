class HpoTree:
    def __init__(self):
        self.root = None
        self.terms = dict()
    
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
                raise Exception('Term already exists: %s' % term.id)
            existingterm.name = term.name
            existingterm.parentid = term.parentid
            existingterm.extra = term.extra
            term = existingterm
        else:
            self.terms[term.id] = term

        if term.parentid is None:
            if self.root is None:
                self.root = term
            else:
                raise Exception('Term with no parent and we already have a root: %s' % term.id)
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

        self.obselete = False
        self.parent = None
        self.children = list()
    
    def __repr__(self):
        return '<%s : %s>' % (self.id, self.name)
