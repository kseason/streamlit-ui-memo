# UI Memo ─ Streamlit ウィジェット網羅カタログ（ライブ・プレイグラウンド）

Streamlit Community Cloud（`ui-memo.streamlit.app`）で公開するソース一式。
[UI Memo](https://ui-memo.com) の記事から「▶ 実際に触ってみる」で誘導するライブ版。

## 構成
```
streamlit_app.py        # カタログ本体（最新 1.58）
requirements.txt        # streamlit==1.58.0, pandas
.streamlit/config.toml  # テーマ（ui-memo寄せ。色は差し替え前提）
```

## 中身の特徴
- **導入バージョンをTierバッジで明記**（Kの要件：古い環境で使えるか即判断）
  - Tier A（アンバー・新しめ／要確認）: v1.37以降
  - Tier B（グレー・中堅）: v1.23〜v1.32
  - Tier C（緑・広く使える）: ごく初期から安定
- 各カテゴリは**導入バージョンの新しい順**に並ぶ（最新UI優先）。
- 各ウィジェット = 動く本体 ＋ コード ＋ 短い解説 ＋（関連あれば）ui-memoリンク。
- 主役は データ表示・編集 / チャート / チャット を前方タブに配置。
- 上部に「v1.58で動作中」表示＋リアルタイム反応ショーケース。

## デプロイ（既存アプリの更新）
すでに `ui-memo.streamlit.app` を作成済みなら、繋いだGitHubリポジトリに
この3ファイルを push（上書き）するだけで自動再デプロイされる。

## 仕上げ前の2つの宿題
1. **配色の確定**：`streamlit_app.py` 冒頭の色定数（ACCENT 等）と
   `.streamlit/config.toml` の `[theme]` を、ui-memo.com の正確なブランド色に差し替える。
   現状はパステルの仮置き。color定数は1か所に集約済みなので置換は容易。
2. **ui-memoクロスリンクのURL**：`UIMEMO` 辞書に確認済みURL（pagination / slider）のみ記載。
   他は `# 要URL確認` コメントで保留。公開前に実URLを確認して追記する
   （当て推量のリンクは入れない方針）。

## 更新の流れ
ウィジェット追加・修正は `streamlit_app.py` を編集して push するだけ。
チャット版Claudeが編集 → K が push → 自動再デプロイ。
本文・スクショ（クロール/AI可視の本編）は ui-memo.com 側に置き、ここは「触る場」に徹する。
