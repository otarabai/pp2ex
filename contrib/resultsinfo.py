filename = '../results/cleanFasta_hhResult.txt'

counts = dict()
targetcount = 0
curtarget = ''
hitcount = 0

for line in open(filename):
    parts = line.split()
    if parts[0] == curtarget:
        hitcount += 1
    else:
        if curtarget != '':
            if hitcount in counts:
                counts[hitcount] += 1
            else:
                counts[hitcount] = 1
        targetcount += 1
        hitcount = 1
        curtarget = parts[0]

print 'Total sequences: %d\n' % targetcount
for key, value in sorted(counts.items()):
    print '%d : %d' % (key, value)
