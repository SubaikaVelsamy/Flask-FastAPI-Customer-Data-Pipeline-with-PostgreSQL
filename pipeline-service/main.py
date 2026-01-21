from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.customer import Base, Customer
from services.ingestion import fetch_and_upsert
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Pipeline")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    records = fetch_and_upsert(db)
    return {"status": "success", "records_processed": records}

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()
    return {
        "data": [c.__dict__ for c in customers],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer_id = str(customer_id)
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.__dict__
