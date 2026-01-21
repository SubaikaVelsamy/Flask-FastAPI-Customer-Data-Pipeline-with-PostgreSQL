import requests
from sqlalchemy.orm import Session
from models.customer import Customer
from datetime import datetime

FLASK_URL = "http://mock-server:5000/customers"  # Docker internal hostname

def fetch_and_upsert(db: Session):
    page = 1
    limit = 10
    total_processed = 0

    while True:
        resp = requests.get(f"{FLASK_URL}?page={page}&limit={limit}")
        if resp.status_code != 200:
            break
        data = resp.json().get("data", [])
        if not data:
            break

        for c in data:
            customer_id_str = str(c["customer_id"])
            customer = db.query(Customer).filter_by(customer_id=customer_id_str).first()
            if not customer:
                customer = Customer(customer_id=c["customer_id"])
            # Update fields
            customer.first_name = c["first_name"]
            customer.last_name = c["last_name"]
            customer.email = c["email"]
            customer.phone = c.get("phone")
            customer.address = c.get("address")
            customer.date_of_birth = datetime.fromisoformat(c["date_of_birth"]).date()
            customer.account_balance = c.get("account_balance")
            customer.created_at = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
            db.add(customer)
            total_processed += 1

        db.commit()
        page += 1

    return total_processed
