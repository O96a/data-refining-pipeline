# Gemini Data Refining Pipeline

This project is a Python-based, flexible, and extensible tool for transforming raw conversational data (TXT, PDF, DOCX) into high-quality JSONL datasets for fine-tuning large language models (LLMs).

## Features
- **Multi-format Input:** Supports `.txt`, `.pdf`, and `.docx` files.
- **Automated Chunking:** Segments long texts into coherent conversational pairs.
- **Customizable Prompt:** Easily modify the system prompt for your use case.
- **Error Handling:** Robust error reporting for each chunk.
- **Modern Pythonic CLI:** Simple, interactive command-line interface.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/O96a/data-refining-pipeline.git
   cd data-refining-pipeline
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the tool:
   ```sh
   python main.py
   ```
2. Follow the prompts:
   - Enter your Google AI Studio API key.
   - (Optionally) Edit the system prompt.
   - Enter the path to your input file (`.txt`, `.pdf`, or `.docx`).

3. The output will be saved as a `.jsonl` file in the same directory as your input file.

## Example

```
Enter your Google AI Studio API key: <your-api-key>
Modify system prompt? (y/n): n
Enter the path to your input text file: dataset_samples.txt
Processing dataset_samples.txt with Gemini...
Processed: ...
Processing complete! Output saved as: gemini_output_dataset_samples.txt.jsonl
```

## System Prompt Customization
You can fully customize the system prompt to fit your data cleaning, translation, or formatting needs. The default prompt is designed for general conversational data refinement.

## File Support
- `.txt`: Standard UTF-8 text files.
- `.pdf`: Extracts text from all pages.
- `.docx`: Extracts text from all paragraphs.

## Contributing
Contributions, issues, and feature requests are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
