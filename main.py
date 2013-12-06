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

def cleanblastresults(results):
    matchids = list()
    for r in list(results):
        if r['matchid'] in matchids:
            results.remove(r)
        else:
            matchids.append(r['matchid'])
    return results

def main(argv):

    testseqscount = 1000 # Number of test sequences to use    
    randomseed = 1 # Set this to some value if you want to use the same test set more than once, or None if you want it random each time
    sequencesfile = 'initial/clean.fasta' # Used to get test sequences at random
    hitscount = 5
    outputfilename = 'scores.dat'

    # Initializations
    treecreator = HpoTreeCreator()
    blastalign = Blast('blastdb/db.fasta')
    combiner = HpoTreeCombiner()
    evaluator = Evaluator()
    
    # Find the number of sequences we have in the sequences file
    totalseqscount = sum(1 for line in open(sequencesfile)) / 2
    
    # Get sequences from file at random
    testseqs = list()
    random.seed(randomseed)
    for i in range(0, testseqscount):
        seqindex = random.randint(0, totalseqscount - 1)
        seqid = linecache.getline(sequencesfile, seqindex * 2 + 1).strip()
        seqid = seqid[1:]
        seqstring = linecache.getline(sequencesfile, seqindex * 2 + 2).strip()
        testseqs.append({'seqid' : seqid, 'seqstring' : seqstring})
    
    # Repeat operations for each test sequence
    nomatches = list()
    for inputseq in testseqs:
        # Query for blast results
        hits = blastalign.run(inputseq['seqstring'], hitscount + 1) # +1 because the sequence itself will be in the results
        hits = [h for h in hits if h['matchid'] != inputseq['seqid']] # Remove the sequence itself from results
        #hits = cleanblastresults(hits)
        if len(hits) == 0:
            nomatches.append(inputseq)
            continue
        
        # TODO: query for hhblits results and merge it with blast
        
        # Create annotation trees for all hits
        for hit in hits:
            hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
        
        #print '%s\n' % inputseq['seqid']
        # Use one of the merging methods to construct predicted tree with scores
        #prediction = combiner.combineNaive(hits)
        #prediction = combiner.combineBasedOnFrequency(hits)
        #prediction = combiner.combineBasedOnPercentage(hits)
        prediction = combiner.combineBasedOnScore(hits)
        #print prediction
        
        # Create the reference tree for scoring
        reference = treecreator.constructTreeForUniprotId(inputseq['seqid'])
        #print reference
        # Get evaluation results
        inputseq['scores'] = evaluator.getallscores(prediction, reference)
        #print inputseq['scores']
    
    for n in nomatches:
        testseqs.remove(n)
    
    # Do some analysis on the resulting scores
    avgfvalue = 0.0
    thresholds = dict()
    for t in evaluator.getthresholds():
        thresholds[t] = 0.0
    for inputseq in testseqs:
        maxfvalue = 0.0
        for s in inputseq['scores']:
            thresholds[s['threshold']] += s['fvalue']
            if s['fvalue'] > maxfvalue:
                maxfvalue = s['fvalue']
        avgfvalue += maxfvalue
    avgfvalue = avgfvalue / float(len(testseqs))
    print 'Average f-value: %f' % avgfvalue
    print 'Thresholds:'
    for k,v in sorted(thresholds.items()):
        print '%f: %f' % (k,v/float(len(testseqs)))
    
    # Calculate average precision and recall over all thresholds used
    #avgs = dict()
    #for inputseq in testseqs:
    #    for s in inputseq['scores']:
    #        if s['threshold'] not in avgs.keys():
    #            avgs[s['threshold']] = {'precision': 0.0, 'recall': 0.0}
    #        avgs[s['threshold']]['precision'] += s['precision']
    #        avgs[s['threshold']]['recall'] += s['recall']
    # Write results to file
    #f = open(outputfilename, 'w')
    #for t, a in sorted(avgs.items()):
    #    a['precision'] /= float(len(testseqs))
    #    a['recall'] /= float(len(testseqs))
    #    f.write('%f\t%f\n' % (a['recall'], a['precision']))


def test():
    evaluator = Evaluator()
    blastalign = Blast('blastdb/db.fasta')
    treecreator = HpoTreeCreator()
    combiner = HpoTreeCombiner()
    
    seqid = 'O15120'
    seqstring = 'MELWPCLAAALLLLLLLVQLSRAAEFYAKVALYCALCFTVSAVASLVCLLRHGGRTVENMSIIGWFVRSFKYFYGLRFEVRDPRRLQEARPCVIVSNHQSILDMMGLMEVLPERCVQIAKRELLFLGPVGLIMYLGGVFFINRQRSSTAMTVMADLGERMVRENLKVWIYPEGTRNDNGDLLPFKKGAFYLAVQAQVPIVPVVYSSFSSFYNTKKKFFTSGTVTVQVLEAIPTSGLTAADVPALVDTCHRAMRTTFLHISKTPQENGATAGSGVQPAQ'
    
    hits = blastalign.run(seqstring, 6)
    hits = [h for h in hits if h['matchid'] != seqid]
    hits = cleanblastresults(hits)

    reference = treecreator.constructTreeForUniprotId(seqid)

    for h in hits:
        h['tree'] = treecreator.constructTreeForUniprotId(h['matchid'])
        print h['tree']
        print '\n'
    
    prediction = combiner.combineBasedOnScore(hits)
    print '\n\nPrediction:\n\n'
    print prediction
    

if __name__ == "__main__":
    main(sys.argv)
    #test()
