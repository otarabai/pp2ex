from pp2ex.Hpo import HpoTreeCreator

def getnexttestseq(filehandle):
    seqid = filehandle.readline()
    while seqid:
        seqid = seqid[1:].strip()
        seq = filehandle.readline().strip()
        yield (seqid, seq)
        seqid = filehandle.readline()

def main2():
    sequencesfile = 'initial/clean.fasta'
    
    treecreator = HpoTreeCreator()

    termscount = 0
    seqcount = 0
    for seqid, seq in getnexttestseq(open(sequencesfile)):
        tree = treecreator.constructTreeForUniprotId(seqid)
        seqcount += 1
        termscount += len(tree.terms)
    
    print 'Average terms: %f' % (float(termscount) / float(seqcount))


def main():
    sequencesfile = 'initial/clean.fasta'
    
    treecreator = HpoTreeCreator()
    terms = dict()

    for seqid, seq in getnexttestseq(open(sequencesfile)):
        tree = treecreator.constructTreeForUniprotId(seqid)
        for term in tree.terms.keys():
            if term in terms:
                terms[term] += 1
            else:
                terms[term] = 1

    getTop = 73
    counter = 1
    for term in sorted(terms, key=terms.get, reverse=True):
        print '%s' % term
        counter += 1
        if counter > getTop:
            break

if __name__ == "__main__":
    main()
