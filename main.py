import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from apps.hello.router import router as hello_router
from apps.video.router import router as video_router

app = FastAPI()
add_pagination(app)

app.include_router(hello_router, prefix="/hello", tags=["hello"])
app.include_router(video_router, prefix="/video", tags=["video"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
