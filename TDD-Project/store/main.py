from ast import arg
from fastapi import FastAPI
from core.config import Settings
from store.routers import api_router

class APP(FastAPI):
    def __init__(self: *arg, **kwargs) -> None: # type: ignore
        super().__init__(
            *arg, 
            **kwargs, 
            version="0.0.1",
            title = Settings.PROJECT_NAME,
            root_path=Settings.ROOT_PATH
        )

app = APP()
app.include_router(api_router)