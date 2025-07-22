from transformers import pipeline

# Load summarizer model once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text: str, max_chunks=5) -> list:
    """
    Break text into chunks and summarize each.
    Returns list of bullet-point summaries.
    """
    summaries = []
    max_len = 900  # Tokens per chunk (~900 words max for distilbart)

    # Split into smaller chunks
    paragraphs = text.split("\n")
    chunk = ""

    for para in paragraphs:
        if len(chunk) + len(para) < max_len:
            chunk += para + "\n"
        else:
            summaries += summarize_chunk(chunk)
            chunk = para + "\n"

        if len(summaries) >= max_chunks:
            break

    if chunk and len(summaries) < max_chunks:
        summaries += summarize_chunk(chunk)

    return summaries

def summarize_chunk(chunk: str) -> list:
    try:
        result = summarizer(chunk.strip(), max_length=130, min_length=30, do_sample=False)
        bullet = result[0]['summary_text']
        return [f"• {bullet.strip()}"]
    except:
        return ["• (Could not summarize this section)"]
