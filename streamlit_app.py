"""
UI Memo ─ Streamlit UI ウィジェット網羅カタログ（ライブ・プレイグラウンド）
https://ui-memo.com の記事から「実際に触ってみる」で誘導する用途。

各ウィジェットに「導入バージョン」をTierバッジで明記する：
  Tier A（新しめ・アンバー）= 古い環境だと未提供の可能性。要確認ゾーン
  Tier B（中堅・グレー）    = 2023後半〜2024
  Tier C（広く使える・緑）  = ごく初期から安定。ほぼ全環境でOK
"""
import time
import pandas as pd
import streamlit as st

# ───────────────────────────────────────────────
# 配色（ここを差し替えれば全体のトーンが変わる）
# ───────────────────────────────────────────────
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
)

# ───────────────────────────────────────────────
# ui-memo へのクロスリンク（確認済みURLのみ。空は非表示）
#   ⚠ 公開前に実URLを確認して追記すること（当て推量で死にリンクを作らない）
# ───────────────────────────────────────────────
UIMEMO = {
    "pagination": "https://www.ui-memo.com/categories/navigation/pagination",
    "slider": "https://www.ui-memo.com/categories/simple-operations/slider",
    # "dialog": "",        # 要URL確認（modal/dialog）
    # "popover": "",       # 要URL確認（popover/tooltip/dropdown）
    # "tabs": "",          # 要URL確認
    # "expander": "",      # 要URL確認（accordion）
    # "line_chart": "",    # 要URL確認（データ可視化比較）
    # "selectbox": "",     # 要URL確認（select）
    # "date_input": "",    # 要URL確認（datepicker）
    # "toast": "",         # 要URL確認（notification）
}

# ───────────────────────────────────────────────
# スタイル
# ───────────────────────────────────────────────
st.markdown(f"""
<style>
  .block-container {{ max-width: 760px; }}
  .wt-hero h1 {{ margin-bottom: .2rem; }}
  .wt-pill {{
    display:inline-block; padding:2px 10px; border-radius:999px;
    background:{ACCENT_SOFT}; color:{ACCENT_DARK}; font-size:.78rem; font-weight:600;
  }}
  .wt-legend {{ display:flex; gap:8px; flex-wrap:wrap; margin:.6rem 0 .2rem; }}
  .wt-legend span {{ font-size:.72rem; padding:2px 8px; border-radius:6px; }}
  .wt-head {{ display:flex; align-items:center; gap:8px; margin:.2rem 0 .1rem; }}
  .wt-name {{ font-weight:700; font-family:monospace; color:{TEXT}; font-size:.98rem; }}
  .wt-badge {{ font-size:.7rem; font-weight:700; padding:1px 8px; border-radius:999px; border:1px solid; }}
  .wt-A {{ background:{TIER_A[0]}; color:{TIER_A[1]}; border-color:{TIER_A[2]}; }}
  .wt-B {{ background:{TIER_B[0]}; color:{TIER_B[1]}; border-color:{TIER_B[2]}; }}
  .wt-C {{ background:{TIER_C[0]}; color:{TIER_C[1]}; border-color:{TIER_C[2]}; }}
  .wt-desc {{ color:{MUTED}; font-size:.85rem; margin:.1rem 0 .4rem; }}
  .wt-link {{ font-size:.82rem; color:{ACCENT_DARK}; text-decoration:none; font-weight:600; }}
  .wt-link:hover {{ text-decoration:underline; }}
  .wt-sep {{ border-top:1px solid {BORDER}; margin:1.1rem 0; }}
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# ヘッダ
# ───────────────────────────────────────────────
st.markdown('<div class="wt-hero">', unsafe_allow_html=True)
st.title("Streamlit UI ウィジェット網羅カタログ")
st.markdown(
    f'<span class="wt-pill">このデモは v{st.__version__} で動作中</span>',
    unsafe_allow_html=True,
)
st.markdown(
    "PythonだけでこのUIが全部リアルタイムに動く。"
    "UIコンポーネント実装リファレンス [UI Memo](https://ui-memo.com) のプレイグラウンド。",
)
st.markdown(f"""
<div class="wt-legend">
  <span style="background:{TIER_A[0]};color:{TIER_A[1]}">A 新しめ・要確認</span>
  <span style="background:{TIER_B[0]};color:{TIER_B[1]}">B 中堅</span>
  <span style="background:{TIER_C[0]};color:{TIER_C[1]}">C 広く使える</span>
  <span style="color:{MUTED}">← 各ウィジェットの導入バージョンを明記。古い環境で使えるか即判断</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────
# トップのフック：操作すると即反応するショーケース
# ───────────────────────────────────────────────
with st.container(border=True):
    st.markdown("**リアルタイムに反応するショーケース** — 系列を切り替えると即グラフ更新")
    series = st.segmented_control(
        "系列", ["売上", "UU", "PV"], default="売上",
        key="hook_series", label_visibility="collapsed",
    ) or "売上"
    base = {"売上": [120, 150, 170, 140, 190, 230, 260],
            "UU": [800, 920, 1010, 980, 1120, 1340, 1500],
            "PV": [2400, 2600, 3010, 2880, 3320, 3900, 4400]}
    df_hook = pd.DataFrame({series: base[series]}, index=[f"D{i+1}" for i in range(7)])
    c1, c2 = st.columns([3, 1])
    c1.line_chart(df_hook, height=160)
    c2.metric(series, f"{base[series][-1]:,}",
              f"+{base[series][-1] - base[series][-2]:,}")

st.divider()

# ───────────────────────────────────────────────
# Tier / バッジ計算
# ───────────────────────────────────────────────
def tier_of(ver):
    if ver >= (1, 37):
        return "A"
    if ver >= (1, 23):
        return "B"
    return "C"

def badge_text(ver):
    if ver <= (1, 0):
        return "初期〜"
    return f"v{ver[0]}.{ver[1]}〜"

def card(name, ver, desc, code, render, link_key=None):
    t = tier_of(ver)
    st.markdown(
        f'<div class="wt-head"><span class="wt-name">{name}</span>'
        f'<span class="wt-badge wt-{t}">{badge_text(ver)}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="wt-desc">{desc}</p>', unsafe_allow_html=True)
    render()
    st.code(code, language="python")
    url = UIMEMO.get(link_key or "")
    if url:
        st.markdown(
            f'<a class="wt-link" href="{url}" target="_blank">ui-memoで実装比較を見る →</a>',
            unsafe_allow_html=True,
        )
    st.markdown('<div class="wt-sep"></div>', unsafe_allow_html=True)

def render_section(items):
    """items: list of dict. 導入バージョンの新しい順に並べて描画。"""
    for w in sorted(items, key=lambda x: x["ver"], reverse=True):
        card(w["name"], w["ver"], w["desc"], w["code"], w["render"],
             w.get("link"))

tabs = st.tabs([
    "データ表示・編集", "チャート", "チャット",
    "入力ウィジェット", "オーバーレイ＆コンテナ", "フィードバック",
])

# ── データ表示・編集 ──
with tabs[0]:
    _df = pd.DataFrame({
        "ライブラリ": ["Recharts", "ECharts", "Plotly", "Nivo", "Chart.js", "ApexCharts"],
        "Stars(k)": [24, 62, 17, 13, 65, 14],
        "推奨": [True, True, False, True, True, False],
    })

    def _r_pagination():
        per = 2
        n = (len(_df) + per - 1) // per
        pg = st.pagination(n, default=1, key="pg_data")
        s = (pg - 1) * per
        st.dataframe(_df.iloc[s:s+per], use_container_width=True, hide_index=True)

    render_section([
        {"name": "st.dataframe", "ver": (1, 0), "link": "line_chart",
         "desc": "ソート・検索・列メニューが標準装備の表示テーブル。",
         "code": "st.dataframe(df, use_container_width=True, hide_index=True)",
         "render": lambda: st.dataframe(_df, use_container_width=True, hide_index=True)},
        {"name": "st.data_editor", "ver": (1, 23),
         "desc": "セルを直接編集できるグリッド。行追加も可能。",
         "code": 'st.data_editor(df, num_rows="dynamic")',
         "render": lambda: st.data_editor(_df, use_container_width=True,
                                          hide_index=True, num_rows="dynamic",
                                          key="ed_data")},
        {"name": "st.pagination", "ver": (1, 58), "link": "pagination",
         "desc": "ページ送りUI。dataframe等のページングに。v1.58で追加。",
         "code": "page = st.pagination(num_pages, default=1)",
         "render": _r_pagination},
        {"name": "st.metric", "ver": (1, 0),
         "desc": "数値＋増減デルタを大きく見せるKPI表示。",
         "code": 'st.metric("UU", "2,840", "+12%")',
         "render": lambda: st.metric("UU", "2,840", "+12%")},
        {"name": "st.json", "ver": (1, 0),
         "desc": "辞書/リストを折りたたみ可能なJSONビューで表示。",
         "code": 'st.json({"lib": "Streamlit", "ok": True})',
         "render": lambda: st.json({"lib": "Streamlit", "ok": True})},
    ])

# ── チャート ──
with tabs[1]:
    _cd = pd.DataFrame({"A": [3, 5, 4, 6, 8, 7], "B": [2, 3, 5, 4, 6, 9]})
    _map = pd.DataFrame({"lat": [35.466, 35.443, 35.46],
                         "lon": [139.622, 139.638, 139.63]})
    render_section([
        {"name": "st.line_chart", "ver": (1, 0), "link": "line_chart",
         "desc": "DataFrameを渡すだけで折れ線。1行で描ける。",
         "code": "st.line_chart(df)",
         "render": lambda: st.line_chart(_cd, height=180)},
        {"name": "st.area_chart", "ver": (1, 0),
         "desc": "面グラフ。積み上げ表示にも対応。",
         "code": "st.area_chart(df)",
         "render": lambda: st.area_chart(_cd, height=180)},
        {"name": "st.bar_chart", "ver": (1, 0),
         "desc": "棒グラフ。横持ち/積み上げも引数で。",
         "code": "st.bar_chart(df)",
         "render": lambda: st.bar_chart(_cd, height=180)},
        {"name": "st.scatter_chart", "ver": (1, 27),
         "desc": "散布図。サイズ・色も列で指定可能。v1.27で追加。",
         "code": "st.scatter_chart(df, x='A', y='B')",
         "render": lambda: st.scatter_chart(_cd, x="A", y="B", height=180)},
        {"name": "st.map", "ver": (1, 0),
         "desc": "緯度経度のDataFrameを地図にプロット。",
         "code": "st.map(df)  # 列名 lat / lon",
         "render": lambda: st.map(_map, height=180)},
    ])

# ── チャット ──
with tabs[2]:
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

    st.code(
        'with st.chat_message("user"):\n'
        '    st.write(prompt)\n'
        'st.write_stream(stream)   # ストリーミング表示',
        language="python",
    )
    st.markdown(
        '<span class="wt-badge wt-B">v1.24〜</span> '
        '<span style="color:#6B7280;font-size:.8rem">chat_message / chat_input。'
        'write_stream は v1.31〜</span>',
        unsafe_allow_html=True,
    )

# ── 入力ウィジェット ──
with tabs[3]:
    render_section([
        {"name": "st.pills", "ver": (1, 40),
         "desc": "タグ状の単一/複数選択。v1.40で追加。",
         "code": 'st.pills("lib", opts, selection_mode="multi")',
         "render": lambda: st.pills("lib", ["A", "B", "C"], selection_mode="multi",
                                    default=["A"], key="w_pills",
                                    label_visibility="collapsed")},
        {"name": "st.segmented_control", "ver": (1, 40),
         "desc": "セグメント切替ボタン。v1.40で追加。",
         "code": 'st.segmented_control("期間", ["日","週","月"])',
         "render": lambda: st.segmented_control("期間", ["日", "週", "月"], default="週",
                                                key="w_seg", label_visibility="collapsed")},
        {"name": "st.audio_input", "ver": (1, 40),
         "desc": "マイク録音の入力。v1.40でGA。",
         "code": 'audio = st.audio_input("録音")',
         "render": lambda: st.audio_input("録音", key="w_audio",
                                          label_visibility="collapsed")},
        {"name": "st.toggle", "ver": (1, 26),
         "desc": "オン/オフのスイッチUI。v1.26で追加。",
         "code": 'st.toggle("有効化", value=True)',
         "render": lambda: st.toggle("有効化", value=True, key="w_toggle")},
        {"name": "st.link_button", "ver": (1, 27),
         "desc": "外部リンクへ飛ぶボタン。v1.27で追加。",
         "code": 'st.link_button("開く", "https://...")',
         "render": lambda: st.link_button("UI Memoを開く", "https://ui-memo.com")},
        {"name": "st.button", "ver": (1, 0),
         "desc": "基本のボタン。type='primary'で強調。",
         "code": 'st.button("送信", type="primary")',
         "render": lambda: st.button("送信", type="primary", key="w_btn")},
        {"name": "st.selectbox", "ver": (1, 0), "link": "selectbox",
         "desc": "単一選択のドロップダウン。",
         "code": 'st.selectbox("枠組み", ["Next.js","Remix"])',
         "render": lambda: st.selectbox("枠組み", ["Next.js", "Remix", "Astro"],
                                        key="w_sel")},
        {"name": "st.multiselect", "ver": (1, 0),
         "desc": "複数選択。タグ表示。",
         "code": 'st.multiselect("技術", opts)',
         "render": lambda: st.multiselect("技術", ["TS", "Tailwind", "Vercel"],
                                          default=["TS"], key="w_ms")},
        {"name": "st.slider", "ver": (1, 0), "link": "slider",
         "desc": "数値/範囲をドラッグ入力。範囲はtupleで。",
         "code": "st.slider('量', 0, 100, (20, 80))",
         "render": lambda: st.slider("量", 0, 100, (20, 80), key="w_sld")},
        {"name": "st.date_input", "ver": (1, 0), "link": "date_input",
         "desc": "日付ピッカー。範囲選択も可能。",
         "code": 'st.date_input("日付")',
         "render": lambda: st.date_input("日付", key="w_date")},
        {"name": "st.color_picker", "ver": (1, 0),
         "desc": "カラーピッカー。HEXを返す。",
         "code": 'st.color_picker("色", "#6C8CF5")',
         "render": lambda: st.color_picker("色", "#6C8CF5", key="w_color")},
        {"name": "st.file_uploader", "ver": (1, 0),
         "desc": "ファイルアップロード。複数・拡張子制限可。",
         "code": 'st.file_uploader("ファイル")',
         "render": lambda: st.file_uploader("ファイル", key="w_file",
                                            label_visibility="collapsed")},
    ])

# ── オーバーレイ＆コンテナ ──
with tabs[4]:
    def _r_dialog():
        @st.dialog("確認")
        def _d():
            st.write("これはモーダルダイアログ。")
            if st.button("閉じる", key="dlg_close"):
                st.rerun()
        if st.button("ダイアログを開く", key="w_dlg"):
            _d()

    def _r_popover():
        with st.popover("設定を開く"):
            st.checkbox("通知", value=True, key="pop_chk")
            st.slider("音量", 0, 100, 60, key="pop_sld")

    render_section([
        {"name": "st.dialog", "ver": (1, 37), "link": "dialog",
         "desc": "モーダルダイアログ。@st.dialogで関数を装飾。v1.37でGA。",
         "code": '@st.dialog("確認")\ndef show(): ...',
         "render": _r_dialog},
        {"name": "st.popover", "ver": (1, 32), "link": "popover",
         "desc": "その場で開くポップオーバー。v1.32で追加。",
         "code": 'with st.popover("設定"):\n    ...',
         "render": _r_popover},
        {"name": "st.tabs", "ver": (1, 11), "link": "tabs",
         "desc": "タブ切替コンテナ。v1.11で追加。",
         "code": 'a, b = st.tabs(["A","B"])',
         "render": lambda: st.tabs(["A", "B"])},
        {"name": "st.expander", "ver": (1, 0), "link": "expander",
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

# ── フィードバック ──
with tabs[5]:
    def _r_toast():
        if st.button("toastを出す", key="w_toast"):
            st.toast("保存しました", icon="✅")

    render_section([
        {"name": "st.feedback", "ver": (1, 37),
         "desc": "星/サムズ評価ウィジェット。v1.37で追加。",
         "code": 'st.feedback("stars")',
         "render": lambda: st.feedback("stars", key="w_fb")},
        {"name": "st.toast", "ver": (1, 27), "link": "toast",
         "desc": "一時的な通知トースト。v1.27で追加。",
         "code": 'st.toast("保存しました", icon="✅")',
         "render": _r_toast},
        {"name": "st.status", "ver": (1, 27),
         "desc": "処理状況をまとめる展開可能なステータス。v1.27で追加。",
         "code": 'with st.status("処理中"):\n    ...',
         "render": lambda: st.status("処理中", expanded=True).write("ログ…")},
        {"name": "st.progress", "ver": (1, 0),
         "desc": "進捗バー。0.0〜1.0で指定。",
         "code": 'st.progress(0.6, text="progress")',
         "render": lambda: st.progress(0.6, text="progress")},
        {"name": "st.info / success / warning / error", "ver": (1, 0),
         "desc": "色付きアラート。v1.58で title 引数が追加。",
         "code": 'st.success("完了しました")',
         "render": lambda: st.success("完了しました")},
    ])

st.divider()
st.caption("Made for [UI Memo](https://ui-memo.com)")
