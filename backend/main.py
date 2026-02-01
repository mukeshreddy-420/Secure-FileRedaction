from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
import os
import traceback

from auth import router as auth_router
from database import cursor, conn
from redact_pdf import redact_pdf
from redact_image import redact_image
from redact_word import redact_word
from redact_excel import redact_excel

# ------------------ APP SETUP ------------------

app = FastAPI(title="File Redaction System API", version="1.0.0")

# Serve uploaded/redacted files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# CORS - Allow all origins for development/deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes
app.include_router(auth_router, prefix="/auth")

# Health check endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "File Redaction System API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "file-redaction-api"}

# ------------------ UPLOAD & REDACTION ------------------

@app.post("/upload/{file_type}")
async def upload(
    file_type: str,
    email: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        if file_type not in ["pdf", "image", "word", "excel"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        input_path = f"{UPLOAD_DIR}/{file.filename}"
        output_path = f"{UPLOAD_DIR}/redacted_{file.filename}"

        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Redaction logic
        if file_type == "pdf":
            redact_pdf(input_path, output_path)
        elif file_type == "image":
            redact_image(input_path, output_path)
        elif file_type == "word":
            redact_word(input_path, output_path)
        elif file_type == "excel":
            redact_excel(input_path, output_path)

        # Save history to database
        cursor.execute(
            "INSERT INTO downloads (user_email, filename) VALUES (?, ?)",
            (email, output_path),
        )
        conn.commit()

        return {"download": output_path}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Redaction failed: {str(e)}")

# ------------------ HISTORY ------------------

@app.get("/history/{email}")
def history(email: str):
    try:
        cursor.execute(
            "SELECT filename, created_at FROM downloads WHERE user_email=?",
            (email,),
        )
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------ DELETE ALL HISTORY (OPTIONAL) ------------------

@app.delete("/history/{email}")
def delete_all_history(email: str):
    try:
        cursor.execute(
            "SELECT filename FROM downloads WHERE user_email=?",
            (email,),
        )
        files = cursor.fetchall()

        for (filename,) in files:
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception as e:
                    print(f"Failed to delete file {filename}: {e}")

        cursor.execute(
            "DELETE FROM downloads WHERE user_email=?",
            (email,),
        )
        conn.commit()

        return {"message": "All download history deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------ DELETE SINGLE HISTORY ITEM ------------------

@app.delete("/history/item")
def delete_history_item(
    email: str = Query(...),
    filename: str = Query(...)
):
    try:
        # Delete database record
        cursor.execute(
            "DELETE FROM downloads WHERE user_email=? AND filename=?",
            (email, filename),
        )
        conn.commit()

        # Delete file from disk
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Failed to delete file {filename}: {e}")

        return {"message": "History item deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------ STARTUP ------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
