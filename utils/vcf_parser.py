import pandas as pd

def parse_vcf(filepath, output_csv='uploads/snp_data.csv'):
    snps = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 10:  # Ensure enough columns for genotype
                continue
            chrom, pos, rsid, ref, alt, qual, filter_, info, format_, sample = parts[:10]
            if rsid.startswith('rs'):
                # Extract genotype (e.g., 0/1, 1/1) from the sample column
                genotype = sample.split(':')[0]  # Assuming GT is the first field in FORMAT
                snps.append([chrom, pos, rsid, ref, alt, genotype])
            if len(snps) >= 300:  # Limit for demo
                break
    df = pd.DataFrame(snps, columns=['Chromosome', 'Position', 'rsID', 'Ref', 'Alt', 'Genotype'])
    print("Parsed SNPs from VCF:", df.head().to_dict())  # Debug print
    df.to_csv(output_csv, index=False)
    return output_csv