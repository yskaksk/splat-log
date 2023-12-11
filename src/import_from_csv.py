import pandas as pd
import requests as r


API_HOST = "http://localhost:8000/api/v1"


def main():
    df = pd.read_csv("data/log.csv")
    for _, row in df.iterrows():
        mode = row['モード']
        rule = row['ルール']
        stage = row['ステージ']
        result = row['結果']
        r.post(f"{API_HOST}/battlelog", json={
            "mode": mode,
            "rule": rule,
            "stage": stage,
            "result": result
        })


if __name__ == "__main__":
    main()
