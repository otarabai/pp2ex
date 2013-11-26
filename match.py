import sys
import multiprocessing
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.ResultComparison import ComparisonResult
from pp2ex.ResultComparison import ResultFilterer
from gethpo import HpoTreeCreator 

def main(argv):
    if len(argv) < 3:
        print "Usage: %s <sequence> <hits>" % argv[0]
        return

    numberOfCpus = multiprocessing.cpu_count()
    if not numberOfCpus or numberOfCpus <= 0:
        numberOfCpus=1

    numberOfCpus=str(numberOfCpus)

    # Blast
    b = Blast('blastdb/db.fasta')
    blastdata = b.run(argv[1], numberOfCpus, argv[2])
    print blastdata
    blastResultList = list()
    for b in blastdata:
        bResult = ComparisonResult(b['matchid'], b['percentage'], b['e-value'])
        blastResultList.append(bResult)

    # HHBlits
    h = Hhblits('/mnt/project/pp2_hhblits_db/pp2_hhm_db')
    hhblitsdata = h.run(argv[1], numberOfCpus, argv[2])
    hhSearchResultList = list()
    for h in hhblitsdata:
        hhResult = ComparisonResult(h['matchid'], h['percentage'], h['e-value'], h['score'])
        hhSearchResultList.append(hhResult)

    # Take relevant results
    filterer = ResultFilterer(blastResultList, hhSearchResultList)
    filteredResults = filterer.filterTopResults()
    # "feed" gethpo with the results
    hpoCreator = HpoTreeCreator() # build base-tree only once
    for uniprotId in filteredResults:
        hpoCreator.constructTreeForUniprotId(uniprotId)
    # TODO: merge resulting trees of multiple gethpo-items

    # TOOD: Spit out resulting tree

if __name__ == "__main__":
    main(sys.argv)
