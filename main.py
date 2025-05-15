# main.py
# Data-Refining-Pipeline: Gemini Text Processor (Local Version)

import os
import json
import google.generativeai as genai
from tqdm import tqdm
import PyPDF2
import docx

def extract_text_from_file(input_file_path):
    ext = os.path.splitext(input_file_path)[1].lower()
    if ext == '.txt':
        with open(input_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        text = ''
        with open(input_file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
    elif ext == '.docx':
        doc = docx.Document(input_file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError('Unsupported file type. Supported: .txt, .pdf, .docx')

def process_with_gemini(input_file_path, output_file_path, api_key, system_prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
    text_content = extract_text_from_file(input_file_path)
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        chunks = [chunk.strip() for chunk in text_content.split('\n\n') if chunk.strip()]
        for chunk in tqdm(chunks, desc="Processing chunks"):
            try:
                conversation = {
                    "contents": [
                        {"role": "user", "parts": [{"text": chunk}]},
                        {"role": "model", "parts": [{"text": ""}]}
                    ]
                }
                response = model.generate_content(chunk, request_options={"timeout": 60})
                conversation["contents"][1]["parts"][0]["text"] = response.text
                json_line = json.dumps(conversation, ensure_ascii=False, indent=None)
                outfile.write(json_line + '\n')
                print(f"Processed: {chunk[:50]}...")
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                error_conversation = {
                    "contents": [
                        {"role": "user", "parts": [{"text": chunk}]},
                        {"role": "model", "parts": [{"text": f"ERROR: {str(e)}"}]}
                    ]
                }
                outfile.write(json.dumps(error_conversation, ensure_ascii=False, indent=None) + '\n')

def main():
    print("=== Gemini Data Refining Tool ===")
    api_key = input("Enter your Google AI Studio API key: ").strip()
    system_prompt = """
You are an AI assistant preparing a dataset for fine-tuning a language model using conversational data.

The input is a long raw text file with informal Q/A dialogue or narrative content. Your task is to:

1. Carefully read and understand the context of the full text.
2. Use your creativity and natural understanding of conversation flow to segment the text into coherent question-answer or prompt-response pairs.
3. Format each pair as a separate JSONL object (one per line) using the following structure:
{
  "contents": [
    {"role": "user", "parts": [{"text": "user input or question"}]},
    {"role": "model", "parts": [{"text": "AI/model reply"}]}
  ]
}
4. If the input text is in a specific language or dialect, maintain its original form unless otherwise instructed.
5. Clean the data by removing unnecessary characters, special symbols, excessive punctuation, irrelevant metadata, or any non-textual elements.
6. Standardize formatting and improve clarity, rewriting illogical or unclear text to be logical and coherent while preserving the original intent.
7. Enhance overall data quality by refining sentence structures and ensuring the text is natural and well-formed.
8. Optionally, split long and complex examples into multiple shorter, self-contained examples where logically feasible, ensuring each retains its meaning and context.

Goal: Output a .jsonl dataset that represents a high-quality dialogue/conversation fine-tuning corpus.
"""
    print("\nDefault system prompt:")
    print(system_prompt)
    if input("\nModify system prompt? (y/n): ").lower() == 'y':
        system_prompt = input("Enter your custom system prompt: ")
    input_filename = input("\nEnter the path to your input text file: ").strip()
    if not os.path.isfile(input_filename):
        print("File not found. Exiting.")
        return
    output_filename = f"gemini_output_{os.path.basename(input_filename)}.jsonl"
    output_path = os.path.join(os.path.dirname(input_filename), output_filename)
    print(f"\nProcessing {input_filename} with Gemini...")
    process_with_gemini(input_filename, output_path, api_key, system_prompt)
    print(f"\nProcessing complete! Output saved as: {output_path}")

if __name__ == "__main__":
    main()
