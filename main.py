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

def getdefaulTree(treecreator):
    # Top 73 termids
    termids = ['HP:0000001','HP:0000118','HP:0000005','HP:0000707','HP:0002011','HP:0000007','HP:0000152','HP:0011446','HP:0000234','HP:0000478','HP:0100543','HP:0000271','HP:0001939','HP:0001438','HP:0000924','HP:0011842','HP:0000006','HP:0001574','HP:0001507','HP:0003011','HP:0000119','HP:0000598','HP:0011804','HP:0001626','HP:0000951','HP:0002012','HP:0000153','HP:0000004','HP:0007319','HP:0000929','HP:0011844','HP:0002813','HP:0011354','HP:0002086','HP:0001250','HP:0011442','HP:0000163','HP:0000366','HP:0000078','HP:0012252','HP:0000364','HP:0000365','HP:0000079','HP:0001871','HP:0001627','HP:0009121','HP:0002564','HP:0012243','HP:0000284','HP:0000002','HP:0001249','HP:0003808','HP:0001252','HP:0003674','HP:0004323','HP:0002814','HP:0004329','HP:0007256','HP:0002817','HP:0001098','HP:0011007','HP:0001263','HP:0004322','HP:0000240','HP:0000496','HP:0001155','HP:0001392','HP:0011121','HP:0000925','HP:0100022','HP:0011458','HP:0002088','HP:0004328']
    tree = treecreator.constructTreeFromHpoIds(termids)
    for term in tree.terms.itervalues():
        term.score = 0.5
    return tree
    

def getnexttestseq(filehandle):
    seqid = filehandle.readline()
    while seqid:
        seqid = seqid[1:].strip()
        seq = filehandle.readline().strip()
        yield (seqid, seq)
        seqid = filehandle.readline()

def cleanblastresults(results): # Remove duplications in blast results
    matchids = list()
    for r in list(results):
        if r['matchid'] in matchids:
            results.remove(r)
        else:
            matchids.append(r['matchid'])
    return results

def main(argv):

    sequencesfile = 'initial/clean.fasta'
    hitscount = 7

    # Initializations
    treecreator = HpoTreeCreator()
    blastalign = Blast('blastdb/db.fasta')
    combiner = HpoTreeCombiner()
    evaluator = Evaluator()

    counter = 0
    fvalues = dict()
    precision = dict()
    recall = dict()
    for t in evaluator.getthresholds():
        fvalues[t] = 0.0
        precision[t] = 0.0
        recall[t] = 0.0
    
    # Repeat operations for each test sequence
    for seqid, seqstring in getnexttestseq(open(sequencesfile)):
        counter += 1
        
        # Query for blast results
        hits = blastalign.run(seqstring, hitscount + 1) # +1 because the sequence itself will be in the results
        hits = [h for h in hits if h['matchid'] != seqid] # Remove the sequence itself from results
        
        hits = cleanblastresults(hits)
        
        if len(hits) == 0:
            prediction = HpoTree()#getdefaulTree(treecreator)
        else:
            for hit in hits:
                hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
            
            # Use one of the merging methods to construct predicted tree with scores
            prediction = combiner.combineNaive(hits)
            #prediction = combiner.combineBasedOnFrequency(hits)
            #prediction = combiner.combineBasedOnPercentage(hits)
            #prediction = combiner.combineBasedOnScore(hits)
        
        # Create the reference tree for scoring
        reference = treecreator.constructTreeForUniprotId(seqid)

        # Get evaluation results
        scores = evaluator.getallscores(prediction, reference)
        for s in scores:
            fvalues[s['threshold']] += s['fvalue']
            precision[s['threshold']] += s['precision']
            recall[s['threshold']] += s['recall']

    print 'F-values:\n'
    for t, f in sorted(fvalues.items()):
        print '%.1f\t%.4f' % (t, f / counter)
    
    print '\nPrecisions:\n'
    
    for t, f in sorted(precision.items()):
        print '%.1f\t%.4f' % (t, f / counter)
        
    print '\nRecalls:\n'
    
    for t, f in sorted(recall.items()):
        print '%.1f\t%.4f' % (t, f / counter)

if __name__ == "__main__":
    main(sys.argv)
