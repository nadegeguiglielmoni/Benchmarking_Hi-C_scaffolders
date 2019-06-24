
# Preprocessing

The input data to run SALSA2 is generated with the mapping pipeline available at https://github.com/ArimaGenomics 

## Mapping


```bash
bwa index sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa
bwa mem -B 8 sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa end1.fastq | samtools view -bS > salsa_scaffolding.end1.bam
bwa mem -B 8 sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa end2.fastq | samtools view -bS > salsa_scaffolding.end2.bam
```

## Filtering 5'


```bash
samtools view -h salsa_scaffolding.end1.bam | perl filter_five_end.pl | samtools view -bS > salsa_scaffolding.filtered.end1.bam
samtools view -h salsa_scaffolding.end2.bam | perl filter_five_end.pl | samtools view -bS > salsa_scaffolding.filtered.end2.bam
```

## Combine and filter on mapping quality


```bash
perl two_read_bam_combiner.pl salsa_scaffolding.filtered.end1.bam salsa_scaffolding.filtered.end2.bam samtools 10 | samtools view -bS -t sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa | samtools sort -o salsa_scaffolding.end.bam
```

## Add read group


```bash
java -Xmx2g -jar picard.jar AddOrReplaceReadGroups \
            INPUT=salsa_scaffolding.end.bam \
            OUTPUT=salsa_scaffolding.processed.bam \
            ID=salsa_scaffolding LB=salsa_scaffolding \
            SM="overall_exp_name" PL=ILLUMINA PU=none
```

## Preparing inputs for SALSA2


```bash
bamToBed -i salsa_scaffolding.processed.bam > salsa_scaffolding.alignment.bed
sort -k 4 salsa_scaffolding.alignment.bed > tmp && mv tmp salsa_scaffolding.alignment.bed

samtools faidx sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa
```

# Scaffolding

The program can be found at https://github.com/machinegun/SALSA

It can be run with the script run_pipeline.py. The parameters used in this work are:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-a : path to the draft assembly
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-l : path to file generated with samtools faidx, containing the contigs length
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-b : processed Hi-C reads
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-c : minimum contig length, here set to 0
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-e : restriction enzyme
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-i : number of iterations to perform
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-m : yes to correct misassemblies

SALSA2 was run both with and without misassemblies correction. The number of iteration is set to the high value of 30, but the program never reached 30 iterations because it stops automatically when all information brought by Hi-C data is exhausted.


```bash
#with misassemblies correction
python SALSA/run_pipeline.py -a sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa \
    -l sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa.fai \
    -b salsa_scaffolding.alignment.bed -o scaffolds_yescorrect \
    -c 0 -e GATC -i 30 -m yes 

#without misassemblies correction
python SALSA/run_pipeline.py -a sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa \
    -l sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa.fai \
    -b salsa_scaffolding.alignment.bed -o scaffolds_yescorrect \
    -c 0 -e GATC -i 30 -m no
```
