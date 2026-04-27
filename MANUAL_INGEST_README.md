# Manual PDF Ingestion

This script allows you to add PDF documents directly to the FAQ Chatbot system without using the web interface.

## Prerequisites

1. **Activate Virtual Environment:**
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

2. **Ensure Database is Running:**
   Make sure PostgreSQL is running and the database is set up.

3. **Valid API Key:**
   Make sure you have a valid OpenAI API key in your `.env` file.

## Usage

```bash
python manual_ingest.py <pdf_file_path> [optional_title]
```

### Examples

```bash
# Basic usage with auto-generated title
python manual_ingest.py my_document.pdf

# With custom title
python manual_ingest.py my_document.pdf "My Important Document"

# With full path
python manual_ingest.py "C:\Users\HP\Desktop\my_document.pdf" "Desktop Document"
```

## What it does

1. **Text Extraction:** Uses OCR to extract text from the PDF
2. **Text Chunking:** Splits the text into manageable chunks
3. **Embedding Generation:** Creates vector embeddings using OpenAI
4. **Database Storage:** Saves document metadata to PostgreSQL
5. **Vector Store:** Adds embeddings to FAISS for similarity search

## Output

The script will show:
- Processing status
- Number of characters extracted
- Document title and ID
- Number of chunks created
- File path where saved

## Troubleshooting

- **Module not found:** Make sure virtual environment is activated
- **Database connection error:** Ensure PostgreSQL is running
- **API key error:** Check your OpenAI API key in `.env`
- **No text extracted:** PDF might be image-only or corrupted
- **Tesseract error:** Ensure Tesseract is installed

## Notes

- The script creates an admin user if one doesn't exist
- Documents are associated with `admin@example.com`
- The original PDF is copied to the uploads directory
- Processing may take time for large documents