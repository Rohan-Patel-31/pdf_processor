from transformers import pipeline

# ⚡ Faster than BART, works well for dev
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

def summarize_text(text, max_chunk_len=512, max_summary_len=200):
    chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
    summaries = []
    for chunk in chunks:
        result = summarizer(chunk, max_length=max_summary_len, min_length=30, do_sample=False)
        summaries.append(result[0]['summary_text'])
    return ' '.join(summaries)



