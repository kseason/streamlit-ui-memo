"""
UI Memo ─ Streamlit UI ウィジェット網羅カタログ（ライブ・プレイグラウンド）
サイドバーでカテゴリを切り替えるマルチページ構成。各ウィジェットは 左:デモ／右:コード。
"""
import time
import pandas as pd
import streamlit as st

# ── 配色：ui-memo.com のトークンに合わせる（ここを差し替えれば全体のトーンが変わる）──
ACCENT = "#cc0000"        # --color-accent（赤）
ACCENT_DARK = "#990000"
CREAM = "#efe7cf"         # --color-button（クリーム #e8e0c6）の echo
CREAM_TEXT = "#6b5a2e"
TEXT = "#2b2b2b"          # 見出し・ウィジェット名（本文 #555 はテーマ側）
MUTED = "#888888"         # 補足テキスト
BORDER = "#e5e5e5"
TIER_A = ("#FFF3E0", "#B26A00", "#FFE0B2")   # 新しめ・要確認
TIER_B = ("#EEF1F6", "#4B5563", "#E2E6EE")   # 中堅
TIER_C = ("#E8F6EE", "#257A52", "#CDEBD9")   # 広く使える

st.set_page_config(
    page_title="Streamlit UI ウィジェット網羅カタログ | UI Memo",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="auto",  # PCでは開き、スマホでは閉じた状態で始まる
)

# ── ui-memo クロスリンク（確認済みURLのみ。空は非表示。⚠公開前に実URL確認）──
UIMEMO = {
    "pagination": "https://www.ui-memo.com/categories/navigation/pagination",
    "slider": "https://www.ui-memo.com/categories/simple-operations/slider",
    "data_grid": "https://www.ui-memo.com/categories/data-input/data_grid",
    "pie_chart": "https://www.ui-memo.com/categories/data-visualization/pie_chart",
    "chat_ui": "https://www.ui-memo.com/categories/data-input/chat_ui",
    "form_validation": "https://www.ui-memo.com/categories/data-input/form-validation",
    "hamburger_menu": "https://www.ui-memo.com/categories/navigation/hamburger-menu",
    "skeleton": "https://www.ui-memo.com/categories/simple-display/skeleton",
}

# ── 被リンク：playground → ui-memo.com の対応ページ ──
UIMEMO_PAGE = {
    "hub": "https://www.ui-memo.com/categories/streamlit",
    "data": "https://www.ui-memo.com/categories/streamlit/data",
    "charts": "https://www.ui-memo.com/categories/streamlit/charts",
    "chat": "https://www.ui-memo.com/categories/streamlit/chat",
    "inputs": "https://www.ui-memo.com/categories/streamlit/inputs",
    "overlay": "https://www.ui-memo.com/categories/streamlit/overlay",
    "feedback": "https://www.ui-memo.com/categories/streamlit/feedback",
}

def umemo_backlink(key, label):
    """ui-memo.com の対応ページへの戻り導線（解説・コード・React比較）。"""
    st.markdown(
        f'<a class="wt-back" href="{UIMEMO_PAGE[key]}" target="_blank" '
        f'rel="noopener">📖 {label}の解説・コード・React比較を読む（UI Memo）↗</a>',
        unsafe_allow_html=True,
    )

# ── スタイル ──
st.markdown(f"""
<style>
  .block-container {{ max-width: min(1280px, 94vw); margin-inline: auto; padding-top: 2rem; }}
  .block-container h1, .block-container h2, .block-container h3 {{ color:{TEXT}; }}
  .wt-pill {{ display:inline-block; padding:2px 10px; border-radius:5px;
    background:{CREAM}; color:{CREAM_TEXT}; font-size:.78rem; font-weight:700; }}
  .wt-head {{ display:flex; align-items:center; gap:8px; margin:.1rem 0 .15rem; }}
  .wt-name {{ font-weight:700; font-family:monospace; color:{TEXT}; font-size:.95rem; }}
  .wt-badge {{ font-size:.7rem; font-weight:700; padding:1px 8px; border-radius:999px; border:1px solid; white-space:nowrap; }}
  .wt-A {{ background:{TIER_A[0]}; color:{TIER_A[1]}; border-color:{TIER_A[2]}; }}
  .wt-B {{ background:{TIER_B[0]}; color:{TIER_B[1]}; border-color:{TIER_B[2]}; }}
  .wt-C {{ background:{TIER_C[0]}; color:{TIER_C[1]}; border-color:{TIER_C[2]}; }}
  .wt-desc {{ color:{MUTED}; font-size:.82rem; margin:.1rem 0 .5rem; }}
  .wt-link {{ font-size:.8rem; color:{ACCENT}; text-decoration:none; font-weight:600; }}
  .wt-link:hover {{ text-decoration:underline; }}
  .wt-back {{ display:inline-block; border:1px solid {ACCENT}; border-radius:5px;
    padding:6px 12px; color:{ACCENT}; text-decoration:none; font-size:.85rem; font-weight:700;
    background:{CREAM}; margin-bottom:.6rem; }}
  .wt-back:hover {{ opacity:.8; }}
  .wt-sep {{ border-top:1px solid {BORDER}; margin:1.2rem 0; }}
  .wt-legrow {{ display:flex; align-items:center; gap:6px; margin:.2rem 0; font-size:.74rem; }}
  .wt-legrow b {{ padding:1px 8px; border-radius:999px; border:1px solid; }}
</style>
""", unsafe_allow_html=True)

# ── Tier / バッジ ──
def tier_of(ver):
    return "A" if ver >= (1, 37) else "B" if ver >= (1, 23) else "C"

def badge_text(ver):
    return "初期〜" if ver <= (1, 0) else f"v{ver[0]}.{ver[1]}〜"

def card(name, ver, desc, code, render, link_key=None):
    """左:デモ／右:コード の2カラム。"""
    left, right = st.columns([1, 1], gap="medium")
    with left:
        t = tier_of(ver)
        st.markdown(
            f'<div class="wt-head"><span class="wt-name">{name}</span>'
            f'<span class="wt-badge wt-{t}">{badge_text(ver)}</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<p class="wt-desc">{desc}</p>', unsafe_allow_html=True)
        render()
    with right:
        st.code(code, language="python")
        url = UIMEMO.get(link_key or "")
        if url:
            st.markdown(
                f'<a class="wt-link" href="{url}" target="_blank">ui-memoで実装比較 →</a>',
                unsafe_allow_html=True,
            )
    st.markdown('<div class="wt-sep"></div>', unsafe_allow_html=True)

def render_section(items):
    for w in sorted(items, key=lambda x: x["ver"], reverse=True):
        card(w["name"], w["ver"], w["desc"], w["code"], w["render"], w.get("link"))

# ── サイドバーに常設のTier凡例 ──
def sidebar_legend():
    with st.sidebar:
        st.markdown("###### バージョン凡例")
        st.markdown(f"""
        <div class="wt-legrow"><b style="background:{TIER_A[0]};color:{TIER_A[1]};border-color:{TIER_A[2]}">A</b> 新しめ・要確認</div>
        <div class="wt-legrow"><b style="background:{TIER_B[0]};color:{TIER_B[1]};border-color:{TIER_B[2]}">B</b> 中堅</div>
        <div class="wt-legrow"><b style="background:{TIER_C[0]};color:{TIER_C[1]};border-color:{TIER_C[2]}">C</b> 広く使える</div>
        <div style="color:{MUTED};font-size:.72rem;margin-top:.3rem">各UIの導入バージョンを明記</div>
        """, unsafe_allow_html=True)

# ═══════════════ ページ定義 ═══════════════
def page_home():
    st.title("Streamlit UI ウィジェット網羅カタログ")
    st.markdown(f'<span class="wt-pill">このデモは v{st.__version__} で動作中</span>',
                unsafe_allow_html=True)
    st.markdown(
        "PythonだけでこのUIが動く、UIコンポーネント実装リファレンス "
        "[UI Memo](https://ui-memo.com) のプレイグラウンド。"
        "左のサイドバーからカテゴリを選ぶと、各ウィジェットを実際に触れます。"
    )
    umemo_backlink("hub", "Streamlit UI ガイド（総括）")

    # 版が上がっても見出しと中身がずれないよう、対象の版は固定で書く（次の更新時に差し替える）
    st.subheader("v1.59〜1.66 の主な新機能")
    st.markdown("前回の更新（v1.58）以降に入った主な機能です。デモは各ページで実際に触れます。")

    new_features = [
        ("**ButtonColumn・MarkdownColumn**（v1.59）｜ 表のセルにボタンや Markdown を置ける。",
         P_DATA, "データ表示・編集 で触る"),
        ("**st.echarts_chart**（v1.64）・**st.mermaid_chart**（v1.59）｜ "
         "ECharts の図や Mermaid のフローチャートを Python から描ける。",
         P_CHARTS, "チャート で触る"),
        ("**st.chat_input の `submit_mode`・ファイルの貼り付け**（v1.59）｜ "
         "生成中の停止ボタンと、画像の添付。",
         P_CHAT, "チャット で触る"),
        ("**st.text_input の `type`・`validate`**（v1.62）・**`live`**（v1.64）・**`required`**（v1.65）｜ "
         "メール・URL・検索の入力と、その場での検証。",
         P_INPUTS, "入力ウィジェット で触る"),
        ('**st.dialog の `position`**（v1.65）・**st.expander の `type="step"`**（v1.63）｜ '
         "画面の端から出るドロワーと、線でつながったタイムライン。",
         P_OVERLAY, "オーバーレイ＆コンテナ で触る"),
        ('**st.skeleton**（v1.59）・**st.status の `type="step"`**（v1.63）｜ '
         "読み込み中のプレースホルダーと、処理の手順の表示。",
         P_FEEDBACK, "フィードバック で触る"),
    ]
    for text, page, label in new_features:
        with st.container(border=True):
            st.markdown(text)
            st.page_link(page, label=label, icon=":material/arrow_forward:")
    st.caption("このほか、アプリのコードで async / await が使えるようになりました（v1.64）。"
               "v1.66 から Python 3.11 以上が必要です。")

    st.subheader("バージョン表記の見方")
    st.markdown(f"""
    <div class="wt-legrow"><b style="background:{TIER_A[0]};color:{TIER_A[1]};border-color:{TIER_A[2]}">Tier A　v1.37〜</b> 新しめ。古い環境だと未提供の可能性（要確認）</div>
    <div class="wt-legrow"><b style="background:{TIER_B[0]};color:{TIER_B[1]};border-color:{TIER_B[2]}">Tier B　v1.23〜1.32</b> 中堅</div>
    <div class="wt-legrow"><b style="background:{TIER_C[0]};color:{TIER_C[1]};border-color:{TIER_C[2]}">Tier C　初期〜</b> ごく初期から安定。ほぼ全環境でOK</div>
    """, unsafe_allow_html=True)

def page_data():
    st.header("データ表示・編集")
    umemo_backlink("data", "データ表示・編集")
    _df = pd.DataFrame({
        "ライブラリ": ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts"],
        "Stars(k)": [24, 62, 17, 13, 65, 14],
        "推奨": [True, True, False, True, True, False],
    })
    def _pg():
        per = 2
        n = (len(_df) + per - 1) // per
        p = st.pagination(n, default=1, key="pg_data")
        st.dataframe(_df.iloc[(p-1)*per:(p-1)*per+per], width="stretch", hide_index=True)
    _names = ["ECharts", "Recharts", "Plotly"]
    def _btn_md():
        # MarkdownColumn のセルは素の文字で表示され、ダブルクリックで開くと Markdown が整形される
        df = pd.DataFrame({
            "ライブラリ": _names,
            "メモ": ["図の種類が豊富\n\n- canvas で描画\n- ゲージやサンキーも",
                     "React 向けの定番\n\n- SVG で描画\n- 部品を組み合わせて作る",
                     "科学技術系に強い\n\n- WebGL で大量の点も\n- 3D のグラフも"],
            "詳細": [":material/visibility: 見る"] * len(_names),
        })
        def _on_click():
            row = st.session_state.btn_col["row"]
            st.toast(f"{_names[row]} の「見る」が押されました")
        st.dataframe(df, width="stretch", hide_index=True, column_config={
            "メモ": st.column_config.MarkdownColumn(width="medium"),
            "詳細": st.column_config.ButtonColumn(on_click=_on_click, key="btn_col"),
        })
        st.caption("「見る」を押すと、押された行をコールバックで受け取ります。"
                   "メモのセルはダブルクリックで開くと Markdown が整形されて表示されます。")
    render_section([
        {"name": "ButtonColumn / MarkdownColumn", "ver": (1, 59), "link": "data_grid",
         "desc": "ButtonColumn はセルにボタンを置き、押された行をコールバックで受け取れる。"
                 "MarkdownColumn はセルを開くと Markdown を整形して表示する。v1.59で追加。",
         "code": 'st.dataframe(df, column_config={\n'
                 '    "メモ": st.column_config.MarkdownColumn(),\n'
                 '    "詳細": st.column_config.ButtonColumn(\n'
                 '        on_click=show, key="btn",\n'
                 '    ),\n'
                 '})\n'
                 '# show の中で、押された行は\n'
                 '# st.session_state.btn["row"]',
         "render": _btn_md},
        {"name": "st.dataframe", "ver": (1, 0), "link": "line_chart",
         "desc": "ソート・検索・列メニュー標準装備の表示テーブル。v1.59で列メニューに統計も追加。",
         "code": "st.dataframe(\n    df,\n    hide_index=True,\n)",
         "render": lambda: st.dataframe(_df, width="stretch", hide_index=True)},
        {"name": "st.data_editor", "ver": (1, 23),
         "desc": "セルを直接編集できるグリッド。行追加も可。",
         "code": 'st.data_editor(\n    df,\n    num_rows="dynamic",\n)',
         "render": lambda: st.data_editor(_df, width="stretch", hide_index=True,
                                          num_rows="dynamic", key="ed_data")},
        {"name": "st.pagination", "ver": (1, 58), "link": "pagination",
         "desc": "ページ送りUI。dataframe等のページングに。v1.58で追加。",
         "code": "page = st.pagination(\n    num_pages,\n    default=1,\n)",
         "render": _pg},
        {"name": "st.metric", "ver": (1, 0),
         "desc": "数値＋増減デルタを大きく見せるKPI表示。",
         "code": 'st.metric(\n    "UU", "2,840", "+12%",\n)',
         "render": lambda: st.metric("UU", "2,840", "+12%")},
        {"name": "st.json", "ver": (1, 0),
         "desc": "辞書/リストを折りたたみJSONビューで表示。",
         "code": 'st.json(\n    {"lib": "Streamlit"},\n)',
         "render": lambda: st.json({"lib": "Streamlit", "ok": True})},
    ])

def page_charts():
    st.header("チャート")
    umemo_backlink("charts", "チャート")
    _cd = pd.DataFrame({"A": [3, 5, 4, 6, 8, 7], "B": [2, 3, 5, 4, 6, 9]})
    _map = pd.DataFrame({"lat": [35.466, 35.443, 35.46], "lon": [139.622, 139.638, 139.63]})
    _donut = {
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
    }
    _flow = """
flowchart LR
    A[入力] --> B{検証}
    B -->|OK| C[保存]
    B -->|NG| D[エラー表示]
    D --> A
"""
    render_section([
        {"name": "st.echarts_chart", "ver": (1, 64), "link": "pie_chart",
         "desc": "ECharts の option（dict）をそのまま渡して描く。色やフォントは Streamlit のテーマに揃う。v1.64で追加。",
         "code": 'st.echarts_chart({\n'
                 '    "tooltip": {"trigger": "item"},\n'
                 '    "series": [{\n'
                 '        "type": "pie",\n'
                 '        "radius": ["45%", "70%"],\n'
                 '        "data": [\n'
                 '            {"name": "スマホ", "value": 58},\n'
                 '            {"name": "PC", "value": 36},\n'
                 '        ],\n'
                 '    }],\n'
                 '})',
         "render": lambda: st.echarts_chart(_donut, height=260,
                                            alt="デバイス別のアクセスのドーナツグラフ")},
        {"name": "st.mermaid_chart", "ver": (1, 59),
         "desc": "Mermaid 記法の文字列から、フローチャートやシーケンス図を描く。v1.59で追加。",
         "code": 'st.mermaid_chart("""\n'
                 'flowchart LR\n'
                 '    A[入力] --> B{検証}\n'
                 '    B -->|OK| C[保存]\n'
                 '    B -->|NG| D[エラー表示]\n'
                 '    D --> A\n'
                 '""")',
         "render": lambda: st.mermaid_chart(_flow, alt="入力から保存までのフローチャート")},
        {"name": "st.line_chart", "ver": (1, 0), "link": "line_chart",
         "desc": "DataFrameを渡すだけで折れ線。1行で描ける。",
         "code": "st.line_chart(df)",
         "render": lambda: st.line_chart(_cd, height=160)},
        {"name": "st.area_chart", "ver": (1, 0),
         "desc": "面グラフ。積み上げ表示にも対応。",
         "code": "st.area_chart(df)",
         "render": lambda: st.area_chart(_cd, height=160)},
        {"name": "st.bar_chart", "ver": (1, 0),
         "desc": "棒グラフ。横持ち/積み上げも引数で。",
         "code": "st.bar_chart(df)",
         "render": lambda: st.bar_chart(_cd, height=160)},
        {"name": "st.scatter_chart", "ver": (1, 27),
         "desc": "散布図。サイズ・色も列指定可。v1.27で追加。",
         "code": "st.scatter_chart(\n    df, x='A', y='B',\n)",
         "render": lambda: st.scatter_chart(_cd, x="A", y="B", height=160)},
        {"name": "st.map", "ver": (1, 0),
         "desc": "緯度経度のDataFrameを地図にプロット。",
         "code": "st.map(df)  # lat / lon",
         "render": lambda: st.map(_map, height=160)},
    ])

def page_chat():
    st.header("チャット")
    umemo_backlink("chat", "チャット")
    st.markdown("**3行でチャットUIが組める** — Streamlitの代表的な強み")
    st.caption("送信すると、返答の生成中は送信ボタンが停止ボタンに変わります。"
               "画像は左の＋ボタンから添付するか、入力欄に貼り付けられます。")
    def _stream(text):
        # 停止ボタンで途中で止めても、そこまでの返答が履歴に残るよう1文字ずつ保存する
        st.session_state.hist.append({"role": "assistant", "content": ""})
        for ch in text:
            st.session_state.hist[-1]["content"] += ch
            yield ch
            time.sleep(0.04)
    def _show(text, images):
        if text:
            st.write(text)
        for img in images:
            st.image(img, width=160)
    if "hist" not in st.session_state:
        st.session_state.hist = [{"role": "assistant", "content": "なんでも入力してみてください。"}]
    for m in st.session_state.hist:
        with st.chat_message(m["role"]):
            _show(m["content"], m.get("images", []))
    msg = st.chat_input("メッセージを入力（画像の貼り付けも可）", key="chat_in",
                        accept_file=True, file_type=["png", "jpg", "jpeg", "gif", "webp"],
                        max_upload_size=5, submit_mode="stop")
    if msg:
        images = [f.getvalue() for f in msg.files]
        st.session_state.hist.append({"role": "user", "content": msg.text, "images": images})
        with st.chat_message("user"):
            _show(msg.text, images)
        with st.chat_message("assistant"):
            got = f"（画像 {len(images)} 枚を受け取りました）" if images else ""
            st.write_stream(_stream(f"受け取りました：{msg.text}{got}"
                                    "　返答の生成中は、送信ボタンが停止ボタンに変わります。"
                                    "押すとその場で止まります。"))
    st.markdown('<div class="wt-sep"></div>', unsafe_allow_html=True)
    st.markdown('<span class="wt-badge wt-B">v1.24〜</span> '
                f'<span style="color:{MUTED};font-size:.8rem">chat_message / chat_input。'
                'write_stream は v1.31〜</span>', unsafe_allow_html=True)
    st.code('with st.chat_message("user"):\n'
            '    st.write(prompt)\n'
            'st.write_stream(stream)', language="python")
    st.markdown('<span class="wt-badge wt-A">v1.59〜</span> '
                f'<span style="color:{MUTED};font-size:.8rem">submit_mode="stop" で生成中に停止ボタン。'
                'accept_file（v1.43〜）を付けた入力欄に、ファイルを貼り付けて添付できる</span>',
                unsafe_allow_html=True)
    st.code('msg = st.chat_input(\n'
            '    "メッセージを入力",\n'
            '    accept_file=True,\n'
            '    file_type=["png", "jpg"],\n'
            '    submit_mode="stop",\n'
            ')\n'
            'if msg:\n'
            '    st.write(msg.text)   # 入力した文字\n'
            '    for f in msg.files:  # 添付したファイル\n'
            '        st.image(f)', language="python")
    st.markdown(f'<a class="wt-link" href="{UIMEMO["chat_ui"]}" target="_blank">'
                'ui-memoで実装比較 →</a>', unsafe_allow_html=True)

def page_inputs():
    st.header("入力ウィジェット")
    umemo_backlink("inputs", "入力ウィジェット")
    def _text_validate():
        st.text_input("メール", type="email", key="w_email")
        st.text_input("郵便番号", placeholder="123-4567", required=True,
                      validate=(r"^\d{3}-\d{4}$", "123-4567 の形式で入力してください"),
                      key="w_zip")
    _libs = ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts", "Victory", "D3"]
    def _text_live():
        q = st.text_input("ライブラリを検索", type="search", live=True,
                          placeholder="名前の一部（例: chart）", key="w_search")
        hits = [n for n in _libs if q.lower() in n.lower()]
        st.caption("　".join(hits) if hits else "該当なし")
    render_section([
        {"name": "st.text_input（live）", "ver": (1, 64),
         "desc": "live=True で、入力の手が止まったとき（250ms）に値が確定し、打ちながら絞り込める。v1.64で追加。",
         "code": 'q = st.text_input(\n'
                 '    "検索", type="search", live=True,\n'
                 ')\n'
                 'hits = [n for n in names\n'
                 '        if q.lower() in n.lower()]',
         "render": _text_live},
        {"name": "st.text_input（type / validate）", "ver": (1, 62), "link": "form_validation",
         "desc": 'type="email" などで入力の種類を指定（アイコンと形式の検証付き）。validate に正規表現とメッセージ、'
                 "required（v1.65）で空欄を防ぐ。v1.62で追加。",
         "code": 'st.text_input("メール", type="email")\n'
                 'st.text_input(\n'
                 '    "郵便番号",\n'
                 '    validate=(r"^\\d{3}-\\d{4}$",\n'
                 '              "123-4567 の形式で"),\n'
                 '    required=True,\n'
                 ')',
         "render": _text_validate},
        {"name": "st.pills", "ver": (1, 40),
         "desc": "タグ状の単一/複数選択。v1.40で追加。",
         "code": 'st.pills(\n    "lib", opts,\n    selection_mode="multi",\n)',
         "render": lambda: st.pills("lib", ["A", "B", "C"], selection_mode="multi",
                                    default=["A"], key="w_pills", label_visibility="collapsed")},
        {"name": "st.segmented_control", "ver": (1, 40),
         "desc": "セグメント切替ボタン。v1.40で追加。",
         "code": 'st.segmented_control(\n    "期間", ["日","週","月"],\n)',
         "render": lambda: st.segmented_control("期間", ["日", "週", "月"], default="週",
                                                key="w_seg", label_visibility="collapsed")},
        {"name": "st.audio_input", "ver": (1, 40),
         "desc": "マイク録音の入力。v1.40でGA。",
         "code": 'audio = st.audio_input("録音")',
         "render": lambda: st.audio_input("録音", key="w_audio", label_visibility="collapsed")},
        {"name": "st.toggle", "ver": (1, 26),
         "desc": "オン/オフのスイッチUI。v1.26で追加。",
         "code": 'st.toggle("有効化", value=True)',
         "render": lambda: st.toggle("有効化", value=True, key="w_toggle")},
        {"name": "st.link_button", "ver": (1, 27),
         "desc": "外部リンクへ飛ぶボタン。v1.27で追加。",
         "code": 'st.link_button(\n    "開く", "https://...",\n)',
         "render": lambda: st.link_button("UI Memoを開く", "https://ui-memo.com")},
        {"name": "st.button", "ver": (1, 0),
         "desc": "基本のボタン。type='primary'で強調。",
         "code": 'st.button("送信", type="primary")',
         "render": lambda: st.button("送信", type="primary", key="w_btn")},
        {"name": "st.selectbox", "ver": (1, 0),
         "desc": "単一選択のドロップダウン。",
         "code": 'st.selectbox(\n    "枠組み", ["Next.js","Remix"],\n)',
         "render": lambda: st.selectbox("枠組み", ["Next.js", "Remix", "Astro"], key="w_sel")},
        {"name": "st.multiselect", "ver": (1, 0),
         "desc": "複数選択。タグ表示。",
         "code": 'st.multiselect("技術", opts)',
         "render": lambda: st.multiselect("技術", ["TS", "Tailwind", "Vercel"],
                                          default=["TS"], key="w_ms")},
        {"name": "st.slider", "ver": (1, 0), "link": "slider",
         "desc": "数値/範囲をドラッグ入力。範囲はtupleで。",
         "code": "st.slider(\n    '量', 0, 100, (20, 80),\n)",
         "render": lambda: st.slider("量", 0, 100, (20, 80), key="w_sld")},
        {"name": "st.date_input", "ver": (1, 0),
         "desc": "日付ピッカー。範囲選択も可。",
         "code": 'st.date_input("日付")',
         "render": lambda: st.date_input("日付", key="w_date")},
        {"name": "st.color_picker", "ver": (1, 0),
         "desc": "カラーピッカー。HEXを返す。",
         "code": 'st.color_picker("色", "#6C8CF5")',
         "render": lambda: st.color_picker("色", "#6C8CF5", key="w_color")},
        {"name": "st.file_uploader", "ver": (1, 0),
         "desc": "ファイルアップロード。複数・拡張子制限可。",
         "code": 'st.file_uploader("ファイル")',
         "render": lambda: st.file_uploader("ファイル", key="w_file", label_visibility="collapsed")},
    ])

def page_overlay():
    st.header("オーバーレイ＆コンテナ")
    umemo_backlink("overlay", "オーバーレイ＆コンテナ")
    def _dialog():
        @st.dialog("確認")
        def _d():
            st.write("これはモーダルダイアログ。")
            if st.button("閉じる", key="dlg_close"):
                st.rerun()
        if st.button("ダイアログを開く", key="w_dlg"):
            _d()
    def _popover():
        with st.popover("設定を開く"):
            st.checkbox("通知", value=True, key="pop_chk")
            st.slider("音量", 0, 100, 60, key="pop_sld")
    def _drawer():
        @st.dialog("メニュー", position="left")
        def _menu():
            st.page_link(P_HOME, label="はじめに", icon=":material/home:")
            st.page_link(P_CHARTS, label="チャート", icon=":material/bar_chart:")
            st.page_link(P_INPUTS, label="入力ウィジェット", icon=":material/edit:")
            st.page_link(P_FEEDBACK, label="フィードバック", icon=":material/notifications:")
        @st.dialog("絞り込み", position="right")
        def _filter():
            st.multiselect("カテゴリ", ["チャート", "入力", "表示"], default=["チャート"], key="drw_cat")
            st.slider("価格", 0, 10000, (1000, 8000), step=500, key="drw_price")
            if st.button("この条件で絞り込む", type="primary", key="drw_apply"):
                st.rerun()
        row = st.container(horizontal=True)
        if row.button("左からメニュー", icon=":material/menu:", key="w_drw_l"):
            _menu()
        if row.button("右から絞り込み", icon=":material/tune:", key="w_drw_r"):
            _filter()
    def _expander_steps():
        with st.expander("要件を整理", type="step", icon=":material/check_circle:"):
            st.write("誰が・何のために使うかを書き出す")
        with st.expander("UIを選ぶ", type="step", icon=":material/check_circle:"):
            st.write("UI Memo で候補のライブラリを比べる")
        with st.expander("実装する", type="step", icon="spinner", expanded=True):
            st.write("デモのコードをもとに組み込む")
        st.expander("公開", type="step")  # 中身のないステップでタイムラインを閉じる
    render_section([
        {"name": "st.dialog（position）", "ver": (1, 65), "link": "hamburger_menu",
         "desc": 'position="left" / "right" で、画面の端から全高のドロワーを出す。幅はドラッグで変えられる。v1.65で追加。',
         "code": '@st.dialog("絞り込み", position="right")\n'
                 'def panel():\n'
                 '    st.multiselect("カテゴリ", opts)\n'
                 '\n'
                 'if st.button("右から絞り込み"):\n'
                 '    panel()',
         "render": _drawer},
        {"name": 'st.expander（type="step"）', "ver": (1, 63),
         "desc": "連続した expander が線でつながり、タイムラインになる。手順や処理の流れの表示に。v1.63で追加。",
         "code": 'with st.expander("要件を整理", type="step",\n'
                 '                 icon=":material/check_circle:"):\n'
                 '    st.write("...")\n'
                 'with st.expander("実装する", type="step",\n'
                 '                 icon="spinner"):\n'
                 '    st.write("...")\n'
                 'st.expander("公開", type="step")  # 空で終わり',
         "render": _expander_steps},
        {"name": "st.dialog", "ver": (1, 37),
         "desc": "モーダルダイアログ。@st.dialogで装飾。v1.37でGA。",
         "code": '@st.dialog("確認")\ndef show():\n    ...',
         "render": _dialog},
        {"name": "st.popover", "ver": (1, 32),
         "desc": "その場で開くポップオーバー。v1.32で追加。",
         "code": 'with st.popover("設定"):\n    ...',
         "render": _popover},
        {"name": "st.tabs", "ver": (1, 11),
         "desc": "タブ切替コンテナ。v1.11で追加。",
         "code": 'a, b = st.tabs(["A","B"])',
         "render": lambda: st.tabs(["A", "B"])},
        {"name": "st.expander", "ver": (1, 0),
         "desc": "折りたたみ領域。v1.58で type='compact'、v1.63で type='step' を追加。",
         "code": 'with st.expander("詳細"):\n    ...',
         "render": lambda: st.expander("詳細", expanded=True).write("中身")},
        {"name": "st.columns", "ver": (1, 0),
         "desc": "横並びレイアウト。比率指定可。",
         "code": "c1, c2 = st.columns(2)",
         "render": lambda: [c.button(f"col{i}", key=f"w_col{i}")
                            for i, c in enumerate(st.columns(2))]},
        {"name": "st.container", "ver": (1, 0),
         "desc": "border=Trueでカード的な囲みに。",
         "code": "with st.container(border=True):\n    ...",
         "render": lambda: st.container(border=True).write("囲みコンテナ")},
    ])

def page_feedback():
    st.header("フィードバック")
    umemo_backlink("feedback", "フィードバック")
    def _toast():
        if st.button("toastを出す", key="w_toast"):
            st.toast("保存しました", icon="✅")
    _pv = pd.DataFrame({"日付": ["10/01", "10/02", "10/03"], "PV": [1200, 1350, 980]})
    def _skeleton():
        if st.button("データを読み込む", key="w_skel"):
            with st.skeleton(height=140):
                time.sleep(1.5)  # 重い処理のかわり
            st.dataframe(_pv, width="stretch", hide_index=True)
        else:
            st.skeleton(height=140)  # 押す前は、読み込み中の見た目をそのまま表示
    def _status_steps():
        run = st.button("処理を実行", key="w_steps")
        steps = [("データを取得", "1,240 件を取得"), ("集計", "日別の合計を計算"),
                 ("レポートを作成", "グラフを描画")]
        for label, done in steps:
            # with を抜けると自動で完了（✓）になる。押す前は完了した状態で表示しておく
            with st.status(label, type="step", state="running" if run else "complete"):
                if run:
                    time.sleep(0.8)  # 重い処理のかわり
                st.write(done)
    render_section([
        {"name": "st.skeleton", "ver": (1, 59), "link": "skeleton",
         "desc": "読み込み中のプレースホルダー。with で囲むと処理の間だけ表示され、終わると消える。v1.59で追加。",
         "code": 'with st.skeleton(height=140):\n'
                 '    df = load_data()  # 重い処理\n'
                 'st.dataframe(df)',
         "render": _skeleton},
        {"name": 'st.status（type="step"）', "ver": (1, 63),
         "desc": "連続した status が線でつながり、処理の進み具合をタイムラインで見せられる。v1.63で追加。",
         "code": 'for label in ["データを取得", "集計",\n'
                 '              "レポートを作成"]:\n'
                 '    with st.status(label, type="step"):\n'
                 '        run(label)  # 処理中はスピナー、\n'
                 '                    # 終わると完了の印に',
         "render": _status_steps},
        {"name": "st.feedback", "ver": (1, 37),
         "desc": "星/サムズ評価ウィジェット。v1.37で追加。",
         "code": 'st.feedback("stars")',
         "render": lambda: st.feedback("stars", key="w_fb")},
        {"name": "st.toast", "ver": (1, 27),
         "desc": "一時的な通知トースト。v1.27で追加。",
         "code": 'st.toast(\n    "保存しました", icon="✅",\n)',
         "render": _toast},
        {"name": "st.status", "ver": (1, 27),
         "desc": "処理状況をまとめる展開可能ステータス。v1.27で追加。",
         "code": 'with st.status("処理中"):\n    ...',
         "render": lambda: st.status("処理中", expanded=True).write("ログ…")},
        {"name": "st.progress", "ver": (1, 0),
         "desc": "進捗バー。0.0〜1.0で指定。",
         "code": 'st.progress(0.6, text="...")',
         "render": lambda: st.progress(0.6, text="progress")},
        {"name": "st.info / success / warning / error", "ver": (1, 0),
         "desc": "色付きアラート。v1.58で title 引数追加。",
         "code": 'st.success("完了しました")',
         "render": lambda: st.success("完了しました")},
    ])

# ═══════════════ ナビゲーション ═══════════════
P_HOME = st.Page(page_home, title="はじめに", icon=":material/home:", default=True)
P_DATA = st.Page(page_data, title="データ表示・編集", icon=":material/table:")
P_CHARTS = st.Page(page_charts, title="チャート", icon=":material/bar_chart:")
P_CHAT = st.Page(page_chat, title="チャット", icon=":material/chat:")
P_INPUTS = st.Page(page_inputs, title="入力ウィジェット", icon=":material/edit:")
P_OVERLAY = st.Page(page_overlay, title="オーバーレイ＆コンテナ", icon=":material/layers:")
P_FEEDBACK = st.Page(page_feedback, title="フィードバック", icon=":material/notifications:")

sidebar_legend()
nav = st.navigation({
    "": [P_HOME],
    "カテゴリ": [P_DATA, P_CHARTS, P_CHAT, P_INPUTS, P_OVERLAY, P_FEEDBACK],
})
nav.run()