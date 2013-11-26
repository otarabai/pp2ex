import sys
import multiprocessing
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.ResultComparison import ComparisonResult
from pp2ex.ResultComparison import ResultFilterer
from pp2ex.Hpo import HpoTreeCombiner
from gethpo import HpoTreeCreator 

def main(argv):
    if len(argv) < 4:
        print "Usage: %s <uniprot-id> <sequence> <hits>" % argv[0]
        return

    uniprotid = argv[1]
    sequence = argv[2]
    hits = argv[3]

    numberOfCpus = multiprocessing.cpu_count()
    if not numberOfCpus or numberOfCpus <= 0:
        numberOfCpus=1
    numberOfCpus=str(numberOfCpus)

    # Blast
    b = Blast('blastdb/db.fasta')
    blastdata = b.run(sequence, numberOfCpus, hits)
    blastResultList = list()
    for b in blastdata:
        if b['matchid'] == uniprotid:
            print 'Sequence itself found in blast results, removed'
            continue
        bResult = ComparisonResult(b['matchid'], b['percentage'], b['e-value'])
        blastResultList.append(bResult)

    # HHBlits
    #h = Hhblits('/mnt/project/pp2_hhblits_db/pp2_hhm_db')
    #hhblitsdata = h.run(sequence, numberOfCpus, hits)
    #hhSearchResultList = list()
    #for h in hhblitsdata:
    #    if h['matchid'] == uniprotid:
    #        print 'Sequence itself found in hhblits results, removed'
    #        continue
    #    hhResult = ComparisonResult(h['matchid'], h['percentage'], h['e-value'], h['score'])
    #    hhSearchResultList.append(hhResult)

    # "feed" gethpo with the results
    hpoCreator = HpoTreeCreator() # build base-tree only once
    
    # This part is where we use blast or hhblits or combination of both to get the top N matches
    # For testing purposes, we will use the blast results now as it is
    blastTrees = list()
    for match in blastResultList:
        blastTrees.append({'tree': hpoCreator.constructTreeForUniprotId(match.uniprotId), 'match': match})
    
    # Now we combine the trees using one of the methods in HpoTreeCombiner
    combiner = HpoTreeCombiner()
    prediction = combiner.combineNaive(blastTrees)
    
    print "Predicted tree"
    print prediction
    
    # Validation phase (this is only when we are using a sequence we already have annotations for)
    (precision, recall) = combiner.compareTrees(hpoCreator.constructTreeForUniprotId(uniprotid), prediction)
    print "Precision: %f" % precision
    print "Recall: %f" % recall
    

if __name__ == "__main__":
    main(sys.argv)
