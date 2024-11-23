from PyPDF2 import PdfReader, PdfWriter
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.post("/encrypt")
async def encrypt_pdf(password: str = Form(...), file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .pdf files are allowed.")

    try:
        file_data = await file.read()
        reader = PdfReader(io.BytesIO(file_data))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_pdf = io.BytesIO()
        writer.encrypt(user_password=password)
        writer.write(output_pdf)
        output_pdf.seek(0)

        return StreamingResponse(
            output_pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=encrypted_{file.filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
