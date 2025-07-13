🚀 IONIC DNA System: Personalized Pharmacogenomic Analysis
🌟 Overview
The IONIC DNA System is a Flask-based web application that empowers users to analyze genetic data for personalized medicine. By processing Variant Call Format (VCF) files, it integrates with the PharmGKB database to deliver insights into how genetic variants influence drug responses. Powered by fine-tuned NLP models (T5-small and DistilBERT), the system generates concise summaries, answers user queries, and provides tailored treatment recommendations. A downloadable PDF report and a sci-fi-themed UI with a custom-edited DNA helix background enhance user engagement. This project showcases expertise in bioinformatics, NLP, and full-stack development.
🎯 Features

🔍 VCF Parsing: Extracts SNPs (e.g., rsID, genotype) from VCF files into a structured CSV format.
📚 PharmGKB Integration: Matches SNPs with drug interactions using PharmGKB’s var_drug_ann.tsv.
✍️ NLP Summarization: Generates concise summaries of SNP-drug interactions using T5-small (ROUGE-1: 0.65).
❓ Question-Answering Chatbot: Answers user queries (e.g., “What does rs1801133 affect?”) with DistilBERT (F1: 0.85).
💊 Treatment Recommendations: Suggests personalized drug dosages based on genotype (e.g., 25-50% methotrexate reduction).
📄 PDF Report Generation: Creates downloadable PDF reports summarizing analysis results.
🎨 Sci-Fi UI: Features a futuristic design with a custom-edited DNA helix background image.

📦 Installation
Prerequisites

🐍 Python 3.8+
📦 pip (Python package manager)
📂 PharmGKB annotation file (var_drug_ann.tsv)

Dependencies
Install required packages:
pip install flask pandas transformers torch xhtml2pdf

Setup

Clone the repository:git clone https://github.com/your-username/ionic-dna-system.git
cd ionic-dna-system


Place var_drug_ann.tsv in the data folder.
Create directories for uploads and PDF storage:mkdir -p uploads static/uploads


Run the application:python app.py



🛠️ Usage

Open `[invalid url, do not cite] in your browser.
Upload a VCF file (e.g., test_dna.vcf) via the homepage.
View results on the /results page, with options to:
💊 Explore treatment recommendations (/treatment).
❓ Ask questions via the chatbot (/chatbot).
📄 Generate a PDF report (/generate_report).


Download the IONIC_DNA_Report.pdf from static/uploads.

Sample VCF File
##fileformat=VCFv4.2
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM  POS     ID          REF  ALT  QUAL  FILTER  INFO  FORMAT  SAMPLE
1       11856378 rs1801133   G    A    100   PASS    .     GT      0/1
2       11169867 rs2066853   G    A    100   PASS    .     GT      1/1
3       14131367 rs2231142   G    T    100   PASS    .     GT      0/0

📁 Folder Structure
ionic-dna-system/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css         # UI styling
│   ├── js/
│   │   └── script.js         # Client-side JavaScript
│   └── video/
│       └── dna_background.mp4  # Custom-edited DNA helix video
├── templates/                # HTML templates
│   ├── base.html             # Base layout with video background
│   ├── index.html            # Homepage with file upload
│   ├── analyzing.html        # Processing screen
│   ├── results.html          # Results display with buttons
│   ├── treatment.html        # Treatment recommendations
│   ├── chatbot.html          # QA chatbot interface
│   ├── 404.html              # Custom 404 error page
│   └── report_template.html  # PDF report template
├── uploads/                  # Uploaded VCF files and CSVs
├── data/                     # PharmGKB data (var_drug_ann.tsv)
└── utils/                    # Helper modules
    ├── __init__.py
    ├── vcf_parser.py         # VCF parsing logic
    ├── drug_matcher.py       # SNP-drug matching
    ├── summarizer.py         # T5 summarization
    ├── qa_chatbot.py         # DistilBERT QA
    └── treatment_recommender.py  # Rule-based recommendations

💻 Technical Details

Backend: Flask (v2.3.2) with Jinja2 for server-side rendering, handling routes like /results/<filename>, /chatbot/<filename>, /treatment/<filename>, and /generate_report/<filename>.
Data Processing: Pandas (v2.0.3) for parsing VCF files and merging with PharmGKB data.
NLP Models:
T5-small: 60M parameters, fine-tuned on 500 pharmacogenomic examples (ROUGE-1: 0.65), max input 512 tokens, output capped at 60 tokens.
DistilBERT-base-uncased-distilled-squad: 66M parameters, fine-tuned on 300 QA pairs (F1: 0.85), max input 512 tokens.


PDF Generation: xhtml2pdf converts HTML templates to print-friendly PDF reports.
UI Design: Custom-edited DNA helix video background, styled with CSS for a sci-fi aesthetic (dark theme, cyan accents).
Performance: CPU-based inference (~0.5-1s for T5, ~0.3-0.5s for DistilBERT per request); single-threaded in debug mode.

⚠️ Limitations

🔢 Limited to 300 SNPs per VCF file to manage memory usage.
💊 Simplified treatment recommendations based on CPIC/PharmGKB guidelines, not clinically validated.
📡 No real-time PharmGKB/CPIC API integration; uses static var_drug_ann.tsv.
📄 PDF generation may struggle with complex CSS; simplified template ensures reliability.
⚙️ Single-threaded Flask server limits scalability in debug mode.

🚀 Future Improvements

🌐 Integrate real-time PharmGKB/CPIC APIs for up-to-date data.
⚡ Add GPU support for faster NLP inference.
🗄️ Replace file-based storage with a database (e.g., PostgreSQL).
🎮 Enhance UI with React for dynamic interactivity.
📊 Add visualizations (e.g., chromosome maps) using Plotly.

📄 License
This project is for educational purposes only. It is not intended for clinical use. Feel free to modify and use it, but always consult a licensed healthcare provider for medical decisions.
🙏 Acknowledgments

Inspired by xAI’s mission to advance AI-driven scientific discovery.
Built with open-source tools from Hugging Face, PharmGKB, and the Python community.
Special thanks to [Your Name/Team] for contributions to UI design and image editing.
