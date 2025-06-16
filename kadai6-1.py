import requests
import pandas as pd

# =============================================
# e-Stat APIを使用して「婚姻件数（全国・年次・夫）」を取得するプログラム
# 統計表ID: 0003411954（婚姻に関する統計）
# 初婚・再婚（cdCat02）: 初婚・再婚
# 性別（cdCat03）: 夫
# 年齢（cdCat04）: 総数
# エリア: 全国（固定のため省略）
# =============================================

APP_ID = "3aaf2d3e893db77e589a9b948718cd0432547cbd"
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,
    "statsDataId": "0003411954",   # 婚姻件数統計
    "cdCat02": "00100",            # 夫
    "cdCat03": "00110",            # 調査年
    "cdCat04": "00100",            # 年齢：総数
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"
}

# APIリクエスト送信
response = requests.get(API_URL, params=params)
data = response.json()

# =====================
# JSONから必要なデータ抽出
# =====================
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# pandasのDataFrameに変換
df = pd.DataFrame(values)

# メタ情報からコード変換辞書を作成し、IDを名前に置換
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名をわかりやすく変換
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    col_replace_dict['@' + class_obj['@id']] = class_obj['@name']

df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 結果表示
print(df)
