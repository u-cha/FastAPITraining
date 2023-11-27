import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/file/")
async def file():
    headers = {"Content-Disposition": "attachment; filename=index.html"}
    return FileResponse("response.html", headers=headers)


@app.get("/multiply")
async def multiply(num1: int, num2: int):
    return {"result": num1 * num2}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, workers=1)
