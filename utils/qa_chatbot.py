from transformers import pipeline

# Load the question-answering model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def answer_question(question, context):
    """
    Answer a question based on the given context (summaries).
    Args:
        question (str): The user's question.
        context (str): The context (e.g., concatenated summaries).
    Returns:
        str: The answer to the question.
    """
    result = qa_pipeline(question=question, context=context)
    return result['answer']