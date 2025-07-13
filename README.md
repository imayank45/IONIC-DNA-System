# 🚀 IONIC DNA System: Personalized Pharmacogenomic Analysis

## 🌟 Overview

The **IONIC DNA System** is a Flask-based web application for personalized pharmacogenomic analysis. By processing Variant Call Format (VCF) files and integrating with the PharmGKB database, it helps uncover how genetic variants influence drug response. Fine-tuned NLP models (T5-small and DistilBERT) power summary generation, query answering, and treatment recommendations. A downloadable PDF report and a sci-fi-themed UI elevate the user experience.

This project demonstrates strengths in bioinformatics, natural language processing, and full-stack development.

---

## 🎯 Features

- 🔍 **VCF Parsing**: Extracts SNPs (e.g., rsID, genotype) into structured CSV format.
- 📚 **PharmGKB Integration**: Maps SNPs to drug interactions using `var_drug_ann.tsv`.
- ✍️ **NLP Summarization**: Generates SNP-drug summaries via T5-small (ROUGE-1: 0.65).
- ❓ **QA Chatbot**: Answers queries like “What does rs1801133 affect?” using DistilBERT (F1: 0.85).
- 💊 **Treatment Recommendations**: Provides genotype-based drug dosage advice (e.g., 25–50% methotrexate reduction).
- 📄 **PDF Report Generation**: Creates downloadable summary reports.
- 🎨 **Sci-Fi UI**: Futuristic design with DNA helix video background.

---

## 📦 Installation

### Prerequisites

- 🐍 Python 3.8+
- 📦 pip
- 📂 PharmGKB file: `var_drug_ann.tsv`

### Dependencies

Install required packages:
```bash
pip install flask pandas transformers torch xhtml2pdf
````

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ionic-dna-system.git
cd ionic-dna-system

# Place PharmGKB file
mkdir -p data && mv var_drug_ann.tsv data/

# Create upload directories
mkdir -p uploads static/uploads

# Run the app
python app.py
```

---

## 🛠️ Usage

1. Open the app in your browser (typically at `http://127.0.0.1:5000/`).
2. Upload a VCF file (e.g., `test_dna.vcf`) on the homepage.
3. View results on the `/results` page.
4. Use additional features:

   * 💊 Treatment recommendations: `/treatment`
   * ❓ Ask questions: `/chatbot`
   * 📄 Generate report: `/generate_report`
5. Download your report from `static/uploads/IONIC_DNA_Report.pdf`.

### Sample VCF Format

```
##fileformat=VCFv4.2
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM  POS     ID          REF  ALT  QUAL  FILTER  INFO  FORMAT  SAMPLE
1       11856378 rs1801133   G    A    100   PASS    .     GT      0/1
2       11169867 rs2066853   G    A    100   PASS    .     GT      1/1
3       14131367 rs2231142   G    T    100   PASS    .     GT      0/0
```

---

## 📁 Folder Structure

```
ionic-dna-system/
├── app.py
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── video/dna_background.mp4
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── analyzing.html
│   ├── results.html
│   ├── treatment.html
│   ├── chatbot.html
│   ├── 404.html
│   └── report_template.html
├── uploads/
├── data/
│   └── var_drug_ann.tsv
└── utils/
    ├── __init__.py
    ├── vcf_parser.py
    ├── drug_matcher.py
    ├── summarizer.py
    ├── qa_chatbot.py
    └── treatment_recommender.py
```

---

## 💻 Technical Details

* **Backend**: Flask (v2.3.2), Jinja2 templates
* **Routes**: `/results/<filename>`, `/chatbot/<filename>`, `/treatment/<filename>`, `/generate_report/<filename>`
* **Data Handling**: `pandas` for parsing and merging VCF and PharmGKB data

### NLP Models

* **T5-small**

  * Parameters: 60M
  * Fine-tuned on 500 samples
  * ROUGE-1: 0.65
  * Max input: 512 tokens
  * Output capped at 60 tokens

* **DistilBERT (base-uncased-distilled-squad)**

  * Parameters: 66M
  * Fine-tuned on 300 QA pairs
  * F1 score: 0.85
  * Max input: 512 tokens

* **PDF Generation**: `xhtml2pdf` to convert HTML reports to printable PDF.

* **UI Design**: Dark theme with cyan accents and animated DNA helix background.

* **Performance**:

  * CPU inference
  * T5: \~0.5–1s/request
  * DistilBERT: \~0.3–0.5s/request
  * Single-threaded (debug mode)

---

## ⚠️ Limitations

* 🔢 Max 300 SNPs per VCF to conserve memory
* 💊 Recommendations are guideline-based, **not clinically validated**
* 📡 No real-time PharmGKB/CPIC API (uses static TSV)
* 📄 PDF styling simplified for compatibility
* ⚙️ Debug server is not production-ready

---

## 🚀 Future Improvements

* 🌐 Real-time API integration with PharmGKB/CPIC
* ⚡ GPU support for faster inference
* 🗄️ Switch to a database (PostgreSQL)
* 🎮 Upgrade UI to React for dynamic interactions
* 📊 Add visualizations (e.g., chromosome maps via Plotly)

---

## 📄 License

This project is for **educational purposes only** and is **not intended for clinical use**. You are welcome to use or adapt it, but always consult a licensed medical professional for healthcare decisions.

```
