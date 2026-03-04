from pathlib import Path
import sys

# Ensure current directory is on sys.path so imports work when running from elsewhere
sys.path.insert(0, str(Path(__file__).parent))

from doc_editor import DocumentEditor


def main():
    editor = DocumentEditor()
    editor.add_text("Title: Demo Document")
    editor.add_text("This document demonstrates adding images and text.")
    editor.add_image("image.png")
    editor.add_image("image2.png")
    editor.add_image("image1.png")

    print("Rendered document:\n")
    print(editor.render_document())

    saved = editor.save_to_file()
    print(f"\nSaved output to: {saved}")


if __name__ == "__main__":
    main()
