library( "VariantAnnotation" )
library(TxDb.Hsapiens.UCSC.hg19.knownGene)

filepath <- commandArgs(TRUE)[1]
genome <- commandArgs(TRUE)[2]
locate <- commandArgs(TRUE)[3]
out_dir <- commandArgs(TRUE)[4]


## start from single file first
vcf <- readVcf(filepath, genome)

txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
seqlevels(vcf) <- "chr22"
rd <- rowData(vcf)
loc.cat <- switch(locate,
              all = AllVariants(),
              coding = CodingVariants(),
              intron = IntronVariants(),
              fiveUTR = FiveUTRVariants(),
              threeUTR = ThreeUTRVariants(),
              intergenic = IntergenicVariants(),
              sliceSite = SpliceSiteVariants(),
              promoter = PromoterVariants())
loc <- locateVariants(rd, txdb, loc.cat)
names(loc) <- NULL
write.table(as.data.frame(loc), file = paste0(out_dir, "/sum.tsv"), sep='\t', row.names=FALSE)
