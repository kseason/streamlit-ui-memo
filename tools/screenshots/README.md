# スクリーンショットの撮影用アプリ

[UI Memo](https://www.ui-memo.com/categories/streamlit) の Streamlit ページ（`/categories/streamlit/*`）に載せるスクリーンショットを、まとめて撮り直すための道具。Streamlit の版を上げたときに使う。

- `app.py` … 1枚ごとの場面を描く Streamlit アプリ。`?s=<カテゴリ>/<名前>` で1場面だけを幅600pxの白い枠に描く
- `shoot.py` … Playwright で各場面を開き、必要な操作（入力・貼り付け・ダイアログを開くなど）をして撮る。幅1200pxの PNG になる
- `sync_sizes.py` … ui-memo のページに書いてある画像の width / height を、実際の画像の大きさに合わせる

テーマはプレイグラウンドと同じ（リポジトリのルートの `.streamlit/config.toml` が読まれる）。Streamlit の版もルートの `requirements.txt` と同じになるので、プレイグラウンドの版を上げてからこの手順を行う。

## 手順

リポジトリのルートで行う。

```bash
# 1. 準備（初回だけ）
python -m venv .venv && source .venv/bin/activate
pip install -r tools/screenshots/requirements.txt
python -m playwright install chromium

# 2. 撮影用アプリを起動（別のターミナルで）
streamlit run tools/screenshots/app.py --server.port 8603 --server.headless true

# 3. 全場面を撮る → tools/screenshots/out/ に保存される
python tools/screenshots/shoot.py

# 4. ui-memo にコピーして、ページの画像サイズを合わせる（ui-memo が隣にある場合）
cp -r tools/screenshots/out/* ../ui-memo/public/images/streamlit/
python tools/screenshots/sync_sizes.py ../ui-memo
```

一部だけ撮り直すときは、場面の名前を渡す（`python tools/screenshots/shoot.py charts/echarts_chart overlay/drawer`）。場面の名前は `app.py` の関数名（`charts_echarts_chart` → `charts/echarts_chart`）で、画像のファイル名と同じ。

## 注意

- **地図（`charts/map_chart`）はインターネットから地図のタイルを読む**。外に出られない環境（クラウドの作業環境など）では地図が白くなるので、`--skip charts/map_chart` を付けて撮り、地図だけは手元のPCで撮る
- 撮った画像は1枚ずつ目で確かめる（場面によっては、操作のタイミングで状態が変わる）
  - `chat/submit_mode` … 送信すると `app.py` 側がわざと実行中のまま止まり、停止ボタンが出た状態を撮る
  - `inputs/text_validate` … 検証のメッセージは入力欄右の (!) アイコンのツールチップに出るので、アイコンにマウスを載せて撮る
  - `feedback/status_step` … `st.status` を `with` で使うと抜けたときに自動で完了になるため、最後のステップだけ `with` を使わずに描いて実行中の見た目にしている
- 同じ版・同じテーマなら、撮り直しても画像はほぼ同じになる（1.66.1 で確かめたところ、46枚中44枚が完全に一致）。グラフ（`st.line_chart` などの Vega 系）だけは、読み込みのたびに軸の位置が数ピクセルずれることがある
- 新しいウィジェットの場面を足すときは、`app.py` に `<カテゴリ>_<名前>()` を書く（`shoot.py` が自動で拾う）。操作が要る場面は `shoot.py` の `prepare()` に追記する
- `out/` は git に入れない
