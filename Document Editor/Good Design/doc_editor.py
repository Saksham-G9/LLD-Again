from abc import ABC, abstractmethod
from typing import Optional, Sequence


# Interfaces
class IElement(ABC):
    @abstractmethod
    def to_text(self) -> str: ...


class IPersistence(ABC):
    @abstractmethod
    def save(self, elements: Sequence[IElement]) -> None: ...


# Concrete Implementation
class TextElement(IElement):
    def __init__(self, data: str) -> None:
        self.data = data

    def to_text(self) -> str:
        return self.data


class ImageElement(IElement):
    def __init__(self, path: str) -> None:
        self.path = path

    def to_text(self) -> str:
        return f"[Image: {self.path}]"


class FilePersistence(IPersistence):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save(self, elements: Sequence[IElement]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            for el in elements:
                f.write(el.to_text() + "\n")


# Renderer abstraction
class Renderer(ABC):
    @abstractmethod
    def render(self, element: IElement) -> None: ...


class ConsoleRenderer(Renderer):
    def render(self, element: IElement) -> None:
        print(element.to_text())


class Document:
    def __init__(self) -> None:
        self._elements: list[IElement] = []

    def addElement(self, element: IElement) -> None:
        self._elements.append(element)

    def removeElement(self, element: IElement) -> None:
        if element in self._elements:
            self._elements.remove(element)

    def moveElement(self, from_index: int, to_index: int) -> None:
        n = len(self._elements)
        if n <= 1:
            return

        # normalize negative indices
        if from_index < 0:
            from_index += n
        if to_index < 0:
            to_index += n

        if not (0 <= from_index < n):
            raise IndexError("from_index out of range")
        if not (0 <= to_index <= n):
            raise IndexError("to_index out of range")

        el = self._elements.pop(from_index)
        if from_index < to_index:
            to_index -= 1

        self._elements.insert(to_index, el)

    def updateElement(self, index: int, new_element: IElement) -> bool:
        n = len(self._elements)
        if index < 0:
            index += n
        if 0 <= index < n:
            self._elements[index] = new_element
            return True
        return False

    @property
    def elements(self) -> Sequence[IElement]:
        return self._elements

    def render(self, renderer: Optional["Renderer"] = None) -> None:
        if renderer is None:
            renderer = ConsoleRenderer()
        for el in self._elements:
            renderer.render(el)

    def to_text(self) -> str:
        return "\n".join(el.to_text() for el in self._elements)


class DocumentEditor:
    def __init__(self, document: Document, persistence: IPersistence) -> None:
        self.document: Document = document
        self.persistence: IPersistence = persistence

    def addElement(self, element: IElement) -> None:
        self.document.addElement(element)

    def removeElement(self, element: IElement) -> None:
        self.document.removeElement(element)

    # Convenience, simpler names
    def add(self, element: IElement) -> None:
        self.addElement(element)

    def remove(self, element: IElement) -> None:
        self.removeElement(element)

    def move(self, from_index: int, to_index: int) -> None:
        self.document.moveElement(from_index, to_index)

    def update(self, index: int, new_element: IElement) -> bool:
        return self.document.updateElement(index, new_element)

    def save(self) -> None:
        self.persistence.save(self.document.elements)

    def render_document(self, renderer: Optional["Renderer"] = None) -> None:
        self.document.render(renderer)
