import sys
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.ResultComparison import ComparisonResult
from pp2ex.ResultComparison import ResultFilterer
from pp2ex.Hpo import HpoTree
from pp2ex.Hpo import HpoTreeCreator
from pp2ex.Hpo import HpoTreeCombiner
from pp2ex.Evaluator import Evaluator

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
        hit = {'matchid' : parts[1], 'percentage' : parts[2], 'e-value' : parts[3]}
        hitslist.append(hit)
        l = filehandle.readline()

def getnexttarget(filehandle):
    c = filehandle.read(1)
    seqid = None
    seq = ''
    while c:
        if c == '\n':
            c = filehandle.read(1)
            continue
        if c == '>':
            if seqid is not None:
                yield (seqid, seq)
                seq = ''
            seqid = filehandle.readline().split()[0]
        else:
            seq += c
        c = filehandle.read(1)
    if seqid is not None:
        yield (seqid, seq)

def main(argv):

    hitscount = 10
    inputfilename = 'target/sp_species.9606.all.noexp.tfa'
    outputfilename = 'target/results'

    # Initializations
    treecreator = HpoTreeCreator()
    blastalign = Blast('blastdb/db.fasta')
    combiner = HpoTreeCombiner()
    evaluator = Evaluator()

    # Read sequences from file
    iFile = open(inputfilename)
    oFile = open(outputfilename, 'a')
    counter = 1
    for seqid, seq in getnexttarget(iFile):
        print counter
        counter += 1
        # Get hits
        hits = blastalign.run(seq, hitscount)
    
        # Create annotation trees for all hits
        for hit in hits:
            hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
        
        # Create prediction
        prediction = combiner.combineBasedOnScore(hits)
        
        threshold = 0.3
        # Write leave terms of prediction to file (with threshold 0.3)
        for term in prediction.terms.itervalues():
            if len(term.children) > 0:
                continue
            if term.score < threshold:
                continue
            normalized = (term.score - threshold) / (1.0 - threshold)
            oFile.write('%s\t%s\t%.2f\n' % (seqid, term.id, normalized))
    iFile.close()
    oFile.close()
        

def test():
    filename = 'medians/hhResult_clean.csv'
    f = open(filename)
    counter = 0
    for seq, hits in gethhtarget(f):
        counter += 1
        #print 'Seq: %s' % seq
        #print 'Hits:\n %s' % hits
    print counter

if __name__ == "__main__":
    test()
    #main(sys.argv)
