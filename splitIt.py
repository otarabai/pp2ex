import os
import sys
import random
import subprocess
from pp2ex.Alignment import Blast
from pp2ex.Hpo import HpoTree
from pp2ex.Hpo import HpoTreeCreator
from pp2ex.Hpo import HpoTreeCombiner
from pp2ex.Evaluator import Evaluator

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

def evaluate(dbfile, targetsfile):
    # Initializations
    treecreator = HpoTreeCreator()
    blastalign = Blast(dbfile)
    combiner = HpoTreeCombiner()
    evaluator = Evaluator()
    hitscount = 7
    threshold = 0.2
    
    fvalues = 0.0
    counter = 0.0
    for seqid, seqstring in getnexttestseq(open(targetsfile)):
        counter += 1.0
        # Query for blast results
        hits = blastalign.run(seqstring, hitscount)
        hits = cleanblastresults(hits)
        
        if len(hits) == 0:
            prediction = getdefaulTree(treecreator)
        else:
            for hit in hits:
                hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
            
            # Use one of the merging methods to construct predicted tree with scores
            prediction = combiner.combineBasedOnScore(hits)
        
        # Create the reference tree for scoring
        reference = treecreator.constructTreeForUniprotId(seqid)

        # Apply threshold
        prediction = evaluator.applythreshold(prediction, threshold)

        # Get evaluation results
        scores = evaluator.getscores(prediction, reference)
        fvalues += scores['fvalue']
    
    return (fvalues / counter)


def main(argv):
    if len(sys.argv) < 2:
        print 'Usage: %s <input-file>' % sys.argv[0]
        sys.exit(0)

    fi = open(sys.argv[1])

    proteinDict = dict()
    currentProteinId = ''

    # read the source-file
    for line in fi:
        if line[0] == '>':
        	currentProteinId=line
        	proteinDict[currentProteinId]=''
        else:
        	proteinDict[currentProteinId]+=line
    fi.close()

    numberOfFolds=10
    maxNumberOfProteinsPerIndex = (len(proteinDict))/10
    evaluationIndex = {1:True,2:True,3:True,4:True,5:True,6:True,7:True,8:True,9:True,10:True}
    counter = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0} # not used atm

    # create dictionary of keys of proteins for the folds
    listOfFolds=dict()
    while (numberOfFolds>0):
	    listOfFolds[numberOfFolds]=list()
	    numberOfFolds-=1

    # create folds:
    for key in proteinDict.keys():
	    index = random.randint(1,10)
	    while len(listOfFolds[index]) == maxNumberOfProteinsPerIndex + 1:
	        index = random.randint(1,10)
	    counter[index]+=1
	    listOfFolds[index].append(key)

    totalfmax = 0.0
    # create fastaFile from source-folds
    for indexKey in evaluationIndex:
	    # initializing new iteration
	    sourceFolds = list()
	    sourceFile = open('kfold/train.fasta','w')
	    sourceFile.close()

	    evaluationFile = open('kfold/eval.fasta','w')
	    evaluationFile.close()
	    # end initization

	    # get source-data from all 10 folds
	    for foldIndex in listOfFolds.keys():
		    if(foldIndex != indexKey):
			    for i in listOfFolds[foldIndex]:
				    sourceFolds.append(i)

	    sourceFile = open('kfold/train.fasta','a')
	    for protein in sourceFolds:
			    text = protein
			    text+=proteinDict[protein]
			    sourceFile.write(text)
	    sourceFile.close()
	    # source-data for database created
	    # create blast-DB
	    os.remove('kfold/train.fasta.phr')
	    os.remove('kfold/train.fasta.pin')
	    os.remove('kfold/train.fasta.psq')
	    cmd = 'formatdb -i kfold/train.fasta -p T'
	    cmd = cmd.split()
	    p = subprocess.Popen(cmd)

	    # create evaluation File
	    evaluationFile = open('kfold/eval.fasta','a')
	    evalFold = list()
	    for proteinKey in listOfFolds[indexKey]:
		    evalFold.append(proteinKey)

	    for protein in evalFold:
		    text = protein
		    text+=proteinDict[protein]
		    evaluationFile.write(text)

	    evaluationFile.close()
	    #evaluation File created
	    
	    fmax = evaluate('kfold/train.fasta', 'kfold/eval.fasta')
	    print 'Fmax: %f' % fmax
	    totalfmax += fmax
    
    avgfmax = totalfmax / 10.0
    return avgfmax


if __name__ == "__main__":
    totalfmax = 0.0
    for i in range(1, 11):
        fmax = main(sys.argv)
        print 'Trial %d: %f' % (i, fmax)
        totalfmax += fmax
    print 'All trials average: %f' % (totalfmax / 10)
