import os
from transformers import BartForConditionalGeneration, BartTokenizer
import torch

def summarize_transcript(transcript_path):
    if not os.path.exists(transcript_path):
        print(f"❌ File '{transcript_path}' not found.")
        return

    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()

    print("🔁 Loading BART model and tokenizer...")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

    print("🧠 Summarizing transcript...")
    inputs = tokenizer.encode(transcript, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=200, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Save summary to text file
    summary_file = os.path.splitext(transcript_path)[0] + "_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"\n✅ Summary saved to: {summary_file}")
    print("\n📝 Summary Preview:\n")
    print(summary)

if __name__ == "__main__":
    transcript_path = input("📄 Enter the path to the transcript text file: ").strip()
    summarize_transcript(transcript_path)
