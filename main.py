import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import scipy.stats as stats

# パラメータ
n = 20000  # 回転数
alpha = 0.05  # 有意水準
hit_num = 160 # 大当たり回数
sample_proportion = hit_num / n # 合算確率

# ウィルソンのスコア区間の計算
z = stats.norm.ppf(1 - alpha / 2)
phat = sample_proportion
ci_lower = (phat + z**2 / (2*n) - z * np.sqrt((phat*(1-phat) + z**2 / (4*n)) / n)) / (1 + z**2 / n)
ci_upper = (phat + z**2 / (2*n) + z * np.sqrt((phat*(1-phat) + z**2 / (4*n)) / n)) / (1 + z**2 / n)

# 結果の表示
print(f"95%信頼区間: [{ci_lower}, {ci_upper}]")

# 数直線のデータを生成
data = pd.DataFrame({'x': [i for i in range(200, 101, -1)]})
data['x'] = 1 / data['x']

# 特定の値に縦の実線を引くためのデータ
vlines_data = pd.DataFrame({
    'x': [1/163.8, 1/159.1, 1/148.6, 1/135.2, 1/126.8, 1/114.6],
    'color': ['red'] * 6,
    'number': [1, 2, 3, 4, 5, 6]
})

# 点線を引くための任意の数値を追加（例として1/150を使用）
dotted_lines_data = pd.DataFrame({
    'x': [ci_lower, ci_upper],
    'y': [100, 100],
    'color': ['blue']*2
})

# 数直線のチャートを作成
line_chart = alt.Chart(data).mark_line(color='gray').encode(
    x=alt.X('x', scale=alt.Scale(domain=(1/200, 1/100)))
)

# 縦の実線を追加
vlines = alt.Chart(vlines_data).mark_rule(color='red').encode(
    x='x:Q',
)

# 縦の点線を追加
dotted_lines = alt.Chart(dotted_lines_data).mark_rule(color='blue', strokeDash=[5, 5]).encode(
    x='x:Q',
)

# 区間を色付け
area = alt.Chart(dotted_lines_data).mark_area(color='lightblue',opacity=0.2).encode(
    x='x:Q',
    y='y:Q'
)

# 番号のテキストを追加
text = alt.Chart(vlines_data).mark_text(
    align='center',
    baseline='top',
    dy=65  # テキストの位置を調整
).encode(
    x='x:Q',
    text='number:N'  # 番号を表示
)

# チャートを合成して表示
chart = (line_chart + vlines + dotted_lines + area + text).properties(
    height=200
)

st.altair_chart(chart,use_container_width=True)
