import sys
import csv

def main(argv):

    filename = argv[1] 
    out_cols = ['queryid', 'matchid', 'percentage', 'alignment-len', 'mistmatches', 'gap-openings', 'q.start', 'q.end', 's.start', 's.end', 'e-value', 'bit-score']
    
    result = dict()

    fileToRead = open(filename,'r')
    data = fileToRead.read()
    res = []
    for hit in data.splitlines():
        hit_data = dict()
        counter = 0
        for col in hit.split():
            hit_data[out_cols[counter]] = col
            if out_cols[counter]=='e-value':
                if col in result:
                    result[col] += 1
                else:
                    result[col] = 1

            counter += 1
        res.append(hit_data)

    w = csv.writer(open("output.csv", "w"))
    for key, val in result.items():
        w.writerow([key, val])
        
    

if __name__ == "__main__":
    main(sys.argv)