Outline for summer school



JULY 13TH



**From RNA Molecules to Aligned Reads: Understanding Transcriptomic Data**



*Learning objectives*

Students should be able to:

* Understand what RNA-seq measures.
* Understand why reads need to be aligned.
* Distinguish genomic DNA from mature transcripts.
* Interpret splice junctions and alternative splicing.
* Navigate RNA-seq data in IGV.



*Part 1: What exactly does RNA-seq measure?*

DNA → pre-mRNA → mature mRNA → sequencing reads



*Part 2: Why is alignment difficult*

Exon1 ---- intron ---- Exon2



*Part 3: The biological concept - hematopoiesis*

If every blood cell has the same genome, why do they look and behave differently?



*Activity 1: Visualizing RNA-seq in IGV*

Look at spliced vs. non-spliced data, long and short-read (select which ones)



*Activity 2*

Give the students a summary with the marker genes that are expressed during hematopoiesis

Give them the coordinates of the genes

Give them the datasets to visualize on IGV (or create an IGV session to be directly loaded on their computers), they will be named dataset1,dataset2, and so on

The students will need to identify which dataset belongs to the different differentiation states depending on the presence/absence of reads on the marker genes



JULY 20TH



**Differential Expression: How We Compare Cell Types**



*Learning objectives*

Students should be able to:

* Understand gene counts.
* Understand normalization.
* Understand fold-change.
* Understand statistical significance.
* Interpret volcano plots and heatmaps.



*Part 1. From alignments to counts*

Counts represent transcript abundance.



*Part 2. Why raw counts cannot be compared directly*

Concepts only: 1) library size, 2) normalization factors, 3) compositional effects



*Part 3. What is differential expression?*

Explain: fold change, biological variabiltiy, p-values, p-value normalization



*Activity 1: Be the differential expression algorithm*

Give the students a table with the counts of 4-5 genes, tell which ones are unchanged, which ones are up-regulated, and which ones are down-regulated



*Activity 2: Reconstructing cell differentiation*

Give the student a table with another set of counts, with fold changes and p-values.

Give them also a scheme of hematopoiesis.

The students will need to tell from which cell type are the two datasets (the one with up-regulated values, and the one with down-regulated values), and for each of the datasets how many genes are significantly diff. expressed

