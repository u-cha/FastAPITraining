import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.models import User
from app.models.feedback import Feedback
from app.models.user import UserAgeResponse

app = FastAPI()

users = {1: "ana de armas",
         2: "paul gautier",
         3: "lenny kravitz",
         4: "hp baxxter",
         5: "morgen shtern", }

feedback_storage = {}


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, workers=1)
