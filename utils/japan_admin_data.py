import os
import pandas as pd

japanadmincode_fn = os.path.join("data", "japanadmincode.csv")
if os.path.exists(japanadmincode_fn):
    japanadmincode = pd.read_csv(japanadmincode_fn)
    japanadmincode = (
        japanadmincode[japanadmincode.cat.isin(["1", "2", "3"])]
        .rename(columns={"prefname": "pref", "muniname": "muni"})
        .set_index(["pref", "muni"])
    )
    japanadmincode = japanadmincode.reset_index()
    japanadmin_muni_jp_to_en = japanadmincode.set_index("muni")["en"].to_dict()

else:
    japanadmincode = None

if os.path.exists(japanadmincode_fn):
    japanadmincode_all = pd.read_csv(japanadmincode_fn)
    japanadmincode_all = (
        japanadmincode_all[japanadmincode_all.cat.isin(["0", "1", "2", "3"])]
        .rename(columns={"prefname": "pref", "muniname": "muni"})
        .set_index(["pref", "muni"])
    )
    japanadmincode_all = japanadmincode_all.reset_index()
    japanadmin_muni_all_jp_to_en = japanadmincode_all.set_index("muni")["en"].to_dict()

else:
    japanadmincode_all = None

tokyo_wards = [
    "千代田区",
    "中央区",
    "港区",
    "新宿区",
    "文京区",
    "台東区",
    "墨田区",
    "江東区",
    "品川区",
    "目黒区",
    "大田区",
    "世田谷区",
    "渋谷区",
    "中野区",
    "杉並区",
    "豊島区",
    "北区",
    "荒川区",
    "板橋区",
    "練馬区",
    "足立区",
    "葛飾区",
    "江戸川区",
]

prefecture_dict = {
    1: "北海道",
    2: "青森県",
    3: "岩手県",
    4: "宮城県",
    5: "秋田県",
    6: "山形県",
    7: "福島県",
    8: "茨城県",
    9: "栃木県",
    10: "群馬県",
    11: "埼玉県",
    12: "千葉県",
    13: "東京都",
    14: "神奈川県",
    15: "新潟県",
    16: "富山県",
    17: "石川県",
    18: "福井県",
    19: "山梨県",
    20: "長野県",
    21: "岐阜県",
    22: "静岡県",
    23: "愛知県",
    24: "三重県",
    25: "滋賀県",
    26: "京都府",
    27: "大阪府",
    28: "兵庫県",
    29: "奈良県",
    30: "和歌山県",
    31: "鳥取県",
    32: "島根県",
    33: "岡山県",
    34: "広島県",
    35: "山口県",
    36: "徳島県",
    37: "香川県",
    38: "愛媛県",
    39: "高知県",
    40: "福岡県",
    41: "佐賀県",
    42: "長崎県",
    43: "熊本県",
    44: "大分県",
    45: "宮崎県",
    46: "鹿児島県",
    47: "沖縄県",
}

prefecture_dict_en = {
    1: "Hokkaido",
    2: "Aomori",
    3: "Iwate",
    4: "Miyagi",
    5: "Akita",
    6: "Yamagata",
    7: "Fukushima",
    8: "Ibaraki",
    9: "Tochigi",
    10: "Gunma",
    11: "Saitama",
    12: "Chiba",
    13: "Tokyo",
    14: "Kanagawa",
    15: "Niigata",
    16: "Toyama",
    17: "Ishikawa",
    18: "Fukui",
    19: "Yamanashi",
    20: "Nagano",
    21: "Gifu",
    22: "Shizuoka",
    23: "Aichi",
    24: "Mie",
    25: "Shiga",
    26: "Kyoto",
    27: "Osaka",
    28: "Hyogo",
    29: "Nara",
    30: "Wakayama",
    31: "Tottori",
    32: "Shimane",
    33: "Okayama",
    34: "Hiroshima",
    35: "Yamaguchi",
    36: "Tokushima",
    37: "Kagawa",
    38: "Ehime",
    39: "Kochi",
    40: "Fukuoka",
    41: "Saga",
    42: "Nagasaki",
    43: "Kumamoto",
    44: "Oita",
    45: "Miyazaki",
    46: "Kagoshima",
    47: "Okinawa",
}

prefecture_dict_en_r = {v: k for k, v in prefecture_dict_en.items()}
prefecture_dict_r = {v: k for k, v in prefecture_dict.items()}
prefecture_dict_jp_to_en = {
    k: prefecture_dict_en.get(v, v) for k, v in prefecture_dict_r.items()
}
prefecture_dict_en_to_jp = {v: k for k, v in prefecture_dict_jp_to_en.items()}
prefecture_dict_en_to_no = {
    pref: prefecture_dict_r.get(prefecture_dict_en_to_jp.get(pref))
    for pref in prefecture_dict_en_to_jp.keys()
}
prefecture_dict_no_to_en = {v: k for k, v in prefecture_dict_en_to_no.items()}
