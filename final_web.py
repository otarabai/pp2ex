#!/usr/bin/python

import sys
import os
import argparse
from pp2ex.Alignment import Blast
from pp2ex.Alignment import Hhblits
from pp2ex.Hpo import HpoTree
from pp2ex.Hpo import HpoTreeCreator
from pp2ex.Hpo import HpoTreeCombiner

def init_parser():
    parser = argparse.ArgumentParser(description='Rostlab PP2 2013 Team6 protein predictor')
    parser.add_argument('-s', '--sequence', metavar='SEQUENCE-STRING',
        help="Predict protein sequence function")
    parser.add_argument('-n', '--hits', action='store_true',
        help="Return number of hits used")
    parser.add_argument('-p', '--others', action='store_true',
        help="Return sensitivity, precision and F-measure")
    return parser.parse_args()

def getdefaulTree(treecreator):
    # Top 73 termids
    termids = ['HP:0000001','HP:0000118','HP:0000005','HP:0000707','HP:0002011','HP:0000007','HP:0000152','HP:0011446','HP:0000234','HP:0000478','HP:0100543','HP:0000271','HP:0001939','HP:0001438','HP:0000924','HP:0011842','HP:0000006','HP:0001574','HP:0001507','HP:0003011','HP:0000119','HP:0000598','HP:0011804','HP:0001626','HP:0000951','HP:0002012','HP:0000153','HP:0000004','HP:0007319','HP:0000929','HP:0011844','HP:0002813','HP:0011354','HP:0002086','HP:0001250','HP:0011442','HP:0000163','HP:0000366','HP:0000078','HP:0012252','HP:0000364','HP:0000365','HP:0000079','HP:0001871','HP:0001627','HP:0009121','HP:0002564','HP:0012243','HP:0000284','HP:0000002','HP:0001249','HP:0003808','HP:0001252','HP:0003674','HP:0004323','HP:0002814','HP:0004329','HP:0007256','HP:0002817','HP:0001098','HP:0011007','HP:0001263','HP:0004322','HP:0000240','HP:0000496','HP:0001155','HP:0001392','HP:0011121','HP:0000925','HP:0100022','HP:0011458','HP:0002088','HP:0004328']
    tree = treecreator.constructTreeFromHpoIds(termids)
    for term in tree.terms.itervalues():
        term.score = 0.5
    return tree
    
def main(argv):

    hitscount = 7
    threshold = 0.2

    args = vars(init_parser())

    if args['hits']:
        print hitscount
    elif args['others']:
        print '%.1f %.4f %.4f' % (threshold, 0.0, 0.2842)
    elif args['sequence']:
        sequence = args['sequence']
        # Initializations
        local_path = os.path.dirname(__file__)
        ont_path = os.path.join(local_path, 'initial/hp.obo')
        annot_path = os.path.join(local_path, 'initial/annotations.txt')
        map_path = os.path.join(local_path, 'initial/idmapping')
        db_path = os.path.join(local_path, 'blastdb/db.fasta')
        
        treecreator = HpoTreeCreator(ont_path, annot_path, map_path)
        blastalign = Blast(db_path)
        combiner = HpoTreeCombiner()

        result = ''
        
        hits = blastalign.run(sequence, hitscount)
        
        if len(hits) == 0:
           prediction = getdefaulTree(treecreator)
        else:
           for hit in hits:
               hit['tree'] = treecreator.constructTreeForUniprotId(hit['matchid'])
           prediction = combiner.combineBasedOnScore(hits)
            
        for term in prediction.terms.itervalues():
            if len(term.children) > 0:
                continue
            if term.score < threshold:
                continue
            row = ('%s\t%.2f\n' % (term.id, term.score))
            result+=row
                
        result+='END'
        print result
        sys.exit(0)
    else:
        print 'no option selected'
        
if __name__ == "__main__":
    main(sys.argv)
