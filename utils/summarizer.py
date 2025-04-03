from transformers import pipeline

# Load the T5-small model for summarization
summarizer = pipeline("text2text-generation", model="t5-small")

def generate_summaries(df):
    prompts = [
        f"Summarize: Variant {row['rsID']} in gene {row['Gene']} affects response to {row['Drug(s)']}. "
        f"Phenotype: {row['Phenotype Category']}. Clinical significance: {row['Significance']}."
        for _, row in df.iterrows()
    ]
    summaries = [summarizer(p, max_length=60, do_sample=False)[0]['generated_text'] for p in prompts]
    df["Summary"] = summaries
    return df