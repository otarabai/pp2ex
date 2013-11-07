import subprocess
import tempfile

class Hhblits:
    def __init__(self, dbfilename):
        self.dbfilename = dbfilename
    
    def run(self, sequence, hits = 5):
        """cmd = [
            self.program,
            '-p',
            'blastp',
            '-d',
            self.dbfilename,
            '-m',
            '8',
            '-b',
            str(hits),
            ]"""
        # Create temp file with input
        iFile = tempfile.NamedTemporaryFile(delete=False)
        iFile.write('>TEMP')
        iFile.write(sequence)
        iFile.close()
        
        oFile = tempfile.NamedTemporaryFile(delete=False)
        oFile.close()
        
        cmd = [
            'hhblits',
            '-i', iFile.name,
            '-d', self.dbfilename,
            '-z', hits,
            '-o', oFile.name
            ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        p.communicate()
        o = open(oFile.name)
        out = o.read()
        
        res = []
        for hit in out.splitlines():
            hit_data = dict()
            parts = hit.split()
            hit_data['matchid'] = parts[1]
            hit_data['percentage'] = parts[2]
            hit_data['e-value'] = parts[3]
            res.append(hit_data)
        
        return res
