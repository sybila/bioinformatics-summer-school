
# Methylation exercise

## 🧬 Prepare the environment

1. Download **IGV with Java** and open it (the same way as on the first day).

2. Download the **modkit** binary:
   - `modkit_v0.6.4_u16_x86_64.tar.gz`
   - from the modkit GitHub releases page  https://github.com/nanoporetech/modkit/releases

3. Download the **BAM** file.

## 🧬 Explore the methylation bam file

Great! We will start with a BAM file that stores the read alignments, together with methylation tags. The next step will be for us to visualize the data using an IGV. 

To do this, we will need a reference genome—either one of the pre-loaded references in IGV or our own custom reference. Make sure that the sequence names (such as chromosome labels) are consistent between your BAM file and the reference. Both the reference and the BAM file can be loaded either locally (from your computer) or remotely (for example, from a website).  

Let’s try this in IGV:  
- Open IGV and load your old-fashioned hg38 reference that is already pre-loaded in your IGV (do not use a custom reference this time), alongside its annotated genes
- Load your BAM file  
- In the search bar, type KCNQ1OT1 to jump to that gene  
- Turn on the methylation (depending on your version of IGV, you might want to right-click on the reads, select "Color alignments by", and then pick "*base modification 2-color (5mC)*")

Do you recognize this gene? What do you observe in the methylation pattern—and does it match what you expected?

## 🧬 Call Methylation
Call methylation with **modkit**:

In this section, we’ll learn how to call methylation from a pileup of reads that include methylation tags. The idea is simple: for each genomic position, we’ll use all the reads that cover that site to evaluate whether there’s evidence of methylation.  

We’ll use modkit for this task. Here’s an example command:  

```bash
# let's proceed with modkit:
modkit pileup \
    KCNQ1OT1.bam KCNQ1OT1.modkit.bedgraph \
    --filter-threshold C:0.8 \
    --ignore h \
    --force-allow-implicit \
    --cpg \
    --ref GCA_000001405.15_GRCh38_no_alt_analysis_set.fna \
    --combine-strands \
    --bedgraph 
```
While there’s a simpler way to run modkit, listing out these options is useful—it encourages you to think carefully about which parameters make the most sense for your specific project.  

Let's break this command down using modkit's advanced documentation from https://github.com/nanoporetech/modkit/blob/master/book/src/advanced_usage.md.

 *--filter-threshold*

A higher number corresponds to stricter filtering. Always keep your sequencing coverage in mind—because thresholds can behave very differently depending on how much data you have. For example, 3 out of 4 reads supporting methylation is not nearly as reliable as 30 out of 40 reads, even though both technically meet the same ratio.

*--ignore h*
          
This time, we're only interested in 5mC, not 5hmC. This might or might not be a good idea depending on your biological sample. Ignore a modified base class in situ by redistributing base modification probability equally across other options. For example, if collapsing 'h', with 'm' and canonical options, half of the probability of 'h' will be added to both 'm' and 'C'. A full description of the methods can be found in collapse.md

 *--combine-strands*

When performing motif analysis (such as CpG), sum the counts from the positive and negative strands into the counts for the positive strand position

 *--cpg*
 
 Only output counts at CpG motifs. Requires a reference sequence to be provided as well as FAI index
          
 *--bedgraph*
          
Convenient output file format that includes not only the probability of each modification, but also sequencing coverage. Always check sequencing coverage before trusting any modifications. 

👉 Side note: the update-tags command in modkit renames the Mm/Ml tags to MM/ML.

Now that we’ve seen what modkit does, let’s try visualizing the results. Load your bedGraph file into IGV. By default, modkit creates a folder with modification files—look for m_CG0_combined.bedgraph and open it.

Once it’s loaded, ask yourself:  
  -Does the result look like what you expected?  
  -What changes when you lower the filter-threshold?  
  -What do you see if you include 5hmC instead of ignoring it?  
  -And finally, how does the output differ if you don’t use the --bedgraph option at all?  

Does any gene region look particularly interesting to you?

If you have some extra time, we encourage you to explore the modkit documentation. There are many additional options available, and each can shape your results in different ways. Ultimately, the best settings will depend on the biological question you’re trying to answer.



