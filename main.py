from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from gradio import mount_gradio_app

from src import top, dashboard, xpower
from src.routers import battlelog

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse("/top")


app.include_router(battlelog.router)
app = mount_gradio_app(app, top.blocks, path="/top")
app = mount_gradio_app(app, dashboard.blocks, path="/dashboard")
#app = mount_gradio_app(app, xpower.blocks, path="/xpower")
