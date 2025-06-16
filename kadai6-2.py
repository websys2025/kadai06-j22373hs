import requests
import pandas as pd

# =============================================
# 気象庁が提供する天気予報JSONデータを使用して、
# 千葉県の天気予報（本日・明日・明後日）を取得するプログラム
# エンドポイント: https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json
# 地方コード: 120000（東京地方）
# =============================================

API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json"

# APIリクエスト送信
response = requests.get(API_URL)
data = response.json()

# ================================
# JSONから必要なデータを抽出
# ================================

# 地域名の取得（例: 東京地方）
area_name = data[0]["timeSeries"][0]["areas"][0]["area"]["name"]

# 日時と天気の取得
time_defines = data[0]["timeSeries"][0]["timeDefines"]
weather_list = data[0]["timeSeries"][0]["areas"][0]["weathers"]

# DataFrameに変換
df = pd.DataFrame({
    "日付": time_defines,
    "天気": weather_list
})

# 地域名を表示
print(f"【{area_name}の天気予報】")
print(df)
