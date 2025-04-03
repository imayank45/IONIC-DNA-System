import pandas as pd

def map_snps_to_drugs(snp_csv, ann_tsv='data/var_drug_ann.tsv'):
    snp_df = pd.read_csv(snp_csv)
    print("SNPs from VCF file:", snp_df.head().to_dict())  # Debug print
    drug_ann_df = pd.read_csv(ann_tsv, sep='\t', low_memory=False)
    print("PharmGKB first few entries:", drug_ann_df.head().to_dict())  # Debug print
    merged = pd.merge(snp_df, drug_ann_df, left_on="rsID", right_on="Variant/Haplotypes", how="inner")
    print("Merged DataFrame:", merged.head().to_dict())  # Debug print
    output_cols = ["rsID", "Gene", "Drug(s)", "Phenotype Category", "Significance", "Chromosome", "Position", "Ref", "Alt", "Genotype", "Notes"]
    return merged[output_cols] if not merged.empty else pd.DataFrame(columns=output_cols)