import altair as alt
import pandas as pd
import streamlit as st
import numpy as np
import scipy.stats as stats
from scipy.stats import geom
from scipy.integrate import quad
import yaml
from fractions import Fraction

import my_function

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

#機種名から機種コードに変換するための辞書
machine_series_code_dic = {"SアイムジャグラーEX-TP":"IAM","マイジャグラーV":"MY"}

#設定ファイルの読み込み
# YAMLファイルのパス
yaml_file_path = 'setting.yaml'

# YAMLファイルを読み込み、Pythonの辞書型に変換する
with open(yaml_file_path, 'r') as file:
    machine_setting_dic = yaml.safe_load(file)

# タイトルの追加
st.title("MY Juggler App")

# 入力フォームの上にタブビューを作成
tab1, tab2= st.tabs(["Expected Value", "Probability"])

with tab1:
    # 入力フォーム
    with st.form("my_form"):
        machine_series = st.selectbox("Series", ["SアイムジャグラーEX-TP","マイジャグラーV"], key="machine_series")
        game_num = st.number_input("Games", 0, key="game_num_form")
        big_bonus_num = st.number_input("Big Bonus", 0, key="big_bonus_form")
        regular_bonus_num = st.number_input("Regular Bonus", 0, key="regular_bonus_form")
        # フォームの送信ボタン
        submitted = st.form_submit_button(label="実行")

    # 台の設定
    machine_series_code = machine_series_code_dic[machine_series]
    # 各設定のBonus確率の真値
    true_probabilities_of_bb = [float(Fraction(value).limit_denominator()) for value in machine_setting_dic[machine_series_code]["BB"].values()]
    true_probabilities_of_rb = [float(Fraction(value).limit_denominator()) for value in machine_setting_dic[machine_series_code]["RB"].values()]
    # 各設定の出玉率
    expected_return = list(machine_setting_dic[machine_series_code]["E"].values())
    
    # 事前分布のパラメータは事前情報なしとする
    alpha_prior = 1.0
    beta_prior = 1.0

    # 事後分布のパラメータを計算
    alpha_post_of_bb = alpha_prior + big_bonus_num
    beta_post_of_bb = beta_prior + (game_num - big_bonus_num)
    alpha_post_of_rb = alpha_prior + regular_bonus_num
    beta_post_of_rb = beta_prior + (game_num - regular_bonus_num)

    # pの範囲
    p = np.linspace(0, 1, 10000)
    posterior_of_bb = stats.beta.pdf(p, alpha_post_of_bb, beta_post_of_bb)
    posterior_of_rb = stats.beta.pdf(p, alpha_post_of_rb, beta_post_of_rb)

    # データフレームの作成
    df = pd.DataFrame({
        'p': p,
        'Density_of_bb': posterior_of_bb,
        'Density_of_rb': posterior_of_rb
    })

    chart_of_bb = alt.Chart(df).mark_line(color='blue').encode(
        x=alt.X('p', title='Probability of Success (BB)', scale=alt.Scale(domain=[0.001, 0.008])),
        y=alt.Y('Density_of_bb', axis=alt.Axis(labels=False, title=None, grid=True))
    ).interactive()
    # 縦線のプロット
    vertical_lines_bb = alt.Chart(pd.DataFrame({'x': true_probabilities_of_bb})).mark_rule(color='red',strokeDash=[5, 5]).encode(
        x='x:Q'
    )
    chart_bb_with_lines = chart_of_bb + vertical_lines_bb

    chart_of_rb = alt.Chart(df).mark_line(color='blue').encode(
        x=alt.X('p', title='Probability of Success (RB)', scale=alt.Scale(domain=[0.001, 0.008])),
        y=alt.Y('Density_of_rb', axis=alt.Axis(labels=False, title=None, grid=True))
    ).interactive()
    vertical_lines_rb = alt.Chart(pd.DataFrame({'x': true_probabilities_of_rb})).mark_rule(color='red',strokeDash=[5, 5]).encode(
        x='x:Q'
    )
    chart_rb_with_lines = chart_of_rb + vertical_lines_rb

    if (alpha_post_of_rb + beta_post_of_rb - 2) != 0 and (alpha_post_of_bb + beta_post_of_bb - 2) != 0:
        # 各真値のベータ分布との重なり面積を計算
        overlap_areas_bb = []
        for p_true in true_probabilities_of_bb:
            alpha_true = p_true * (alpha_post_of_bb + beta_post_of_bb)
            beta_true = (1 - p_true) * (alpha_post_of_bb + beta_post_of_bb)
            
            beta_true_pdf = stats.beta(alpha_true, beta_true).pdf
            
            overlap_area, _ = quad(lambda p: np.minimum(stats.beta.pdf(p, alpha_post_of_bb, beta_post_of_bb), beta_true_pdf(p)), 0, 1)
            overlap_areas_bb.append(overlap_area)

        overlap_areas_rb = []
        for p_true in true_probabilities_of_rb:
            alpha_true = p_true * (alpha_post_of_rb + beta_post_of_rb)
            beta_true = (1 - p_true) * (alpha_post_of_rb + beta_post_of_rb)
            
            beta_true_pdf = stats.beta(alpha_true, beta_true).pdf
            
            overlap_area, _ = quad(lambda p: np.minimum(stats.beta.pdf(p, alpha_post_of_rb, beta_post_of_rb), beta_true_pdf(p)), 0, 1)
            overlap_areas_rb.append(overlap_area)

        # 確率の正規化
        total_overlap_area_bb = sum(overlap_areas_bb)
        true_prob_posteriors_bb = [area / total_overlap_area_bb for area in overlap_areas_bb]
        total_overlap_area_rb = sum(overlap_areas_rb)
        true_prob_posteriors_rb = [area / total_overlap_area_rb for area in overlap_areas_rb]

        excepted_values = []
        for pattern in range(6):
            excepted_values.append(((true_prob_posteriors_bb[pattern] + true_prob_posteriors_rb[pattern]) / 2.0) * expected_return[pattern])
        # 結果の表示
        st.write(f"### Expected values {sum(excepted_values)}")
        st.subheader("RB probability distribution")
        st.altair_chart(chart_bb_with_lines,use_container_width=True)
        st.subheader("RB probability distribution")
        st.altair_chart(chart_rb_with_lines,use_container_width=True)

with tab2:
    selected_number = st.selectbox('Setting', [1, 2, 3, 4, 5, 6])
    # ユーザーが指定する回数
    max_draws = st.number_input('Games', min_value=1, max_value=1000, value=100)

    # 各設定のBonus確率の真値
    true_probabilities_of_bb = [float(Fraction(value).limit_denominator()) for value in machine_setting_dic[machine_series_code]["BB"].values()]
    true_probabilities_of_rb = [float(Fraction(value).limit_denominator()) for value in machine_setting_dic[machine_series_code]["RB"].values()]

    # どちらかが当たるまでの確率
    combined_probability = true_probabilities_of_bb[selected_number-1] + true_probabilities_of_rb[selected_number-1] - (true_probabilities_of_bb[selected_number-1] * true_probabilities_of_rb[selected_number-1])

    # 幾何分布を使用して、どちらかが当たるまでに引く回数の分布を計算
    draws = np.arange(1, 1001)
    probability_distribution = geom.pmf(draws, combined_probability)

    # データフレームを作成
    df = pd.DataFrame({
        'Number of Games': draws,
        'Probability': probability_distribution,
        'Highlight': np.where(draws <= max_draws, 'Highlight', 'Normal')
    })
    # ベースとなるラインチャート
    base = alt.Chart(df).mark_line().encode(
        x=alt.X('Number of Games:Q'),
        y=alt.Y('Probability:Q',axis=alt.Axis(labels=False, title=None, grid=True))
    )
    # 色を塗るためのエリアチャート
    highlight = alt.Chart(df[df['Highlight'] == 'Highlight']).mark_area(opacity=0.2, color='blue').encode(
        x='Number of Games:Q',
        y='Probability:Q'
    )

    # ベースとハイライトを重ねる
    chart = alt.layer(base, highlight).interactive()
    # 累積分布関数 (CDF) を使って指定した回数までに当たる確率を計算
    cumulative_probability = geom.cdf(max_draws, combined_probability)

    st.write(f"### {cumulative_probability*100:.4f}%")
    st.altair_chart(chart,use_container_width=True)
