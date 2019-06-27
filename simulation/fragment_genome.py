import Bio
from Bio import SeqIO
import random as rand
import argparse

def parse_args():
	""" Gets the arguments from the command line."""
	parser = argparse.ArgumentParser()
	parser.add_argument('infile',
				help="""Input genome.""")
	parser.add_argument('-c', '--cut', type=int, default=500,
				help="""Number of cuts to make.""")
	parser.add_argument('-o', '--out', default='sim.fa',
				help="""Output path.""")
	return parser.parse_args()

args = parse_args()

filename = args.infile
outfile = args.out
numCut = args.cut

seqData = {}
indexData = {}
i = 0

record = SeqIO.parse(filename, "fasta")

#store the original sequences in a library
for sequence in record :
	seqData[sequence.id] = sequence.seq

#create an index for all the positions of the genome
for sequence in seqData.keys() :
	for pos in range(0, len(seqData[sequence])) :
		indexData[i] = [sequence, pos]
		i+=1

#random sampling of cutting sites among all the positions of the genome		
cutSites = rand.sample(indexData.keys(), numCut)

#create a new library for the cut sequences
seqCut = {}
for seq_id in seqData.keys() :
	seqCut[seq_id] = []
	                                             
for site in cutSites :
	seqCut[indexData[site][0]].append(indexData[site][1])

outdoc = open(outfile, "w")

for seq_id in seqCut.keys() :
	seqCut[seq_id] = sorted(seqCut[seq_id])
	st_pos = 0
	i = 1
	
	if len(seqCut[seq_id]) == 0 :
		outdoc.write(">{0}_1\n{1}\n".format(seq_id, seqData[seq_id]))
	else :
		for site in range(0, len(seqCut[seq_id]) ) :
			outdoc.write(">{0}_{1}\n{2}\n".format(seq_id, site , seqData[seq_id][st_pos:seqCut[seq_id][site]]))
			st_pos = seqCut[seq_id][site]
		outdoc.write(">{0}_{1}\n{2}\n".format(seq_id, len(seqCut[seq_id]) , seqData[seq_id][st_pos:len(seqData[seq_id])]))
	
outdoc.close()

sortedData = {}

record = SeqIO.parse(outfile, "fasta")

for sequence in record :
	sortedData[sequence.id] = sequence.seq
	
unsortList = list(sortedData.keys())
rand.shuffle(unsortList)
print(len(sortedData.keys()))
print(len(unsortList))

outdoc = open(outfile + "mixed", "w")
for frag in unsortList :
	print(frag)
	print(len(sortedData[frag]))
	outdoc.write(">{0}\n{1}\n".format(frag, sortedData[frag]))

outdoc.close()
