import uvicorn
from core import create_app, get_config

app = create_app(get_config())

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
