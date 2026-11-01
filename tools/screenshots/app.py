"""
ui-memo.com の Streamlit ページ（/categories/streamlit/*）に載せるスクリーンショットの撮影用アプリ。

?s=<カテゴリ>/<名前> で1場面だけを、幅600pxの白い枠（.st-key-shot）に描く。
shoot.py がこの枠を2倍の解像度で撮り、幅1200pxの画像にする。

リポジトリのルートで起動すること（ルートの .streamlit/config.toml が読まれ、
プレイグラウンドと同じテーマになる。Streamlit の版も requirements.txt と同じになる）:

    streamlit run tools/screenshots/app.py --server.port 8603 --server.headless true

場面を足すときは、<カテゴリ>_<名前>() という関数を書くだけでよい（下の SCENES が自動で拾う）。
画像のファイル名は <カテゴリ>/<名前>.png になり、ui-memo の public/images/streamlit/ と対応する。
"""
import datetime as dt
import time

import pandas as pd
import streamlit as st

st.set_page_config(page_title="shots", layout="centered", initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
  header[data-testid="stHeader"] { display: none; }
  [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
  .block-container { max-width: 680px !important; padding: 40px 20px 260px !important; }
  .st-key-shot { width: 600px !important; padding: 14px !important; box-sizing: border-box; background: #fff; }
</style>
""",
    unsafe_allow_html=True,
)

DF = pd.DataFrame({
    "ライブラリ": ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts"],
    "Stars(k)": [24, 62, 17, 13, 65, 14],
    "推奨": [True, True, False, True, True, False],
})
CD = pd.DataFrame({"A": [3, 5, 4, 6, 8, 7], "B": [2, 3, 5, 4, 6, 9]})


# ───────── データ ─────────
def data_pagination():
    p = st.pagination(3, default=1, key="pg")
    st.dataframe(DF.iloc[(p - 1) * 2:(p - 1) * 2 + 2], hide_index=True)


def data_data_editor():
    st.data_editor(DF, hide_index=True, num_rows="dynamic", key="ed")


def data_dataframe():
    st.dataframe(DF, hide_index=True)


def data_metric():
    c1, c2, c3 = st.columns(3)
    c1.metric("UU", "2,840", "+12%")
    c2.metric("PV", "9,120", "+8%")
    c3.metric("直帰率", "41%", "-3%")


def data_json():
    st.json({"library": "Streamlit", "version": "1.66", "ok": True,
             "widgets": ["dataframe", "data_editor", "pagination"]})


def data_button_column():
    names = ["ECharts", "Recharts", "Plotly"]
    df = pd.DataFrame({
        "ライブラリ": names,
        "メモ": ["図の種類が豊富\n\n- canvas で描画\n- ゲージやサンキーも",
                 "React 向けの定番\n\n- SVG で描画\n- 部品を組み合わせて作る",
                 "科学技術系に強い\n\n- WebGL で大量の点も\n- 3D のグラフも"],
        "詳細": [":material/visibility: 見る"] * 3,
    })
    st.dataframe(df, hide_index=True, column_config={
        "メモ": st.column_config.MarkdownColumn(width="medium"),
        "詳細": st.column_config.ButtonColumn(key="btn"),
    })


# ───────── チャート ─────────
def charts_line_chart():
    st.line_chart(CD, height=250)


def charts_area_chart():
    st.area_chart(CD, height=250)


def charts_bar_chart():
    st.bar_chart(CD, height=250)


def charts_scatter_chart():
    st.scatter_chart(CD, x="A", y="B", height=250)


def charts_map_chart():
    # 地図のタイルをネットから読むので、外に出られない環境では地図が白くなる（README 参照）
    df = pd.DataFrame({"lat": [35.681, 35.444, 35.861, 35.605],     # 東京・横浜・さいたま・千葉
                       "lon": [139.767, 139.638, 139.645, 140.123]})
    st.map(df, height=290)


def charts_echarts_chart():
    st.echarts_chart({
        "tooltip": {"trigger": "item"},
        "legend": {"bottom": 0},
        "series": [{
            "type": "pie",
            "radius": ["45%", "70%"],
            "label": {"formatter": "{b} {d}%"},
            "data": [
                {"name": "スマホ", "value": 58},
                {"name": "PC", "value": 36},
                {"name": "タブレット", "value": 6},
            ],
        }],
    }, height=280)


def charts_mermaid_chart():
    st.mermaid_chart("""
flowchart LR
    A[入力] --> B{検証}
    B -->|OK| C[保存]
    B -->|NG| D[エラー表示]
    D --> A
""")


# ───────── チャット ─────────
def chat_chat_input():
    st.chat_input("メッセージを入力", key="ci")
    st.caption("Enter で送信。Shift+Enter で改行。")


def chat_chat_message():
    with st.chat_message("user"):
        st.write("Streamlitでチャットを作るには？")
    with st.chat_message("assistant"):
        st.write("st.chat_message と st.chat_input で数行で作れます。ロールごとにアイコン付きの吹き出しが出ます。")


def chat_write_stream():
    text = "受け取りました。以下の手順で進めます：\n\n1. データを読み込む\n2. 集計する\n3. グラフ化する"

    def gen():
        for ch in text:
            yield ch

    with st.chat_message("assistant"):
        st.write_stream(gen())


def chat_submit_mode():
    msgs = st.container()
    v = st.chat_input("メッセージを入力", key="ci_stop", submit_mode="stop")
    with msgs:
        if v:
            with st.chat_message("user"):
                st.write(v)
            with st.chat_message("assistant"):
                st.write("受け取りました。順番に説明します。まず、Streamlit の")
    if v:
        time.sleep(120)  # 生成中のまま止めて、停止ボタンを撮る


def chat_paste_file():
    st.chat_input("メッセージを入力（画像の貼り付けも可）", key="ci_file",
                  accept_file=True, file_type=["png", "jpg", "jpeg", "gif", "webp"])


# ───────── 入力 ─────────
def inputs_pills():
    st.pills("技術", ["TypeScript", "Tailwind", "Vercel"], selection_mode="multi",
             default=["TypeScript"], key="pl")


def inputs_segmented_control():
    st.segmented_control("期間", ["日", "週", "月"], default="週", key="sg")


def inputs_audio_input():
    st.audio_input("音声を録音", key="au")


def inputs_link_button():
    st.link_button("UI Memo を開く", "https://www.ui-memo.com")


def inputs_toggle():
    st.toggle("ダークモードを有効化", value=True, key="tg")


def inputs_button():
    c1, c2 = st.columns(2)
    c1.button("送信", type="primary", key="b1")
    c2.button("キャンセル", key="b2")


def inputs_selectbox():
    st.selectbox("フレームワーク", ["Next.js", "Remix", "Astro"], key="sb")


def inputs_multiselect():
    st.multiselect("使用ライブラリ", ["React", "Vue", "Svelte", "Angular"],
                   default=["React", "Vue"], key="ms")


def inputs_slider():
    st.slider("価格帯（万円）", 0, 100, (20, 80), key="sl")


def inputs_date_input():
    st.date_input("公開日", dt.date(2026, 11, 1), key="di")


def inputs_color_picker():
    st.color_picker("アクセントカラー", "#cc0000", key="cp")


def inputs_file_uploader():
    st.file_uploader("CSV をアップロード", type=["csv"], key="fu")


def inputs_text_validate():
    st.text_input("メール", type="email", key="em")
    st.text_input("郵便番号", placeholder="123-4567", required=True,
                  validate=(r"^\d{3}-\d{4}$", "123-4567 の形式で入力してください"), key="zip")


def inputs_text_live():
    libs = ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts", "Victory", "D3"]
    q = st.text_input("ライブラリを検索", type="search", live=True,
                      placeholder="名前の一部（例: chart）", key="sr")
    hits = [n for n in libs if q.lower() in n.lower()]
    st.caption("　".join(hits) if hits else "該当なし")


# ───────── オーバーレイ ─────────
def overlay_dialog():
    @st.dialog("確認")
    def _d():
        st.write("これはモーダルダイアログです。")
        st.text_input("名前", key="dn")
        c1, c2 = st.columns(2)
        c1.button("OK", type="primary", key="dok")
        c2.button("キャンセル", key="dcancel")
    _d()


def overlay_popover():
    with st.popover("設定"):
        st.checkbox("通知を受け取る", value=True, key="pc")
        st.slider("音量", 0, 100, 60, key="ps")
        st.radio("テーマ", ["ライト", "ダーク"], key="pr")


def overlay_tabs():
    t1, t2, t3 = st.tabs(["概要", "詳細", "設定"])
    with t1:
        st.write("概要タブの内容です。")
        st.metric("ユーザー数", "2,840", "+12%")
    t2.write("詳細タブの内容です。")
    t3.write("設定タブの内容です。")


def overlay_expander():
    with st.expander("詳細を表示", expanded=True):
        st.write("展開された中身。クリックで折りたたみできるセクション。")
        st.code("with st.expander('詳細', expanded=True):", language="python")


def overlay_columns():
    c1, c2, c3 = st.columns(3)
    c1.metric("売上", "¥1.2M")
    c2.metric("UU", "2,840")
    c3.metric("PV", "9,120")


def overlay_container():
    with st.container(border=True):
        st.write("枠付きコンテナ（border=True）。関連する要素をまとめる。")
        st.button("中のボタン", key="cb")


def overlay_expander_step():
    with st.expander("要件を整理", type="step", icon=":material/check_circle:"):
        st.write("誰が・何のために使うかを書き出す")
    with st.expander("UIを選ぶ", type="step", icon=":material/check_circle:"):
        st.write("UI Memo で候補のライブラリを比べる")
    with st.expander("実装する", type="step", icon="spinner", expanded=True):
        st.write("デモのコードをもとに組み込む")
    st.expander("公開", type="step")


def overlay_drawer():
    # 背景のページ（ドロワーを開いたときに暗くなる側）
    st.markdown("#### 商品一覧")
    c1, c2, c3 = st.columns(3)
    for c, (n, p) in zip((c1, c2, c3), [("ノート", "¥480"), ("ペン", "¥220"), ("付箋", "¥160")]):
        with c.container(border=True):
            st.markdown(f"**{n}**")
            st.caption(p)
    st.button("右から絞り込み", icon=":material/tune:", key="open_r")

    @st.dialog("絞り込み", position="right")
    def _filter():
        st.multiselect("カテゴリ", ["文具", "雑貨", "本"], default=["文具"], key="fc")
        st.slider("価格", 0, 1000, (100, 600), step=50, key="fp")
        st.button("この条件で絞り込む", type="primary", key="fa")
    _filter()


# ───────── フィードバック ─────────
def feedback_feedback():
    st.write("この回答は役に立ちましたか？")
    st.feedback("stars", key="fb")
    st.caption("thumbs / stars / faces から選べる")


def feedback_toast():
    st.toast("保存しました", icon="✅", duration="infinite")  # 出したまま撮る


def feedback_status():
    with st.status("データを処理中...", expanded=True):
        st.write("ファイルを読み込み")
        st.write("レコードを集計")
        st.write("完了")


def feedback_progress():
    st.write("ダウンロード中...")
    st.progress(0.6, text="60%")


def feedback_alerts():
    st.info("情報メッセージ（st.info）")
    st.success("成功メッセージ（st.success）")
    st.warning("警告メッセージ（st.warning）")
    st.error("エラーメッセージ（st.error）")


def feedback_skeleton():
    st.markdown("**売上ダッシュボード**")
    c1, c2, c3 = st.columns(3)
    for c in (c1, c2, c3):
        with c:
            st.skeleton(height=72)
    st.skeleton(height=160)


def feedback_status_step():
    with st.status("データを取得", state="complete", type="step"):
        st.write("1,240 件を取得")
    with st.status("集計", state="complete", type="step"):
        st.write("日別の合計を計算")
    s = st.status("レポートを作成中", type="step", expanded=True)  # with を使わないと実行中のまま
    s.write("グラフを描いています…")


SCENES = {name.replace("_", "/", 1): fn for name, fn in globals().items()
          if callable(fn) and name.split("_", 1)[0] in
          ("data", "charts", "chat", "inputs", "overlay", "feedback")}

scene = st.query_params.get("s", "")
if scene == "list":
    st.write(sorted(SCENES))
elif scene in SCENES:
    if scene == "overlay/drawer":  # 背景のページを左に寄せ、ドロワーに隠れない部分を増やす
        st.markdown("<style>[data-testid='stMain']{align-items:flex-start !important;}.block-container{max-width:600px !important;}</style>",
                    unsafe_allow_html=True)
    key = "page" if scene == "overlay/drawer" else "shot"
    with st.container(key=key):
        SCENES[scene]()
else:
    st.write("unknown scene", scene)
