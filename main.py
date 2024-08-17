import uvicorn
from fastapi import FastAPI

from apps.hello.router import router as hello_router

app = FastAPI()
app.include_router(hello_router, prefix="/hello", tags=["hello"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
