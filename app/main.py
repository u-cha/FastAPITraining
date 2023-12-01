from typing import List, Optional
import re

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.models import User
from app.models.feedback import Feedback
from app.models.product import Product
from app.models.user import UserAgeResponse, UserCreate

app = FastAPI()

users = {1: "ana de armas",
         2: "paul gautier",
         3: "lenny kravitz",
         4: "hp baxxter",
         5: "morgen shtern", }

users_extended: List[UserCreate] = []

feedback_storage = {}

products = {1: Product(product_id=1, name="Smartphone", category="Electronics", price=223.1),
            2: Product(product_id=2, name="Smartphone", category="Electronics", price=333.1),}


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/user/{user_id}")
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        return {"error": f"user with id {user_id} not found"}
    return {user_id: user}


@app.get("/users/")
def get_users(limit: int = 0):
    return dict(list(users.items())[:limit]) if limit else users


@app.get("/file/")
async def get_file():
    headers = {"Content-Disposition": "attachment; filename=index.html"}
    return FileResponse("response.html", headers=headers)


@app.post("/feedback/")
async def post_feedback(feedback: Feedback):
    feedback_storage[feedback.name] = feedback.message
    return {"message": f"Thank you, {feedback.name}, for your response"}


@app.get("/feedback/{user_name}")
async def get_feedback(user_name: str):
    return {user_name: feedback_storage.get(user_name, "hasn't submitted feedback this far")}


@app.get("/multiply")
async def multiply(num1: int, num2: int):
    return {"result": num1 * num2}


@app.post("/check_user_age")
async def check_user_age(usr: User):
    return UserAgeResponse(**usr.model_dump())


@app.post("/create_user")
async def create_user(user: UserCreate):
    users_extended.append(user)
    return user


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    return products.get(product_id, {"error": f"no product with id {product_id}"})


@app.get("/products/search/")
async def search_product(keyword: str, category: Optional[str] = None, limit: int = 10):
    product_list = products.values()
    filtered_list = list(filter(lambda p: re.search(keyword.lower(), p.name.lower()), product_list))
    if category:
        filtered_list = list(filter(lambda p: re.match(category, p.category), filtered_list))
    if limit:
        filtered_list = filtered_list[:limit]
    return filtered_list

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, workers=1)
