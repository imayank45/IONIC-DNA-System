import pandas as pd

def recommend_treatment(df):
    """
    Generate personalized treatment recommendations based on SNP data, summaries, and CPIC/PharmGKB guidelines.
    Args:
        df (pd.DataFrame): DataFrame containing rsID, Gene, Drug(s), Phenotype Category, Significance, Genotype, Notes, etc.
    Returns:
        pd.DataFrame: DataFrame with recommendations (Drug, Recommendation, Rationale).
    """
    recommendations = []

    for _, row in df.iterrows():
        rsid = row['rsID']
        drug = row['Drug(s)']
        gene = row['Gene']
        significance = row['Significance']
        phenotype = row['Phenotype Category']
        genotype = row.get('Genotype', 'Unknown')  # From VCF
        notes = row.get('Notes', '')  # From PharmGKB

        # Rule-based recommendations based on CPIC/PharmGKB guidelines
        if significance == 'yes':
            # rs1801133 (MTHFR) - Methotrexate
            if rsid == 'rs1801133' and drug.lower() == 'methotrexate':
                if genotype == '1/1':  # Homozygous variant
                    recommendation = 'Consider alternative therapy (e.g., leflunomide) due to increased toxicity risk.'
                elif genotype == '0/1':  # Heterozygous
                    recommendation = 'Monitor for toxicity; consider 25-50% dose reduction if adverse effects occur.'
                else:
                    recommendation = 'Proceed with standard dosing, but monitor for toxicity.'
                rationale = f'Variant {rsid} in {gene} (C677T polymorphism) may reduce MTHFR activity, potentially increasing methotrexate toxicity risk. {notes}'
            
            # rs1801133 (MTHFR) - Atorvastatin
            elif rsid == 'rs1801133' and drug.lower() == 'atorvastatin':
                recommendation = 'No specific dosing adjustment recommended; monitor lipid levels and liver function.'
                rationale = f'Variant {rsid} in {gene} has limited evidence for impacting atorvastatin metabolism. {notes}'
            
            # rs2066853 (AHR) - Warfarin
            elif rsid == 'rs2066853' and drug.lower() == 'warfarin':
                if genotype == '1/1':  # Homozygous variant
                    recommendation = 'Reduce initial dose by 20-30% and monitor INR closely.'
                elif genotype == '0/1':  # Heterozygous
                    recommendation = 'Reduce initial dose by 10-20% and monitor INR closely.'
                else:
                    recommendation = 'Use standard dosing, but monitor INR.'
                rationale = f'Variant {rsid} in {gene} may influence warfarin metabolism via AHR pathway, potentially affecting dose requirements. {notes}'
            
            # rs2231142 (ABCG2) - Allopurinol
            elif rsid == 'rs2231142' and drug.lower() == 'allopurinol':
                if genotype == '1/1':  # Homozygous variant
                    recommendation = 'Consider alternative (e.g., febuxostat) due to increased risk of allopurinol hypersensitivity syndrome.'
                elif genotype == '0/1':  # Heterozygous
                    recommendation = 'Start with a lower dose (e.g., 100 mg/day) and titrate slowly; monitor for hypersensitivity.'
                else:
                    recommendation = 'Use standard dosing, but monitor for adverse reactions.'
                rationale = f'Variant {rsid} in {gene} (Q141K polymorphism) is associated with reduced ABCG2 function, increasing allopurinol toxicity risk. {notes}'
            
            else:
                recommendation = 'No specific adjustment recommended based on current data.'
                rationale = f'Variant {rsid} in {gene} has insufficient evidence for dosage adjustment. {notes}'
        else:
            recommendation = 'No adjustment needed.'
            rationale = f'Variant {rsid} has no significant clinical impact on {drug}. {notes}'

        recommendations.append({
            'Drug': drug,
            'Recommendation': recommendation,
            'Rationale': rationale
        })

    return pd.DataFrame(recommendations)