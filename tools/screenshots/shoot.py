"""
撮影用アプリ（app.py）の各場面を撮って、ui-memo 用の PNG にする。

    python tools/screenshots/shoot.py                       # app.py の全場面
    python tools/screenshots/shoot.py charts/echarts_chart  # 指定した場面だけ
    python tools/screenshots/shoot.py --skip charts/map_chart

事前に app.py を起動しておくこと（README 参照）。
出力は既定で tools/screenshots/out/<カテゴリ>/<名前>.png（git には入れない）。
"""
import argparse
import ast
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CATEGORIES = ("data", "charts", "chat", "inputs", "overlay", "feedback")


def scenes_from_app():
    """app.py の <カテゴリ>_<名前>() 関数から場面の一覧を作る（場面の定義は app.py だけに置く）。"""
    tree = ast.parse((HERE / "app.py").read_text(encoding="utf-8"))
    scenes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            cat, _, name = node.name.partition("_")
            if cat in CATEGORIES and name:
                scenes.append(f"{cat}/{name}")
    return scenes


def blur(page):
    page.evaluate("() => { if (document.activeElement) document.activeElement.blur(); }")


# スクリプトの実行が終わり、読み込み中の仮の枠（表やグラフの部品を読み込む間の stSkeleton）が消えるまで待つ。
# st.skeleton 自体は stSkeletonElement なので、この条件には掛からない
READY_JS = """() => !document.querySelector('[data-testid="stStatusWidgetRunningIcon"]')
              && !document.querySelector('[data-testid="stSkeleton"]')"""


def wait_ready(page, settle_ms):
    page.wait_for_timeout(1500)
    page.wait_for_function(READY_JS, timeout=30000)
    page.wait_for_timeout(settle_ms)


# 入力欄に画像を貼り付ける（ClipboardEvent に File を載せて送る）
PASTE_IMAGE_JS = """
async () => {
  const ta = document.querySelector('[data-testid="stChatInputTextArea"]');
  const c = document.createElement('canvas'); c.width = 240; c.height = 160;
  const g = c.getContext('2d');
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, 240, 160);
  g.fillStyle = '#cc0000';
  [40, 70, 55, 95, 120].forEach((h, i) => g.fillRect(20 + i * 42, 150 - h, 28, h));
  const blob = await new Promise((r) => c.toBlob(r, 'image/png'));
  const file = new File([blob], 'graph.png', { type: 'image/png' });
  const dt = new DataTransfer(); dt.items.add(file);
  ta.focus();
  ta.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
}
"""


def prepare(page, scene):
    """場面ごとの操作。撮る対象（locator）を返す。None なら画面全体を撮る。"""
    target = page.locator(".st-key-shot")
    if scene == "chat/submit_mode":
        # 送信すると、app.py 側が実行中のまま止まる → 停止ボタンが出た状態を撮る
        ta = page.locator('[data-testid="stChatInputTextArea"]')
        ta.fill("Streamlit の使い方を教えて")
        ta.press("Enter")
        page.wait_for_timeout(2500)
    elif scene == "chat/paste_file":
        page.evaluate(PASTE_IMAGE_JS)
        page.wait_for_timeout(1500)
        page.locator('[data-testid="stChatInputTextArea"]').fill("このグラフの傾向を教えて")
        page.wait_for_timeout(800)
        blur(page)
        page.wait_for_timeout(500)
    elif scene == "inputs/text_validate":
        em = page.get_by_label("メール")
        em.fill("taro@example.com")
        em.press("Enter")
        page.wait_for_timeout(1200)
        zip_input = page.get_by_label("郵便番号")
        zip_input.fill("1234567")
        zip_input.press("Enter")
        page.wait_for_timeout(1200)
        blur(page)
        page.wait_for_timeout(800)
        # 検証のメッセージは入力欄右の (!) アイコンのツールチップに出る
        box = page.locator('[data-testid="stTextInput"]').nth(1).locator("svg").last.bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(1200)
    elif scene == "inputs/text_live":
        page.get_by_label("ライブラリを検索").click()
        page.keyboard.type("ch", delay=80)  # Enter を押さずに打つだけ（live=True）
        page.wait_for_timeout(2500)
        blur(page)
        page.wait_for_timeout(800)
    elif scene == "overlay/dialog":
        page.wait_for_selector('[role="dialog"]')
        page.wait_for_timeout(800)
        blur(page)  # 閉じるボタンのフォーカス枠を消す
        target = page.locator('[role="dialog"]').first
    elif scene == "overlay/popover":
        page.get_by_role("button", name="設定").click()
        page.wait_for_timeout(1200)
        blur(page)
        target = page.locator('[data-testid="stPopoverBody"]').first
    elif scene == "overlay/drawer":
        page.wait_for_selector('[role="dialog"]')
        page.wait_for_timeout(1200)
        blur(page)
        target = None
    elif scene == "feedback/toast":
        page.wait_for_selector('[data-testid="stToast"]')
        page.wait_for_timeout(800)
        target = page.locator('[data-testid="stToast"]').first
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenes", nargs="*", help="撮る場面（省略時は app.py の全場面）")
    ap.add_argument("--base", default="http://localhost:8603", help="撮影用アプリの URL")
    ap.add_argument("--out", default=str(HERE / "out"), help="出力先のフォルダ")
    ap.add_argument("--skip", nargs="*", default=[], help="撮らない場面")
    args = ap.parse_args()

    all_scenes = scenes_from_app()
    unknown = [s for s in args.scenes if s not in all_scenes]
    if unknown:
        sys.exit(f"app.py に無い場面: {', '.join(unknown)}")
    scenes = [s for s in (args.scenes or all_scenes) if s not in args.skip]
    out = Path(args.out)
    failed = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # 起動直後の1回目は部品の読み込みが遅く、表が描かれる前に撮ってしまうので、先に1度開いておく
        warm = browser.new_page()
        warm.goto(f"{args.base}/?s=data/dataframe", wait_until="load", timeout=120000)
        wait_ready(warm, 1000)
        warm.close()
        for scene in scenes:
            drawer = scene == "overlay/drawer"
            # ドロワーは背景のページごと撮る（幅1000px×1.2倍＝1200px）。ほかは枠を2倍で撮る
            ctx = browser.new_context(
                viewport={"width": 1000, "height": 560} if drawer else {"width": 900, "height": 1100},
                device_scale_factor=1.2 if drawer else 2,
            )
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)[:160]))
            page.goto(f"{args.base}/?s={scene}", wait_until="load", timeout=120000)
            try:
                # グラフは描画のアニメーションが終わるまで少し長めに待つ
                wait_ready(page, 3000 if scene.startswith("charts/") else 1500)
                target = prepare(page, scene)
                file = out / f"{scene}.png"
                file.parent.mkdir(parents=True, exist_ok=True)
                if target is None:
                    page.screenshot(path=str(file), animations="disabled")
                else:
                    target.scroll_into_view_if_needed()
                    target.screenshot(path=str(file), animations="disabled")
                # app.py の例外（場面の中の例外・構文エラーのダイアログ）を拾う
                exc = page.locator('[data-testid="stException"]').all_inner_texts()
                if page.get_by_text("Script execution error").count():
                    exc.append("Script execution error")
                status = "EXCEPTION " + " / ".join(t[:160] for t in exc) if exc else "ok"
            except Exception as e:  # noqa: BLE001 — 1場面の失敗で全体を止めない
                status = f"FAILED {str(e).splitlines()[0][:160]}"
            if status != "ok" or errors:
                failed.append(scene)
            print(scene, status, ("pageerror " + " / ".join(errors)) if errors else "")
            ctx.close()
        browser.close()

    print(f"\n{len(scenes) - len(failed)}/{len(scenes)} 場面を {out} に保存")
    if failed:
        sys.exit("失敗した場面: " + ", ".join(failed))


if __name__ == "__main__":
    main()
