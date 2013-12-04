import sys
import csv

def main(argv):

    filename = argv[1] 
    out_cols = ['queryid', 'matchid', 'percentage', 'e-value', 'bit-score']
    
    #result = dict()
    
    fileToRead = open(filename,'r')
    data = fileToRead.read()
    res = list()
    for hit in data.splitlines():
        hit_data = dict()
        counter = 0
        for col in hit.split():
            hit_data[out_cols[counter]] = col
            if out_cols[counter]=='e-value':
                #if col in result:
                #    result[col] += 1
                #else:
                #    result[col] = 1
	           res.append(float(col))
            counter += 1
        #res.append(hit_data)

    #w = csv.writer(open("hh_percentage_new.csv", "w"))
    w = open("hh_eValue_new.csv","w")
    #for key, val in result.items():
    #    w.writerow([key, val])
    for item in res:
        w.write("%s\n" % item)
    

if __name__ == "__main__":
    main(sys.argv)
