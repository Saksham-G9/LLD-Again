from doc_editor import Document, DocumentEditor, TextElement, ImageElement, FilePersistence
import os


def main() -> None:
    out_path = os.path.join(os.path.dirname(__file__), "demo_output.txt")
    doc = Document()
    persistence = FilePersistence(out_path)
    editor = DocumentEditor(doc, persistence)

    editor.addElement(TextElement("Hello from example_usage!"))
    editor.addElement(ImageElement("images/sample.png"))

    editor.render_document()
    editor.save()
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
