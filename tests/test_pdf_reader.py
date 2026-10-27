import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pdf_to_audio.pdf_reader import extract_text_from_pdf


class ExtractTextFromPdfTests(unittest.TestCase):
    def test_extracts_and_joins_page_text(self) -> None:
        fake_reader = SimpleNamespace(
            pages=[
                SimpleNamespace(extract_text=lambda: "Primeira pagina"),
                SimpleNamespace(extract_text=lambda: "Segunda pagina"),
            ]
        )
        fake_module = SimpleNamespace(PdfReader=lambda _: fake_reader)

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "documento.pdf"
            pdf_path.touch()
            with patch.dict(sys.modules, {"pypdf": fake_module}):
                result = extract_text_from_pdf(pdf_path)

        self.assertEqual(result, "Primeira pagina\n\nSegunda pagina")

    def test_rejects_pdf_without_extractable_text(self) -> None:
        fake_reader = SimpleNamespace(
            pages=[SimpleNamespace(extract_text=lambda: "  ")]
        )
        fake_module = SimpleNamespace(PdfReader=lambda _: fake_reader)

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "scan.pdf"
            pdf_path.touch()
            with patch.dict(sys.modules, {"pypdf": fake_module}):
                with self.assertRaisesRegex(ValueError, "OCR"):
                    extract_text_from_pdf(pdf_path)


if __name__ == "__main__":
    unittest.main()
