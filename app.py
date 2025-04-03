import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils.vcf_parser import parse_vcf
from utils.drug_matcher import map_snps_to_drugs
from utils.summarizer import generate_summaries
from utils.qa_chatbot import answer_question
from utils.treatment_recommender import recommend_treatment

app = Flask(__name__)
app.secret_key = 'ionicDNASecretKey'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/results/<filename>')
def results(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        return render_template('results.html', tables=[df.to_html(classes='data-table')], titles=df.columns.values, filename=filename)
    except Exception as e:
        return f"Error loading results: {str(e)}", 500

@app.route('/chatbot/<filename>', methods=['GET', 'POST'])
def chatbot(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        context = " ".join(df['Summary'].astype(str).tolist())
        
        answer = None
        question = None
        if request.method == 'POST':
            question = request.form.get('question')
            if question:
                answer = answer_question(question, context)
        
        return render_template('chatbot.html', context=context, question=question, answer=answer, filename=filename)
    except Exception as e:
        return f"Error loading chatbot: {str(e)}", 500

@app.route('/treatment/<filename>')
def treatment(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        treatment_df = recommend_treatment(df)
        return render_template('treatment.html', tables=[treatment_df.to_html(classes='data-table')], titles=treatment_df.columns.values, filename=filename)
    except Exception as e:
        return f"Error loading treatment recommendations: {str(e)}", 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)