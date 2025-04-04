import os
import time
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from transformers import pipeline
from xhtml2pdf import pisa  # For PDF generation
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ionicDNASecretKey'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load transformer pipelines
summarizer = pipeline("text2text-generation", model="t5-small")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Parse VCF into snp_data.csv
def parse_vcf(filepath, output_csv='uploads/snp_data.csv'):
    snps = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 10:
                continue
            chrom, pos, rsid, ref, alt, qual, filter_, info, format_, sample = parts[:10]
            if rsid.startswith('rs'):
                genotype = sample.split(':')[0]
                snps.append([chrom, pos, rsid, ref, alt, genotype])
            if len(snps) >= 300:
                break
    df = pd.DataFrame(snps, columns=['Chromosome', 'Position', 'rsID', 'Ref', 'Alt', 'Genotype'])
    print("Parsed SNPs from VCF:", df.head().to_dict())
    df.to_csv(output_csv, index=False)
    return output_csv

# Match rsIDs to PharmGKB
def map_snps_to_drugs(snp_csv, ann_tsv='data/var_drug_ann.tsv'):
    snp_df = pd.read_csv(snp_csv)
    print("SNPs from VCF file:", snp_df.head().to_dict())
    drug_ann_df = pd.read_csv(ann_tsv, sep='\t', low_memory=False)
    print("PharmGKB first few entries:", drug_ann_df.head().to_dict())
    merged = pd.merge(snp_df, drug_ann_df, left_on="rsID", right_on="Variant/Haplotypes", how="inner")
    print("Merged DataFrame:", merged.head().to_dict())
    output_cols = ["rsID", "Gene", "Drug(s)", "Phenotype Category", "Significance", "Chromosome", "Position", "Ref", "Alt", "Genotype", "Notes"]
    return merged[output_cols] if not merged.empty else pd.DataFrame(columns=output_cols)

# Generate T5 summaries
def generate_summaries(df):
    prompts = [
        f"Summarize: Variant {row['rsID']} in gene {row['Gene']} affects response to {row['Drug(s)']}. "
        f"Phenotype: {row['Phenotype Category']}. Clinical significance: {row['Significance']}."
        for _, row in df.iterrows()
    ]
    summaries = [summarizer(p, max_length=60, do_sample=False)[0]['generated_text'] for p in prompts]
    df["Summary"] = summaries
    return df

# Generate treatment recommendations
def generate_treatment_recommendations(df):
    recommendations = []
    for _, row in df.iterrows():
        rsid = row['rsID']
        drug = row['Drug(s)']
        gene = row['Gene']
        significance = row['Significance']
        genotype = row['Genotype']
        
        if significance.lower() != 'yes':
            recommendation = f"No significant clinical impact for {drug} based on {rsid}."
            rationale = "Clinical significance not established."
        else:
            if rsid == 'rs1801133' and drug.lower() == 'methotrexate':
                if genotype == '0/1':
                    recommendation = f"Consider 25-50% dose reduction for {drug}."
                    rationale = f"Heterozygous variant in {gene} (C677T) may increase toxicity risk."
                elif genotype == '1/1':
                    recommendation = f"Consider alternative therapy to {drug}."
                    rationale = f"Homozygous variant in {gene} (C677T) significantly increases toxicity risk."
                else:
                    recommendation = f"Standard dosing for {drug}."
                    rationale = f"No variant detected in {gene} for this SNP."
            elif rsid == 'rs2066853' and drug.lower() == 'warfarin':
                if genotype in ['0/1', '1/1']:
                    recommendation = f"Monitor INR closely when using {drug}."
                    rationale = f"Variant in {gene} may affect metabolism, increasing bleeding risk."
                else:
                    recommendation = f"Standard dosing for {drug}."
                    rationale = f"No variant detected in {gene} for this SNP."
            else:
                recommendation = f"Standard dosing for {drug}."
                rationale = "No specific guideline available for this variant-drug pair."
        
        recommendations.append({
            'Drug': drug,
            'Recommendation': recommendation,
            'Rationale': rationale
        })
    
    return pd.DataFrame(recommendations)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Upload handler → redirect to /analyzing
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['filename'] = filename
        return redirect(url_for('analyzing', filename=filename))

# Analyzing screen → background processing → redirect to /results
@app.route('/analyzing/<filename>')
def analyzing(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        if filename.endswith('.vcf'):
            print("📄 Detected VCF. Parsing...")
            snp_csv = parse_vcf(filepath)
            print("✅ VCF parsed.")
        else:
            return "Unsupported file format. Please upload a .vcf file.", 400

        merged_df = map_snps_to_drugs(snp_csv)
        if merged_df.empty:
            return "No drug-related SNPs found in your DNA file.", 200

        print("🧠 Generating summaries with T5...")
        final_df = generate_summaries(merged_df)
        print("✅ Summaries done.")

        summary_path = os.path.join(app.config['UPLOAD_FOLDER'], 'snp_summary.csv')
        final_df.to_csv(summary_path, index=False)

        return redirect(url_for('results', filename='snp_summary.csv'))

    except Exception as e:
        return f"Processing failed: {str(e)}", 500

# Treatment recommendations route (MOVED BEFORE results)
@app.route('/treatment/<filename>')
def treatment(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        df = pd.read_csv(filepath)
        treatment_df = generate_treatment_recommendations(df)
        return render_template('treatment.html', tables=[treatment_df.to_html(classes='data-table')], titles=treatment_df.columns.values, filename=filename)
    except Exception as e:
        return f"Error generating treatment recommendations: {str(e)}", 500

# Chatbot route (MOVED BEFORE results)
@app.route('/chatbot/<filename>', methods=['GET', 'POST'])
def chatbot(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        df = pd.read_csv(filepath)
        context = " ".join(df['Summary'].tolist())
        answer = None
        if request.method == 'POST':
            question = request.form['question']
            result = qa_pipeline(question=question, context=context)
            answer = result['answer']
        return render_template('chatbot.html', filename=filename, answer=answer)
    except Exception as e:
        return f"Error in chatbot: {str(e)}", 500

# Generate and download PDF report (MOVED BEFORE results)
@app.route('/generate_report/<filename>')
def generate_report(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(filepath)

        html_content = render_template(
            "report_template.html",
            table=df.to_html(classes='table table-bordered', index=False),
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        static_upload_path = os.path.join('static', 'uploads')
        os.makedirs(static_upload_path, exist_ok=True)
        pdf_path = os.path.join(static_upload_path, 'IONIC_DNA_Report.pdf')

        with open(pdf_path, "w+b") as f:
            pisa_status = pisa.CreatePDF(html_content, dest=f)
            if pisa_status.err:
                return "Failed to generate PDF", 500

        return redirect(url_for('static', filename='uploads/IONIC_DNA_Report.pdf'))
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500

# Results route (NOW AFTER treatment, chatbot, and generate_report)
@app.route('/results/<filename>')
def results(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        df = pd.read_csv(filepath)
        return render_template('results.html', tables=[df.to_html(classes='data-table')], titles=df.columns.values, filename=filename)
    except Exception as e:
        return f"Error loading results: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)