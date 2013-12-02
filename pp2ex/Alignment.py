import subprocess
import tempfile
import multiprocessing

class Blast:
    def __init__(self, dbfilename, program = 'blastall'):
        self.program = program
        self.dbfilename = dbfilename
    
    def run(self, sequence, hits = 5):
        numberOfCpus = multiprocessing.cpu_count()
        if not numberOfCpus or numberOfCpus <= 0:
            numberOfCpus=1
    
        cmd = [
            self.program,
            '-p', 'blastp', # Program name
            '-d', self.dbfilename, # DB file name
            '-m', '8', # Output format
            '-b', str(hits), # Number of hits
            '-a', str(numberOfCpus)
            ]
        #print cmd
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate(input = '>TEST\n%s' % sequence)
        
        res = []
        for hit in out.splitlines():
            hit_data = dict()
            counter = 0
            cols = hit.split()
            hit_data['matchid'] = cols[1]
            hit_data['percentage'] = cols[2]
            hit_data['e-value'] = cols[10]
            hit_data['score'] = cols[11]
            res.append(hit_data)
        
        return res

class Hhblits:
    def __init__(self, dbfilename='/mnt/project/pp2_hhblits_db/pp2_hhm_db'):
        self.dbfilename = dbfilename
    
    def run(self, sequence, hits = 5):
        numberOfCpus = multiprocessing.cpu_count()
        if not numberOfCpus or numberOfCpus <= 0:
            numberOfCpus=1

        # Create temp file with input
        iFile = tempfile.NamedTemporaryFile(delete=False)
        iFile.write('>TEMP\n')
        iFile.write(sequence)
        iFile.close()
        
        oFile = tempfile.NamedTemporaryFile(delete=False)
        oFile.close()
        
        cmd = [
            'hhsearch',
            '-i', iFile.name,
            '-d', self.dbfilename,
            '-z', hits,
            '-o', oFile.name,
            '-cpu', str(numberOfCpus)
            ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p.communicate()
        o = open(oFile.name)
        out = o.read()
        
        res = []
        resultsStarted = False
        for hit in out.splitlines():
            hit_data = dict()
            parts = hit.split()
            if resultsStarted:
                if len(parts)<=0:
                    break
                else:
                    # parse input 
                    hit_data['matchid'] = parts[1]
                    hit_data['percentage'] = parts[2]
                    hit_data['e-value'] = parts[3]
                    hit_data['score'] = parts[4]
                    res.append(hit_data)
            elif len(parts)>0:
                if parts[0]=='No':
                    resultsStarted = True
                
        return res
