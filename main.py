from PyPDF2 import PdfReader, PdfWriter
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
import shutil

app = FastAPI()

OUTPUT_DIR = "./encrypted_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/encrypt")
async def encrypt_pdf(password: str = Form(...), file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .pdf files are allowed.")

    # Secure the filename and prepare paths
    filename = file.filename
    temp_dir = tempfile.mkdtemp()
    temp_input_path = os.path.join(temp_dir, filename)
    encrypted_filename = f"encrypted_{filename}"
    encrypted_file_path = os.path.join(OUTPUT_DIR, encrypted_filename)

    try:
        # Save the uploaded file temporarily
        with open(temp_input_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Read and encrypt the PDF
        reader = PdfReader(temp_input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Set encryption
        writer.encrypt(user_password=password)

        # Save the encrypted PDF
        with open(encrypted_file_path, "wb") as encrypted_file:
            writer.write(encrypted_file)

        # Return the encrypted PDF as a response
        return FileResponse(
            encrypted_file_path,
            media_type="application/pdf",
            filename=encrypted_filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # Clean up temporary files
        shutil.rmtree(temp_dir)
