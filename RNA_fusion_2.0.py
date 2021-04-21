#Email:yucai.fan@illumina.com
#2021.04.21
#verison:1.0

import subprocess
import os
import argparse
import time

docker_name="rna:latest"

parse=argparse.ArgumentParser("This script will analysis RNA fusion.")
parse.add_argument("-p1","--pe1",help="R1 fastq",required=True)
parse.add_argument("-p2","--pe2",help="R2 fastq",required=True)
parse.add_argument("-r","--ref",help="reference data directory",required=True)
parse.add_argument("-p","--prefix",help="prefix of output",required=True)
parse.add_argument("-d","--dragen",help="true or false",default="false",choices=["true","false"])
parse.add_argument("-dr","--dragen_ref",help="directory dragen hash table,the version:hg38_graph")
args=parse.parse_args()
###############################
start=time.time()
outdir=""
if os.path.dirname(args.pe1)!=os.path.dirname(args.pe2):
    print("%s and %s must be in the same directory." % (args.pe1,args.pe2))
    exit()
else:
    outdir=os.path.dirname(args.pe1)
    subprocess.check_call('mkdir -p %s/pizzy/output'%(outdir),shell=True)
    subprocess.check_call('mkdir -p %s/star_fusion'%(outdir),shell=True)
    subprocess.check_call('mkdir -p %s/Arriba'%(outdir),shell=True)
    subprocess.check_call('mkdir -p %s/fusioncatcher'%(outdir),shell=True)
    subprocess.check_call('mkdir -p %s/fusion_report'%(outdir),shell=True)
if not os.path.isfile("%s/%s" %(outdir,os.path.basename(args.pe1))):
    subprocess.check_call('mv %s %s/raw_data'%(args.pe1,outdir),shell=True)
if not os.path.isfile('%s/%s'%(outdir,os.path.basename(args.pe2))):
    subprocess.check_call('mv %s %s/raw_data'%(args.pe2,outdir),shell=True)
if args.dragen!="false" and os.path.exists(args.dragen):
    subprocess.check_call('mkdir -p %s/dragen_RNA'%(outdir),shell=True)
    subprocess.check_call('cp %s %s/dragen_RNA/'%(args.dragen,outdir),shell=True)
###############################
docker_raw="docker run -v %s:/reference/ -v %s:/project/ %s "%(args.ref,outdir,docker_name)
###############################pizzy(https://github.com/pmelsted/pizzly)
if not os.path.exists("%s/pizzy/output/fusion.txt"%((outdir))):
    docker_cmd=docker_raw+"/software/kallisto quant -i /reference/kallisto/index.idx --fusion " \
                          "-o /project/pizzy/output /project/%s /project/%s"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
    subprocess.check_call(docker_cmd,shell=True)
    docker_cmd1=docker_raw+"/software/pizzly-0.37.3/pizzly -k 31 --gtf /reference/kallisto/Homo_sapiens.GRCh38.102.gtf.gz " \
                   "--align-score 2 --insert-size 400 " \
                   "--fasta /reference/kallisto/Homo_sapiens.GRCh38.cdna.all.fa.gz --output /project/pizzy/output/%s /project/pizzy/output/fusion.txt"%(args.prefix)
    subprocess.check_call(docker_cmd1,shell=True)
if not os.path.exists("%s/pizzy/output/%s_genetable.txt"%((outdir,args.prefix))):
    docker_tmp=docker_raw+"/software/python3/Python-v3.7.0/bin/python3 /software/pizzly-0.37.3/scripts/flatten_json.py " \
                          "/project/pizzy/output/%s.json /project/pizzy/output/%s_genetable.txt"%(args.prefix,args.prefix)
    subprocess.check_call(docker_tmp,shell=True)
###############################star_fusion(https://github.com/STAR-Fusion/STAR-Fusion/wiki)
if not os.path.exists('%s/star_fusion/star-fusion.fusion_predictions.tsv'%(outdir)):
    docker_cmd2=docker_raw+" sh /reference/STAR_fusion/STAR_fusion.sh /project/%s /project/%s /project/star_fusion"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
    subprocess.check_call(docker_cmd2,shell=True)
###############################Arriba(https://arriba.readthedocs.io/en/latest/)
if not os.path.exists('%s/Arriba/fusions.tsv'%(outdir)):
    docker_cmd3=docker_raw+" sh /reference/arriba/arriba_fusion.sh /project/%s /project/%s"%(os.path.basename(args.pe1),os.path.basename(args.pe2))
    subprocess.check_call(docker_cmd3,shell=True)
###############################fusioncatcher123
if not os.path.exists( '%s/fusioncatcher/final-list_candidate-fusion-genes.txt'%(outdir)):
    docker_cmd4=docker_raw+" /software/fusioncatcher-1.20/bin/fusioncatcher -d /reference/fusioncatcher/human_v98/ -o /project/fusioncatcher/ -i /project/ --config=/reference/fusioncatcher/configuration.cfg"
    subprocess.check_call(docker_cmd4,shell=True)
###############################fusion_report(https://github.com/matq007/fusion-report)
docker_cmd5=docker_raw+" /software/python3/Python-v3.7.0/bin/fusion_report run %s /project/fusion_report/ " \
                       "/reference/fusion_report/ --arriba /project/Arriba/fusions.tsv --pizzly /project/pizzy/output/%s_genetable.txt " \
                       "--fusioncatcher /project/fusioncatcher/final-list_candidate-fusion-genes.txt " \
                       "--starfusion /project/star_fusion/star-fusion.fusion_predictions.tsv "%(args.prefix,args.prefix)
###############################dragen RNA fusion
if args.dragen != "false":
    subprocess.check_call('mkdir -p %s/dragen' % (outdir), shell=True)
    if not os.path.exists("%s/dragen_RNA/%s.fusion_candidates.final"%(outdir,args.prefix)):
        dragen_cmd="dragen -f -r %s -1 %s -2 %s -a %s/gtf/gencode.v37.chr_patch_hapl_scaff.annotation.gtf --output-dir %s/dragen/  --output-file-prefix %s --Mapper.max-intron-bases=100000 --rna-gf-min-cis-distance 100000 " \
                   " --rna-gf-min-score 0.35 --RGID dragen_RGID --RGSM illumina --enable-rna true --enable-rna-gene-fusion true "%(args.dragen_ref,args.pe1,args.pe2,args.ref,outdir,args.prefix)
        subprocess.check_call(dragen_cmd,shell=True)
    infile=open("%s/dragen/%s.fusion_candidates.final"%(outdir,args.prefix),"r")
    outfile = open("%s/dragen/%s.fusion.final" % (outdir, args.prefix), "w")
    num=0
    for line in infile:
        num+=1
        line=line.strip()
        if num!=0:
            if int(line.split("\t")[6])>=3:
                outfile.write("%s\n"%(line))
        else:
            outfile.write("%s\n" % (line))
    infile.close()
    outfile.close()
    docker_cmd5 += " --dragen /project/dragen/%s.fusion.final " % (args.prefix)
subprocess.check_call(docker_cmd5,shell=True)
subprocess.check_call("mkdir -p %s/fusion_final_report && mv %s/fusion_report/index.html %s/fusion_final_report && rm -rf %s/fusion_report/"
                      %(outdir,outdir,outdir,outdir),shell=True)
end=time.time()
print("Elapse time is %g seconds" %(end-start))