from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrai e combina o texto de todas as paginas de um PDF."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    text = "\n\n".join(
        page.extract_text() or ""
        for page in reader.pages
    ).strip()

    if not text:
        raise ValueError(
            "O PDF nao contem texto selecionavel. PDFs digitalizados precisam "
            "de OCR, que ainda nao esta incluido."
        )

    return text
