import sys
import subprocess
import os
import argparse

docker_name="rna:latest"

parse=argparse.ArgumentParser("This script will analysis RNA fusion.")
parse.add_argument("-p1","--pe1",help="R1 fastq",required=True)
parse.add_argument("-p2","--pe2",help="R2 fastq",required=True)
parse.add_argument("-r","--ref",help="reference data directory",required=True)
parse.add_argument("-p","--prefix",help="prefix of output",required=True)
parse.add_argument("-o","--outdir",help="output directory",required=True)
args=parse.parse_args()
###############################
if not os.path.exists(args.outdir):
    subprocess.check_call('mkdir -p %s'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/raw_data'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/pizzy/output'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/star_fusion'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/Arriba'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/fusioncatcher'%(args.outdir),shell=True)
subprocess.check_call('mkdir -p %s/fusion_report'%(args.outdir),shell=True)
if not os.path.isfile("%s/raw_data/%s" %(args.outdir,os.path.basename(args.pe1))):
    subprocess.check_call('mv %s %s/raw_data'%(args.pe1,args.outdir),shell=True)
if not os.path.isfile('%s/raw_data/%s'%(args.outdir,os.path.basename(args.pe1))):
    subprocess.check_call('mv %s %s/raw_data'%(args.pe2,args.outdir),shell=True)
###############################
docker_raw="docker run -t -i -v %s:/reference/ -v %s:/project/ %s "%(args.ref,args.outdir,docker_name)
###############################run pizzly
if os.path.exists("%s/pizzy/output/fusion.txt"%((args.outdir))):
    docker_cmd=docker_raw+"/software/kallisto quant -i /reference/kallisto/index.idx --fusion " \
                          "-o /project/pizzy/output /project/raw_data/%s /project/raw_data/%s"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
    subprocess.check_call(docker_cmd,shell=True)
    docker_cmd1=docker_raw+"/software/pizzly-0.37.3/pizzly -k 31 --gtf /reference/kallisto/Homo_sapiens.GRCh38.102.gtf.gz " \
                   "--align-score 2 --insert-size 400 " \
                   "--fasta /reference/kallisto/Homo_sapiens.GRCh38.cdna.all.fa.gz --output /project/pizzy/output/%s /project/pizzy/output/fusion.txt"%(args.prefix)
    subprocess.check_call(docker_cmd1,shell=True)
###############################star_fusion
docker_cmd2=docker_raw+" sh /reference/STAR_fusion.sh /project/raw_data/%s /project/raw_data/%s /project/star_fusion"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
subprocess.check_call(docker_cmd2,shell=True)
###############################Arriba
docker_cmd3=docker_raw+" sh /reference/arriba_fusion.sh /project/%s /project/%s"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
subprocess.check_call(docker_cmd3,shell=True)
###############################fusioncatcher
docker_cmd4=docker_raw+" /software/fusioncatcher-1.20/bin/fusioncatcher -d /reference/fusioncatcher/human_v98/ -o /project/fusioncatcher/ -i /project/raw_data/ --config=/reference/fusioncatcher/configuration.cfg"
subprocess.check_call(docker_cmd4,shell=True)
###############################fusion_report
#docker_cmd5=docker_raw+" /software/python3/Python-v3.7.0/bin/fusion_report run %s /project/fusion_report /reference/fusion_report/ -arriba /project/ --pizzly --fusioncatcher --starfusion  "
