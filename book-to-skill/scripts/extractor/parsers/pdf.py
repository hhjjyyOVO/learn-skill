import shutil
import subprocess


def extract_with_pdftotext(pdf_path: str) -> str | None:
    if not shutil.which("pdftotext"):
        return None
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except Exception:
        pass
    return None


def extract_with_pypdf2(pdf_path: str) -> str | None:
    try:
        import PyPDF2
        text_parts = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                try:
                    text_parts.append(page.extract_text() or "")
                except Exception:
                    text_parts.append("")
        return "\n".join(text_parts)
    except ImportError:
        return None
    except Exception:
        return None


def extract_with_pdfminer(pdf_path: str) -> str | None:
    try:
        from pdfminer.high_level import extract_text
        return extract_text(pdf_path)
    except ImportError:
        return None
    except Exception:
        return None


def extract_with_docling(pdf_path: str) -> str | None:
    """Layout-aware extraction using Docling. Best for technical books with tables and code."""
    try:
        from docling.document_converter import DocumentConverter
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import PdfFormatOption

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        result = converter.convert(pdf_path)
        return result.document.export_to_markdown()
    except ImportError:
        return None
    except Exception:
        return None


def extract_with_opendataloader_pdf(pdf_path: str) -> str | None:
    """Extract using opendataloader-pdf. Produces AI-ready Markdown with structure
    (tables, headers, lists) preserved. Works locally, no API key or GPU needed.
    Returns None for scanned/image-only PDFs (falls through to OCR-capable methods)."""
    try:
        import opendataloader_pdf
        import tempfile
        import os
        import re

        tmpdir = tempfile.mkdtemp(prefix="odl_")
        try:
            opendataloader_pdf.convert(
                input_path=[pdf_path],
                output_dir=tmpdir,
                format="markdown",
            )
            for fname in os.listdir(tmpdir):
                if fname.lower().endswith(".md"):
                    md_path = os.path.join(tmpdir, fname)
                    with open(md_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    # Heuristic: if >80% of non-empty lines are image references,
                    # this is likely a scanned PDF — return None to fall through.
                    lines = [l for l in text.splitlines() if l.strip()]
                    if not lines:
                        return None
                    image_lines = sum(1 for l in lines if re.match(r'!\[image \d+\]', l.strip()))
                    if len(lines) > 0 and image_lines / len(lines) > 0.8:
                        return None  # scanned PDF, let Docling OCR handle it
                    return text
        finally:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
    except ImportError:
        return None
    except Exception:
        return None


def extract_with_pagewise_ocr(pdf_path: str) -> str | None:
    """Page-by-page OCR for scanned PDFs. Renders each page with pypdfium2,
    OCRs with rapidocr, and combines results. Memory-safe for large documents."""
    try:
        import pypdfium2 as pdfium
        from rapidocr import RapidOCR
    except ImportError:
        return None

    try:
        pdf = pdfium.PdfDocument(pdf_path)
        total = len(pdf)
        if total == 0:
            return None

        engine = RapidOCR()
        text_parts = []

        for i in range(total):
            page = pdf[i]
            bitmap = page.render(scale=2.0)
            pil_image = bitmap.to_pil()
            output = engine(pil_image)
            if output is not None and hasattr(output, 'txts') and output.txts:
                page_text = "\n".join(output.txts)
                text_parts.append(page_text)
            else:
                text_parts.append("")
            if (i + 1) % 10 == 0 or i == total - 1:
                print(f"  OCR {i + 1}/{total} pages")

        pdf.close()
        return "\n\n".join(text_parts)
    except Exception:
        return None


def count_pages(pdf_path: str) -> int:
    # Try pdfinfo first
    if shutil.which("pdfinfo"):
        try:
            result = subprocess.run(
                ["pdfinfo", pdf_path], capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.splitlines():
                if line.startswith("Pages:"):
                    return int(line.split(":")[1].strip())
        except Exception:
            pass
    # Fallback: count form-feed chars (pdftotext -layout uses \f between pages)
    try:
        import PyPDF2
        with open(pdf_path, "rb") as f:
            return len(PyPDF2.PdfReader(f).pages)
    except Exception:
        return 0
