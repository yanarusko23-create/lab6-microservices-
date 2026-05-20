import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

STUDENT_N = int(os.getenv("STUDENT_N", 15))

app = FastAPI(title=f"Order Service N{STUDENT_N}")

# Звернення до product-service по імені в Docker-мережі
PRODUCT_SERVICE_URL = "http://product-service-15:8000"

ORDERS = []


class OrderRequest(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders")
def create_order(order: OrderRequest):
    """Створює замовлення після перевірки товару в Product Service"""

    # 1. Запит до Product Service
    try:
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Product Service is unavailable"
        )

    # 2. Чи існує товар?
    if response.status_code == 404:
        raise HTTPException(
            status_code=400,
            detail="Product does not exist"
        )

    payload = response.json()
    product_data = payload["data"]

    # 3. Чи є на складі?
    if product_data["stock"] < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock for this product"
        )

    # 4. Створення замовлення
    new_order = {
        "order_id": len(ORDERS) + 1,
        "student_id": STUDENT_N,
        "product_id": order.product_id,
        "product_name": product_data["name"],
        "quantity": order.quantity,
        "total_price": product_data["price"] * order.quantity,
        "status": "Created"
    }
    ORDERS.append(new_order)
    return new_order


@app.get("/orders")
def get_all_orders():
    """Повертає список усіх замовлень"""
    return {
        "student_id": STUDENT_N,
        "orders": ORDERS
    }
