import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Contact, Review

app = FastAPI(title="De Bessa Hair API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "De Bessa Hair API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', '✅ Connected')
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Contact form endpoint
@app.post("/contact")
def submit_contact(contact: Contact):
    try:
        inserted_id = create_document("contact", contact)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reviews endpoints
@app.get("/reviews", response_model=List[Review])
def list_reviews(limit: int = 10):
    try:
        docs = get_documents("review", {}, limit)
        # Normalize fields and defaults
        reviews: List[Review] = []
        for d in docs:
            reviews.append(Review(
                name=d.get("name", "Client"),
                rating=int(d.get("rating", 5)),
                comment=d.get("comment", ""),
                source=d.get("source"),
                locale=d.get("locale", "en"),
                date=d.get("date") or datetime.utcnow()
            ))
        return reviews
    except Exception as e:
        # Fallback: provide sample reviews if DB unavailable for demo
        return [
            Review(name="Sofia", rating=5, comment="Exceptional service and gorgeous extensions.", source="Google", locale="en", date=datetime.utcnow()),
            Review(name="María", rating=5, comment="Pelo precioso y trato de lujo.", source="Instagram", locale="es", date=datetime.utcnow()),
        ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
