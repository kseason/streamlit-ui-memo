"""
UI Memo ─ Streamlit UI ウィジェット網羅カタログ（ライブ・プレイグラウンド）
サイドバーでカテゴリを切り替えるマルチページ構成。各ウィジェットは 左:デモ／右:コード。
"""
import time
import pandas as pd
import streamlit as st

# ── 配色（ここを差し替えれば全体のトーンが変わる）──
ACCENT = "#6C8CF5"
ACCENT_DARK = "#3B5BDB"
ACCENT_SOFT = "#EEF2FE"
TEXT = "#2A2E3A"
MUTED = "#6B7280"
BORDER = "#E6E9F2"
TIER_A = ("#FFF3E0", "#B26A00", "#FFE0B2")   # 新しめ・要確認
TIER_B = ("#EEF1F6", "#4B5563", "#E2E6EE")   # 中堅
TIER_C = ("#E8F6EE", "#257A52", "#CDEBD9")   # 広く使える

st.set_page_config(
    page_title="Streamlit UI ウィジェット網羅カタログ | UI Memo",
    page_icon="🎛️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── ui-memo クロスリンク（確認済みURLのみ。空は非表示。⚠公開前に実URL確認）──
UIMEMO = {
    "pagination": "https://www.ui-memo.com/categories/navigation/pagination",
    "slider": "https://www.ui-memo.com/categories/simple-operations/slider",
}

# ── スタイル ──
st.markdown(f"""
<style>
  .block-container {{ max-width: 820px; }}
  .wt-pill {{ display:inline-block; padding:2px 10px; border-radius:999px;
    background:{ACCENT_SOFT}; color:{ACCENT_DARK}; font-size:.78rem; font-weight:600; }}
  .wt-head {{ display:flex; align-items:center; gap:8px; margin:.1rem 0 .15rem; }}
  .wt-name {{ font-weight:700; font-family:monospace; color:{TEXT}; font-size:.95rem; }}
  .wt-badge {{ font-size:.7rem; font-weight:700; padding:1px 8px; border-radius:999px; border:1px solid; white-space:nowrap; }}
  .wt-A {{ background:{TIER_A[0]}; color:{TIER_A[1]}; border-color:{TIER_A[2]}; }}
  .wt-B {{ background:{TIER_B[0]}; color:{TIER_B[1]}; border-color:{TIER_B[2]}; }}
  .wt-C {{ background:{TIER_C[0]}; color:{TIER_C[1]}; border-color:{TIER_C[2]}; }}
  .wt-desc {{ color:{MUTED}; font-size:.82rem; margin:.1rem 0 .5rem; }}
  .wt-link {{ font-size:.8rem; color:{ACCENT_DARK}; text-decoration:none; font-weight:600; }}
  .wt-link:hover {{ text-decoration:underline; }}
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
        "PythonだけでこのUIが全部リアルタイムに動く。"
        "UIコンポーネント実装リファレンス [UI Memo](https://ui-memo.com) のプレイグラウンド。"
        "左のサイドバーからカテゴリを選んでください。"
    )

    st.subheader("バージョン表記の見方")
    st.markdown(f"""
    <div class="wt-legrow"><b style="background:{TIER_A[0]};color:{TIER_A[1]};border-color:{TIER_A[2]}">Tier A　v1.37〜</b> 新しめ。古い環境だと未提供の可能性（要確認）</div>
    <div class="wt-legrow"><b style="background:{TIER_B[0]};color:{TIER_B[1]};border-color:{TIER_B[2]}">Tier B　v1.23〜1.32</b> 中堅</div>
    <div class="wt-legrow"><b style="background:{TIER_C[0]};color:{TIER_C[1]};border-color:{TIER_C[2]}">Tier C　初期〜</b> ごく初期から安定。ほぼ全環境でOK</div>
    """, unsafe_allow_html=True)

    st.subheader("リアルタイムに反応するショーケース")
    with st.container(border=True):
        series = st.segmented_control(
            "系列", ["売上", "UU", "PV"], default="売上",
            key="hook_series", label_visibility="collapsed") or "売上"
        base = {"売上": [120, 150, 170, 140, 190, 230, 260],
                "UU": [800, 920, 1010, 980, 1120, 1340, 1500],
                "PV": [2400, 2600, 3010, 2880, 3320, 3900, 4400]}
        df = pd.DataFrame({series: base[series]}, index=[f"D{i+1}" for i in range(7)])
        c1, c2 = st.columns([3, 1])
        c1.line_chart(df, height=160)
        c2.metric(series, f"{base[series][-1]:,}",
                  f"+{base[series][-1]-base[series][-2]:,}")

def page_data():
    st.header("データ表示・編集")
    _df = pd.DataFrame({
        "ライブラリ": ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts"],
        "Stars(k)": [24, 62, 17, 13, 65, 14],
        "推奨": [True, True, False, True, True, False],
    })
    def _pg():
        per = 2
        n = (len(_df) + per - 1) // per
        p = st.pagination(n, default=1, key="pg_data")
        st.dataframe(_df.iloc[(p-1)*per:(p-1)*per+per], use_container_width=True, hide_index=True)
    render_section([
        {"name": "st.dataframe", "ver": (1, 0), "link": "line_chart",
         "desc": "ソート・検索・列メニュー標準装備の表示テーブル。",
         "code": "st.dataframe(\n    df,\n    hide_index=True,\n)",
         "render": lambda: st.dataframe(_df, use_container_width=True, hide_index=True)},
        {"name": "st.data_editor", "ver": (1, 23),
         "desc": "セルを直接編集できるグリッド。行追加も可。",
         "code": 'st.data_editor(\n    df,\n    num_rows="dynamic",\n)',
         "render": lambda: st.data_editor(_df, use_container_width=True, hide_index=True,
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
    _cd = pd.DataFrame({"A": [3, 5, 4, 6, 8, 7], "B": [2, 3, 5, 4, 6, 9]})
    _map = pd.DataFrame({"lat": [35.466, 35.443, 35.46], "lon": [139.622, 139.638, 139.63]})
    render_section([
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
    st.markdown("**3行でチャットUIが組める** — Streamlitの代表的な強み")
    def _stream(text):
        for ch in text:
            yield ch
            time.sleep(0.01)
    if "hist" not in st.session_state:
        st.session_state.hist = [{"role": "assistant", "content": "なんでも入力してみてください。"}]
    for m in st.session_state.hist:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    if prompt := st.chat_input("メッセージを入力", key="chat_in"):
        st.session_state.hist.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            reply = f"受け取りました：{prompt}"
            st.write_stream(_stream(reply))
        st.session_state.hist.append({"role": "assistant", "content": reply})
    st.markdown('<div class="wt-sep"></div>', unsafe_allow_html=True)
    st.markdown('<span class="wt-badge wt-B">v1.24〜</span> '
                f'<span style="color:{MUTED};font-size:.8rem">chat_message / chat_input。'
                'write_stream は v1.31〜</span>', unsafe_allow_html=True)
    st.code('with st.chat_message("user"):\n'
            '    st.write(prompt)\n'
            'st.write_stream(stream)', language="python")

def page_inputs():
    st.header("入力ウィジェット")
    render_section([
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
    render_section([
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
         "desc": "折りたたみ領域。v1.58で type='compact' 追加。",
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
    def _toast():
        if st.button("toastを出す", key="w_toast"):
            st.toast("保存しました", icon="✅")
    render_section([
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
sidebar_legend()
nav = st.navigation({
    "": [st.Page(page_home, title="はじめに", icon=":material/home:", default=True)],
    "カテゴリ": [
        st.Page(page_data, title="データ表示・編集", icon=":material/table:"),
        st.Page(page_charts, title="チャート", icon=":material/bar_chart:"),
        st.Page(page_chat, title="チャット", icon=":material/chat:"),
        st.Page(page_inputs, title="入力ウィジェット", icon=":material/edit:"),
        st.Page(page_overlay, title="オーバーレイ＆コンテナ", icon=":material/layers:"),
        st.Page(page_feedback, title="フィードバック", icon=":material/notifications:"),
    ],
})
nav.run()