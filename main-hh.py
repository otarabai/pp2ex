import sys
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.ResultComparison import ComparisonResult
from pp2ex.ResultComparison import ResultFilterer
from pp2ex.Hpo import HpoTree
from pp2ex.Hpo import HpoTreeCreator
from pp2ex.Hpo import HpoTreeCombiner
from pp2ex.Evaluator import Evaluator
import random
import linecache

def gethhtarget(filehandle):
    l = filehandle.readline()
    seqid = None
    hitslist = list()
    while l:
        parts = l.split()
        if parts[0] != seqid:
            if seqid is not None:
                yield (seqid, hitslist)
            seqid = parts[0]
            hitslist = list()
        hit = {'matchid' : parts[1], 'percentage' : parts[2], 'e-value' : parts[3], 'score' : parts[5]}
        hitslist.append(hit)
        l = filehandle.readline()
    yield (seqid, hitslist)

def main(argv):

    resultsfile = 'results/cleanFasta_hhResult.txt' # Used to get test sequences at random

    # Initializations
    treecreator = HpoTreeCreator()
    combiner = HpoTreeCombiner()
    evaluator = Evaluator()

    counter = 0
    fvalues = dict()
    for t in evaluator.getthresholds():
        fvalues[t] = 0.0
    
    # Repeat operations for each test sequence
    for seqid, hits in gethhtarget(open(resultsfile)):
        counter += 1
        
        hits = [h for h in hits if h['matchid'] != seqid] # Remove the sequence itself from results
        
        for hit in hits:
            hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
        
        # Use one of the merging methods to construct predicted tree with scores
        #prediction = combiner.combineNaive(hits)
        #prediction = combiner.combineBasedOnFrequency(hits)
        #prediction = combiner.combineBasedOnPercentage(hits)
        prediction = combiner.combineBasedOnScore(hits)
        
        # Create the reference tree for scoring
        reference = treecreator.constructTreeForUniprotId(seqid)

        # Get evaluation results
        scores = evaluator.getallscores(prediction, reference)
        for s in scores:
            fvalues[s['threshold']] += s['fvalue']
        
        if counter > 1000:
            break

    for t, f in sorted(fvalues.items()):
        print '%.1f\t%.4f' % (t, f / counter)

if __name__ == "__main__":
    main(sys.argv)
