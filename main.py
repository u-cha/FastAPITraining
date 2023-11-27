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
