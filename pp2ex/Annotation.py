class AnnotationMap:
    def __init__(self):
        self.geneidmap = None
        self.uniprotidmap = None
    
    def parse(self, filename):
        self.geneidmap = dict()
        f = open(filename)
        for line in f:
            if line[0] == '#': #comment
                continue
            parts = line.split()
            geneid = parts[0].strip()
            annotation = parts[-1].strip()
            if geneid not in self.geneidmap:
                self.geneidmap[geneid] = list()
            self.geneidmap[geneid].append(annotation)
        f.close()
    
    def loadidmapping(self, filename):
        self.uniprotidmap = dict()
        f = open(filename)
        for line in f:
            parts = line.split()
            geneid = parts[0].strip()
            uniprotid = parts[1].strip()
            self.uniprotidmap[uniprotid] = self.geneidmap[geneid]
    
    def writegeneids(self, filename):
        f = open(filename, 'w+')
        for geneid in self.geneidmap:
            f.write('%s\n' % geneid)
        f.close()
    
    def getbyuniprotid(self, uniprotid):
        if self.uniprotidmap is None:
            raise Exception('Uniprot map not created')
        if uniprotid not in self.uniprotidmap:
            raise Exception('Uniprot ID does not exist: %s' % uniprotid)
        return self.uniprotidmap[uniprotid]
