# scripts/patch_nook_upload_flow_ux.py — Streamlines Reading Nook empty state to a connected Download -> Upload 2-step journey
# Usage: python3 scripts/patch_nook_upload_flow_ux.py
# Requires: Python 3.8+ (standard library only)

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES_TO_PATCH = [
    ROOT / "bookshelf" / "reader.html",
    ROOT / "docs" / "reader.html"
]

OLD_JS_TARGET = """    const hasDownloadTarget = directDownloadUrl || (driveUrl && (driveUrl.includes('/d/') || driveUrl.includes('id=')));
    if (!hasDownloadTarget && !driveUrl) {
      if (downloadDirectBtn) {
        downloadDirectBtn.style.display = 'none';
      }
    } else {
      if (downloadDirectBtn) {
        downloadDirectBtn.style.display = 'flex';
      }
      if (downloadBtnLabel) downloadBtnLabel.innerText = `Download "${bookTitle}.epub" Directly`;
    }"""

NEW_JS_TARGET = """    const hasDownloadTarget = directDownloadUrl || (driveUrl && (driveUrl.includes('/d/') || driveUrl.includes('id=')));
    const downloadFlowWrapper = document.getElementById('downloadFlowWrapper');
    if (!hasDownloadTarget && !driveUrl) {
      if (downloadFlowWrapper) downloadFlowWrapper.style.display = 'none';
    } else {
      if (downloadFlowWrapper) downloadFlowWrapper.style.display = 'block';
      if (downloadBtnLabel) {
        downloadBtnLabel.innerText = (bookTitle && bookTitle !== 'Untitled Book')
          ? `Download "${bookTitle}.epub"`
          : 'Download Ebook';
      }
    }"""

def patch_file(f: Path):
    print(f"Patching JS in {f}...")
    content = f.read_text(encoding="utf-8")

    if OLD_JS_TARGET in content:
        content = content.replace(OLD_JS_TARGET, NEW_JS_TARGET, 1)
        print("  ✓ Updated JS initialization for downloadFlowWrapper")
    else:
        print("  ⚠ Could not find exact OLD_JS_TARGET")

    f.write_text(content, encoding="utf-8")
    print(f"  ✓ Saved {f}")

def main():
    for f in FILES_TO_PATCH:
        if f.exists():
            patch_file(f)
        else:
            print(f"File not found: {f}")

if __name__ == "__main__":
    main()
