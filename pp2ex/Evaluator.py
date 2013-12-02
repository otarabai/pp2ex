from Hpo import HpoTree

class Evaluator:
    def getthresholds(self):
        x = 0.0
        while x <= 1:
            yield x
            x += 0.1
    
    def applythreshold(self, tree, threshold):
        newTree = HpoTree()
        for term in tree.terms.itervalues():
            if term.score >= threshold:
                newTree.addterm(term.getcopy())
        return newTree

    def getfvalue(self, predicted, reference):
        matchs = 0.0
        
        for predictedTerm in predicted.terms.keys():
            if predictedTerm in reference.terms:
                matchs += 1
        
        if len(predicted.terms) == 0:
            precision = 1.0
        else:
            precision = matchs / len(predicted.terms)
        recall = matchs / len(reference.terms)
        fvalue = (2.0 * precision * recall) / (precision + recall)
        
        return fvalue
    
    def getallfvalues(self, predicted, reference):
        scores = list()
        for t in self.getthresholds():
            cuttree = self.applythreshold(predicted, t)
            fvalue = self.getfvalue(cuttree, reference)
            scores.append({'threshold' : t, 'fvalue' : fvalue})
        return scores
