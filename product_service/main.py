import os
from fastapi import FastAPI, HTTPException

STUDENT_N = int(os.getenv("STUDENT_N", 15))

app = FastAPI(title=f"Product Service N{STUDENT_N}")

# ID товарів починаються з 100 * N = 1500
PRODUCTS = {
    STUDENT_N * 100 + 1: {
        "id": STUDENT_N * 100 + 1,
        "name": "Ноутбук Dell XPS",
        "price": 1500.0,
        "stock": 10
    },
    STUDENT_N * 100 + 2: {
        "id": STUDENT_N * 100 + 2,
        "name": "Мишка Logitech MX",
        "price": 45.0,
        "stock": 30
    },
    STUDENT_N * 100 + 3: {
        "id": STUDENT_N * 100 + 3,
        "name": "Клавіатура Keychron K2",
        "price": 120.0,
        "stock": 0
    },
}


@app.get("/products")
def get_all_products():
    """Повертає список усіх товарів"""
    return {
        "student_id": STUDENT_N,
        "products": list(PRODUCTS.values())
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """Повертає товар за ID"""
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    product = PRODUCTS[product_id]
    return {
        "student_id": STUDENT_N,
        "data": product
    }
