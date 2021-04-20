# RNAseq学习笔记

1.  download docker images:**rna:latest**

2. RNA fusion find using software as following:<br>
   
       dragen(ref hash table must be hg38)
       pizzy(0.37.3)
       Arriba(2.0.0)
       star_fusion(v1.9.1)
       fusioncatcher(1.20)

3. The result was combined by **fusion_report**

4. Example command:

        python3 RNA_fusion.py -p1 /staging/fanyucai/fusion/UHR_S4_L001_R1_001.fastq.gz -p2 /staging/fanyucai/fusion/UHR_S4_L001_R2_001.fas tq.gz -r /staging3/RNA_fusion/reference/ -dr /staging/reference/hg38_rna/ -p test -d true

5. usage:

        python3 RNA_fusion.py --help
        usage: This script will analysis RNA fusion. [-h] -p1 PE1 -p2 PE2 -r REF -p PREFIX [-d {true,false}] [-dr DRAGEN_REF]
        
        optional arguments:
          -h, --help            show this help message and exit
          -p1 PE1, --pe1 PE1    R1 fastq
          -p2 PE2, --pe2 PE2    R2 fastq
          -r REF, --ref REF     reference data directory
          -p PREFIX, --prefix PREFIX
                                prefix of output
          -d {true,false}, --dragen {true,false}
                                true or false
          -dr DRAGEN_REF, --dragen_ref DRAGEN_REF
                                directory dragen hash table,the version:hg38_graph
    


5. output: 
   
[index.html](./index.html)

6. Run time

    TruSight RNA fusion(1397.71 seconds).

## 参考文献

* [Conesa A, Madrigal P, Tarazona S, et al. A survey of best practices for RNA-seq data analysis[J]. Genome biology, 2016, 17(1): 13.](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-0881-8)

* [Haas B J, Dobin A, Li B, et al. Accuracy assessment of fusion transcript detection via read-mapping and de novo fusion transcript assembly-based methods[J]. Genome biology, 2019, 20(1): 213.](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-019-1842-9)

* [Owens N D L, De Domenico E, Gilchrist M J. An RNA-seq protocol for differential expression analysis[J]. Cold Spring Harbor Protocols, 2019, 2019(6): pdb. prot098368.](http://cshprotocols.cshlp.org/content/2019/6/pdb.prot098368.full)

* [Lee H, Huang A Y, Wang L, et al. Diagnostic utility of transcriptome sequencing for rare Mendelian diseases[J]. Genetics in Medicine, 2020, 22(3): 490-499.](https://www.nature.com/articles/s41436-019-0672-1)

* [Gonorazky H D, Naumenko S, Ramani A K, et al. Expanding the boundaries of RNA sequencing as a diagnostic tool for rare mendelian disease[J]. The American Journal of Human Genetics, 2019, 104(3): 466-483.](https://pubmed.ncbi.nlm.nih.gov/30827497/)

* [Van Den Berge K, Hembach K M, Soneson C, et al. RNA sequencing data: hitchhiker's guide to expression analysis[J]. 2019.](https://www.annualreviews.org/doi/abs/10.1146/annurev-biodatasci-072018-021255)

* [Tumor Profiling: Methods and Protocols[M]. Humana Press, 2019.](https://www.springer.com/gp/book/9781493990023)

* [Hartley T, Lemire G, Kernohan K D, et al. New Diagnostic Approaches for Undiagnosed Rare Genetic Diseases[J]. Annual Review of Genomics and Human Genetics, 2020, 21.](https://pubmed.ncbi.nlm.nih.gov/32283948/)

* [Gene Expression Analysis: Methods and Protocols[M]. Humana Press, 2018.](https://www.springer.com/gp/book/9781493978335)

* [Zhao S, Ye Z, Stanton R. Misuse of RPKM or TPM normalization when comparing across samples and sequencing protocols[J]. RNA, 2020: rna. 074922.120.](https://rnajournal.cshlp.org/content/early/2020/04/13/rna.074922.120.short)

* [Arindrarto W, Borràs D M, de Groen R A L, et al. Comprehensive diagnostics of acute myeloid leukemia by whole transcriptome RNA sequencing[J]. Leukemia, 2020: 1-15.](https://www.nature.com/articles/s41375-020-0762-8)