import gradio as gr

import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from scipy.stats import binomtest
import requests as r


API_HOST = "http://localhost:8000/api/v1"


def aggregate_result(group):
    total = group.size
    win = group[group == "勝ち"].size
    lose = group[group == "負け"].size
    ci = binomtest(win, total, 0.5).proportion_ci(confidence_level=0.95)
    win_rate = win / total
    return pd.Series({
        'wins': win,
        'loses': lose,
        'win_rate': win_rate,
        'ci.low': ci.low,
        'ci.high': ci.high,
        'mean': (ci.low + ci.high) / 2,
    })


def result_summary(df, by):
    return df.groupby(by)['結果'].apply(aggregate_result).unstack().sort_values(by='mean')


def win_rate_ci(df):
    df = df[::-1]
    lower_err = df['mean'] - df['ci.low']
    upper_err = df['ci.high'] - df['mean']
    fig, ax = plt.subplots()
    ax.errorbar(x=df['mean'], y=df.index, xerr=[lower_err, upper_err], fmt='o', linewidth=2, capsize=6)
    ax.set(xlim=(0.0, 1.0))
    ax.grid()
    plt.tight_layout()
    return fig


with gr.Blocks() as blocks:
    gr.Button("top", link="/top")
    submit_btn = gr.Button('集計', variant='primary')
    with gr.Row():
        winrate_by_rule = gr.Plot(label='ルール別勝率')
        winrate_by_mode = gr.Plot(label='モード別勝率')
    header_stage = ['ステージ', 'wins', 'loses', 'win_rate', 'ci.low', 'ci.high', 'mean']
    header_rule = ['ルール', 'wins', 'loses', 'win_rate', 'ci.low', 'ci.high', 'mean']
    with gr.Row():
        winrate_by_stage = gr.Plot(label='ステージ別勝率')
        winrate_by_stage_df = gr.DataFrame(
            label='ステージ別勝率',
            headers=header_stage,
        )
    with gr.Row():
        winrate_by_xrule = gr.Plot(label='Xマッチルール別勝率')
        winrate_by_xrule_df = gr.DataFrame(
            label='Xマッチルール別勝率',
            headers=header_rule,
        )
    with gr.Row():
        winrate_by_stage_tw = gr.Plot(label='ナワバリステージ別勝率')
        winrate_by_stage_tw_df = gr.DataFrame(
            label='ナワバリステージ別勝率',
            headers=header_stage,
        )
    with gr.Row():
        winrate_by_stage_sz = gr.Plot(label='ガチエリアステージ別勝率')
        winrate_by_stage_sz_df = gr.DataFrame(
            label='ガチエリアステージ別勝率',
            headers=header_stage,
        )
    with gr.Row():
        winrate_by_stage_tc = gr.Plot(label='ガチヤグラステージ別勝率')
        winrate_by_stage_tc_df = gr.DataFrame(
            label='ガチヤグラステージ別勝率',
            headers=header_stage,
        )
    with gr.Row():
        winrate_by_stage_rm = gr.Plot(label='ガチホコバトルステージ別勝率')
        winrate_by_stage_rm_df = gr.DataFrame(
            label='ガチホコバトルステージ別勝率',
            headers=header_stage,
        )
    with gr.Row():
        winrate_by_stage_cb = gr.Plot(label='ガチアサリステージ別勝率')
        winrate_by_stage_cb_df = gr.DataFrame(
            label='ガチアサリステージ別勝率',
            headers=header_stage,
        )

    @submit_btn.click(
        inputs=[],
        outputs=[
            winrate_by_rule, winrate_by_mode, winrate_by_stage,
            winrate_by_xrule, winrate_by_stage_tw, winrate_by_stage_sz,
            winrate_by_stage_tc, winrate_by_stage_rm, winrate_by_stage_cb,
            winrate_by_stage_df, winrate_by_xrule_df, winrate_by_stage_tw_df,
            winrate_by_stage_sz_df, winrate_by_stage_tc_df,
            winrate_by_stage_rm_df, winrate_by_stage_cb_df
        ]
    )
    def handle_submit():
        df = pd.DataFrame(
            r.get(f"{API_HOST}/battlelog").json(),
            columns=['mode', 'rule', 'stage', 'result', 'created_at']
        )
        df.columns = ['モード', 'ルール', 'ステージ', '結果', 'タイムスタンプ']

        rule = result_summary(df, 'ルール')
        mode = result_summary(df, 'モード')
        stage = result_summary(df, 'ステージ')
        xrule = result_summary(df[df['モード'] == 'Xマッチ'], 'ルール')
        stage_tw = result_summary(df[df['ルール'] == 'ナワバリバトル'], 'ステージ')
        stage_sz = result_summary(df[df['ルール'] == 'ガチエリア'], 'ステージ')
        stage_tc = result_summary(df[df['ルール'] == 'ガチヤグラ'], 'ステージ')
        stage_rm = result_summary(df[df['ルール'] == 'ガチホコバトル'], 'ステージ')
        stage_cb = result_summary(df[df['ルール'] == 'ガチアサリ'], 'ステージ')
        return (
            gr.Plot(win_rate_ci(rule), label='ルール別勝率'),
            gr.Plot(win_rate_ci(mode), label='モード別勝率'),
            gr.Plot(win_rate_ci(stage), label='ステージ別勝率'),
            gr.Plot(win_rate_ci(xrule), label='Xマッチルール別勝率'),
            gr.Plot(win_rate_ci(stage_tw), label='ナワバリステージ別勝率'),
            gr.Plot(win_rate_ci(stage_sz), label='ガチエリアステージ別勝率'),
            gr.Plot(win_rate_ci(stage_tc), label='ガチヤグラステージ別勝率'),
            gr.Plot(win_rate_ci(stage_rm), label='ガチホコバトルステージ別勝率'),
            gr.Plot(win_rate_ci(stage_cb), label='ガチアサリステージ別勝率'),
            gr.DataFrame(stage.reset_index(), label='ステージ別勝率'),
            gr.DataFrame(xrule.reset_index(), label='Xマッチルール別勝率'),
            gr.DataFrame(stage_tw.reset_index(), label='ナワバリステージ別勝率'),
            gr.DataFrame(stage_sz.reset_index(), label='ガチエリアステージ別勝率'),
            gr.DataFrame(stage_tc.reset_index(), label='ガチヤグラステージ別勝率'),
            gr.DataFrame(stage_rm.reset_index(), label='ガチホコバトルステージ別勝率'),
            gr.DataFrame(stage_cb.reset_index(), label='ガチアサリステージ別勝率'),
        )
