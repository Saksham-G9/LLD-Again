class DocumentEditor:
    _elements = []

    def add_text(self, text: str):
        self._elements.append(text)

    def add_image(self, path: str):
        self._elements.append(path)

    def render_document(self): 
        """Return a simple rendered representation of the document.
        Image file paths (by extension) are rendered as `[Image: path]`.
        """
        rendered_lines = []
        image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
        for el in self._elements:
            if isinstance(el, str) and el.lower().endswith(image_exts):
                rendered_lines.append(f"[Image: {el}]")
            else:
                rendered_lines.append(str(el))
        return '\n'.join(rendered_lines)

    def save_to_file(self):
        """Save the rendered document to 'document.txt' in the current directory.
        Returns the path of the saved file.
        """
        file_path = 'document.txt'
        content = self.render_document()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
