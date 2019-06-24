
# Preprocessing step

The input data to run 3D-DNA can be generated using Juicer, which is available at https://github.com/aidenlab/juicer

The script generate_restriction_sites_positions.py is used to generate the file sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa_DpnII.txt with the restriction sites. The arguments are the restriction enzyme and the assembly to scaffold.


```bash
python generate_restriction_sites_positions.py DpnII sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa
```

A second file needs to be created with the contigs name and length, here called chrom_sizes_c500.txt.

The pipeline Juicer is run with the following arguments:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-s : restriction enzyme<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-y : restriction sites file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-z : assembly to scaffold<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-p : contigs length file<br/>

To run the program, the Hi-C reads must be in a subfolder called fastq, with the two ends ending with _R1.fastq and _R2.fastq.


```bash
./juicer-master/CPU/juicer.sh -s DpnII \
    -y sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa_DpnII.txt \
    -z sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa \
    -p chrom_sizes_c500.txt \
    -D ./juicer-master/CPU
```

The output which will then be used for scaffolding is stored in the subfolder aligned and is called merged_nodups.txt.

# Scaffolding

The script run-asm-pipeline.sh is used for scaffolding. The arguments are the assembly to scaffold, then the merged_nodups.txt file. Parameters can be specified such as:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--mode : haploid/diploid (default=haploid)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--input : minimum input contig size (default=15000)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--round : number of rounds for misjoin correction (default=2)<br/>

For the simulations, the default parameters were used, except for --input which was set to 500.


```bash
run-asm-pipeline.sh -i 500 sim_c500/sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.fa aligned/merged_nodups.txt
```

The output scaffolds can be found in the file sim_c500_GCF_000002985.6_WBcel235_genomic.mixed.FINAL.fasta.
