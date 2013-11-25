import sys
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.ResultComparison import ComparisionResult
from pp2ex.ResultComparison import ResultFilterer
from gethpo import HpoTreeCreator 

def main(argv):
    if len(argv) < 4:
        print "Usage: %s <sequence> <hits> <number of cpus>" % argv[0]
        return

    # Blast
    b = Blast('blastdb/db.fasta')
    blastdata = b.run(argv[1], argv[2], argv[3])

    blastResultList = list()
    for b in blastdata:
        bResult = ComparisionResult(b['matchid'], b['percentage'], b['e-value'])

    # HHBlits
    h = Hhblits('/mnt/project/pp2_hhblits_db/pp2_hhm_db')
    hhblitsdata = h.run(argv[1], argv[2], argv[3])
    hhSearchResultList = list()
    for h in hhblitsdata:
        hhResult = ComparisionResult(h['matchid'], h['percentage'], h['e-value'], h['score'])

    # TODO: Take relevant results
    filterer = ResultFilterer(blastResultList, hhSearchResultList)
    filteredResults = filterer.filterTopResults()
    # TODO: "feed" gethpo with the results
    hpoCreator = HpoTreeCreator()
    hpoCreator.constructTreeForUniprotId('P01023') # for now: fixed test-entry
    # TODO: merge resulting trees of multiple gethpo-items

    # TOOD: Spit out resulting tree

if __name__ == "__main__":
    main(sys.argv)