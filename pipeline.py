########################################################################################################################
# 2021-07-21
# Ewan Xiong
# RNA-seq snakemake pipeline 
########################################################################################################################

REP_INDEX = {"0211","3211"}
genome = "/mnt/l/pipeline/JFZ.genome.fasta"
gff = "/mnt/l/pipeline/JFZ.genome.gff"

rule all:
	input:
		expand('/mnt/l/pipeline/bam/{rep}_JFZ_mapping_sort.bam',rep=REP_INDEX),
		expand('/mnt/l/pipeline/cuffquant/{rep}/abundances.cxb',rep=REP_INDEX)

rule trimmomatic:
	input:
		"/mnt/l/pipeline/raw_fastq/{rep}.R1.fastq",
		"/mnt/l/pipeline/raw_fastq/{rep}.R2.fastq"
	output:
		"/mnt/l/pipeline/clean_fastq/{rep}_R1_clean.fastq",
		"/mnt/l/pipeline/clean_fastq/{rep}_R2_clean.fastq",
		"/mnt/l/pipeline/clean_fastq/{rep}_R1_unpaired.fastq",
		"/mnt/l/pipeline/clean_fastq/{rep}_R2_unpaired.fastq"
	log:
		"/mnt/l/pipeline/clean_fastq/{rep}_trimmomatic.log"
	shell:
		"trimmomatic \
		PE -threads 4 \
		ILLUMINACLIP:/mnt/l/pipeline/adapter.fa:2:30:10 \
		MINLEN:100 SLIDINGWINDOW:4:15 LEADING:20 AVGQUAL:20 \
		> {log} 2>&1"

rule hisat2_mapping:
	input:
		"/mnt/l/pipeline/clean_fastq/{rep}_R1_clean.fastq",
		"/mnt/l/pipeline/clean_fastq/{rep}_R2_clean.fastq",
	output:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping.sam"
	log:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping.log"
	shell:
		"hisat2 -x {genome}\
		-p 4 \
		-1 {input[0]} -2 {input[1]} -S {output} --dta-cufflinks > {log} 2>&1"

rule sam2bam_sort:
	input:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping.sam"
	output:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping_sort.bam"
	log:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping_sort.log"
	shell:
		"samtools sort -O BAM -o {output} -T {output}.temp -@ 4 -m 2G {input}"

rule cuffquant:
	input:
		"/mnt/l/pipeline/bam/{rep}_JFZ_mapping_sort.bam"
	output:
		"/mnt/l/pipeline/cuffquant/{rep}/abundances.cxb"
	shell:
		"cuffquant -p 4 \
		-b {genome} \
		-u {gff} \
		{input} \
		-o {output}"


