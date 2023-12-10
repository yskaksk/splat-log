import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gradio as gr
import pandas as pd
import requests as r

from src.enum import Rule, Mode, Stage, Result

DATA_DIR = "data"
LOG_FILE = "log.csv"
API_HOST = "http://localhost:8000/api/v1"

with gr.Blocks() as blocks:
    with gr.Row():
        gr.Button("ダッシュボード", link="/dashboard")
        #gr.Button("Xパワー", link="/xpower")
    mode = gr.Radio(
            label="モード",
            choices=[m.value for m in Mode],
    )
    rule = gr.Radio(
            label="ルール",
            choices=[m.value for m in Rule],
    )
    stage = gr.Dropdown(
            label="ステージ",
            choices=[m.value for m in Stage],
    )
    result = gr.Radio(
            label="結果",
            choices=[m.value for m in Result],
    )

    submit_btn = gr.Button("登録", variant="primary")

    columns = ["mode", "rule", "stage", "result", "created_at"]
    latest = gr.DataFrame(
        label="最新の戦績",
        headers=columns,
        value=pd.DataFrame(columns=columns),
    )

    #@submit_btn.click(
    #    inputs=[mode, rule, stage, result],
    #    outputs=[latest],
    #)
    def add_record(mode, rule, stage, result):
        res = r.post(f"{API_HOST}/battlelog", json={
            "mode": mode,
            "rule": rule,
            "stage": stage,
            "result": result
        })
        if res.status_code == 400:
            raise gr.Error("登録できませんでした")
        logs = r.get(f"{API_HOST}/battlelog").json()
        latest = pd.DataFrame(logs, columns=columns)
        return latest

    submit_btn.click(
        add_record,
        inputs=[mode, rule, stage, result],
        outputs=[latest],
    ).success(None, _js="window.alert('登録しました')")
