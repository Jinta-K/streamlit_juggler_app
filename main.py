import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import scipy.stats as stats

import streamlit as st

st.set_page_config(
    page_title="MY Juggler App",
    page_icon="🤡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# CSSファイルの読み込み
with open("style.css") as f:
    style = f.read()
    st.markdown(f"<style>{style}</style>",unsafe_allow_html=True)


# タイトルの追加
st.title("MY Juggler App")
# 3つの入力フォームを縦に並べる
with st.form("my_form"):
    game_num = st.number_input("Games", 0, key="game_num_form")
    big_bonus_num = st.number_input("Big Bonus", 0, key="big_bonus_form")
    regular_bonus_num = st.number_input("Regular Bonus", 0, key="regular_bonus_form")
    # フォームの送信ボタン
    submitted = st.form_submit_button(label="実行")

# 入力フォームの下にタブビューを作成
tab1, tab2 = st.tabs(["Expected Value", "Probability"])

with tab1:
    st.write("これはタブ1の内容です。")
    st.write(f"入力フォーム1の値: {game_num}")
with tab2:
    st.write("これはタブ2の内容です。")
    st.write("タブ2に別の表示内容を追加できます。")
