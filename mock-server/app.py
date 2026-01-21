from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "customers.json")

def load_customers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.route("/customers", methods=["GET"])
def get_customers():
    customers = load_customers()

    # Pagination params
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    paginated_customers = customers[start:end]

    return jsonify({
        "data": paginated_customers,
        "total": len(customers),
        "page": page,
        "limit": limit
    })

@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customers = load_customers()
    customer = next((c for c in customers if c["customer_id"] == customer_id), None)

    if not customer:
        abort(404, description="Customer not found")

    return jsonify(customer)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
