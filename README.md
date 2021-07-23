############################################################### 
##########             RNA-seq-pipelines           ############
###############################################################

### snakemake pipeline workflow
1. conda activate/create env with python = 3*
2. conda install trimmomatic,hisat2,samtools,cufflinks 
3. prepare working directory 
4. move raw data into working directory
5. snakemake pipeline start to check workflow logic 
6. plot workflow_dag.pdf 

### snakemake pipeline start

snakemake -s pipeline.py -n -p

-n not start for reall, just test workflow logic

-p show workflow details

### plot workflow dag_plot 

1.snakemake -s pipeline.py --dag

2.snakemake -s pipeline.py --dag | dot -Tpdf > pipeline_dag.pdf







