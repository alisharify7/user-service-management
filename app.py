import uvicorn
from core import app


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, workers=2, port=8888)
