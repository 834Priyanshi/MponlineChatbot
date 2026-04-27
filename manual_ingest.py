#!/usr/bin/env python3
"""
Manual PDF ingestion script for FAQ Chatbot.
This script allows you to add a PDF document directly to the system without using the API.

Usage: python manual_ingest.py <pdf_path> [title]
Example: python manual_ingest.py my_document.pdf "My Document Title"

Make sure to activate the virtual environment first:
.\\venv\\Scripts\\Activate.ps1
"""

import os
import sys
from pathlib import Path
from io import BytesIO

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(app_dir))

# Only import what's needed at top level
from app.services.ocr_service import extract_text


class MockUploadFile:
    """Mock UploadFile for manual ingestion"""
    def __init__(self, file_path: str):
        self.filename = Path(file_path).name
        self.file_path = file_path
        with open(file_path, "rb") as f:
            self.file = BytesIO(f.read())


def manual_ingest_pdf(pdf_path: str, user_email: str = "admin@example.com", title: str = None):
    """
    Manually ingest a PDF document into the system.

    Args:
        pdf_path: Path to the PDF file
        user_email: Email of the user to associate with the document
        title: Optional custom title for the document
    """
    # Import here to avoid top-level database connections
    from sqlalchemy.orm import Session
    from app.config import get_settings
    from app.database import get_db
    from app.models.entities import User
    from app.services.document_service import ingest_document
    from app.services.ocr_service import extract_text

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return False

    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: File must be a PDF. Got: '{pdf_path}' (ends with: '{pdf_path[-4:]}')")
        return False

    # Get database session
    db: Session = next(get_db())

    try:
        # Find or create user
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            print(f"Creating user: {user_email}")
            user = User(
                email=user_email,
                full_name="Admin User",
                hashed_password="dummy",  # Not used for manual ingestion
                is_active=True,
                is_admin=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Create mock upload file
        mock_file = MockUploadFile(pdf_path)

        print(f"Processing PDF: {pdf_path}")
        print("Extracting text...")

        # Test text extraction first
        extracted_text = extract_text(pdf_path)
        if not extracted_text:
            print("Error: No text could be extracted from the PDF")
            return False

        print(f"Extracted {len(extracted_text)} characters of text")

        # Ingest the document
        print("Generating embeddings and saving to database...")
        document = ingest_document(db, mock_file, user, title)

        print("✅ PDF successfully ingested!")
        print(f"Title: {document.title}")
        print(f"ID: {document.id}")
        print(f"Chunks: {document.chunk_count}")
        print(f"File: {document.file_path}")

        return True

    except Exception as e:
        print(f"Error during ingestion: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python manual_ingest.py <pdf_path> [title]")
        print("Example: python manual_ingest.py my_document.pdf \"My Document Title\"")
        sys.exit(1)

    pdf_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None

    print("Manual PDF Ingestion Tool")
    print("=" * 40)

    success = manual_ingest_pdf(pdf_path, title=title)

    if success:
        print("\nDocument added successfully! You can now query it through the chatbot.")
    else:
        print("\nFailed to add document. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()