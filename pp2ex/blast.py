import subprocess

class Blast:
    def __init__(self, dbfilename, program = 'blastall'):
        self.program = program
        self.dbfilename = dbfilename
        self.out_cols = ['queryid', 'matchid', 'percentage', 'alignment-len', 'mistmatches', 'gap-openings', 'q.start', 'q.end', 's.start', 's.end', 'e-value', 'bit-score']
    
    def run(self, sequence, hits = 5):
        cmd = [
            self.program,
            '-p', 'blastp',
            '-d', self.dbfilename,
            '-m', '8',
            '-b', str(hits),
            ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate(input = '>TEST\n%s' % sequence)
        
        res = []
        for hit in out.splitlines():
            hit_data = dict()
            counter = 0
            for col in hit.split():
                hit_data[self.out_cols[counter]] = col
                counter += 1
            res.append(hit_data)
        
        return res
