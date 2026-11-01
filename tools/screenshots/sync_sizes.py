"""
ui-memo の Streamlit ページのカード画像（img の width / height）を、実際の PNG の大きさに合わせる。

撮り直すと画像の高さが変わることがあるので、画像を ui-memo にコピーしたあとに実行する。

    python tools/screenshots/sync_sizes.py ../ui-memo            # 書き換える
    python tools/screenshots/sync_sizes.py ../ui-memo --check    # ずれを表示するだけ

対象は app/categories/streamlit/*/page.tsx の
    src: "/images/streamlit/...png",
    alt: "...",
    width: 1200,
    height: 384,
の並び。
"""
import argparse
import re
import struct
import sys
from pathlib import Path

PATTERN = re.compile(
    r'(src: "(/images/streamlit/[^"]+\.png)",\n\s+alt: (?:"(?:[^"\\]|\\.)*"|\'[^\']*\'),\n\s+width: )'
    r"(\d+)(,\n\s+height: )(\d+)(,)"
)


def png_size(path):
    """PNG の幅と高さ（IHDR チャンク）を読む。"""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"PNG ではない: {path}")
    return struct.unpack(">II", head[16:24])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ui_memo", help="ui-memo リポジトリのパス")
    ap.add_argument("--check", action="store_true", help="書き換えずに、ずれだけ表示する")
    args = ap.parse_args()

    root = Path(args.ui_memo)
    pages = sorted(root.glob("app/categories/streamlit/*/page.tsx"))
    if not pages:
        sys.exit(f"Streamlit のページが見つからない: {root}")

    total = changed = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        srcs = re.findall(r'src: "(/images/streamlit/[^"]+)"', text)
        diffs = []

        def fix(m):
            w, h = png_size(root / "public" / m.group(2).lstrip("/"))
            if (int(m.group(3)), int(m.group(5))) != (w, h):
                diffs.append(f"{m.group(2)}  {m.group(3)}x{m.group(5)} -> {w}x{h}")
            return f"{m.group(1)}{w}{m.group(4)}{h}{m.group(6)}"

        new, n = PATTERN.subn(fix, text)
        if n != len(srcs):
            sys.exit(f"{page}: 画像 {len(srcs)} 件のうち {n} 件しか読めなかった（並びが想定と違う）")
        total += n
        changed += len(diffs)
        for d in diffs:
            print(f"{page.relative_to(root)}: {d}")
        if diffs and not args.check:
            page.write_text(new, encoding="utf-8")

    if args.check:
        print(f"\n画像 {total} 件のうち、サイズがずれているのは {changed} 件")
    else:
        print(f"\n画像 {total} 件のうち {changed} 件のサイズを書き換えた")
    if args.check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
