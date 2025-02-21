from pathlib import Path

from pypdf import PdfReader, PdfWriter
from click.testing import CliRunner

# Import the CLI main function from your module.
# Adjust the import below if your module name is different.
from duplex_pdf_cat.cli import main


def create_sample_pdf(num_pages: int, file_path: Path) -> None:
    """
    Create a simple PDF with the given number of blank pages.
    Each page is generated with a standard A4 size.
    """
    writer = PdfWriter()
    # A4 dimensions in points: 595.28 x 841.89 (approx)
    for _ in range(num_pages):
        writer.add_blank_page(width=595.28, height=841.89)
    with file_path.open("wb") as f:
        writer.write(f)


def get_pdf_page_count(file_path: Path) -> int:
    """Return the number of pages in the PDF at file_path."""
    reader = PdfReader(str(file_path))
    return len(reader.pages)


def test_single_even_pdf(tmp_path: Path):
    """
    Test that a single PDF with an even number of pages remains unchanged.
    Here, we generate a PDF with 2 pages and expect the output to have 2 pages.
    """
    # Create a sample even-page PDF
    pdf_file = tmp_path / "even.pdf"
    create_sample_pdf(2, pdf_file)

    # Define the output file path
    output_pdf = tmp_path / "output_even.pdf"

    # Invoke the CLI tool using Click's CliRunner
    runner = CliRunner()
    result = runner.invoke(main, ["--output", str(output_pdf), str(pdf_file)])
    assert result.exit_code == 0, result.output

    # Check that the output PDF has 2 pages (even remains unchanged)
    page_count = get_pdf_page_count(output_pdf)
    assert page_count == 2, f"Expected 2 pages, got {page_count}"


def test_multiple_pdf_mixed(tmp_path: Path):
    """
    Test concatenation of multiple PDFs with mixed parity.
    Here, we generate:
      - one PDF with 3 pages (odd) which should get an extra blank page (total 4),
      - one PDF with 2 pages (even) which remains unchanged.
    The concatenated output should have 4 + 2 = 6 pages.
    """
    odd_pdf = tmp_path / "odd.pdf"
    even_pdf = tmp_path / "even.pdf"
    create_sample_pdf(3, odd_pdf)
    create_sample_pdf(2, even_pdf)

    output_pdf = tmp_path / "output_mixed.pdf"

    runner = CliRunner()
    result = runner.invoke(
        main, ["--output", str(output_pdf), str(odd_pdf), str(even_pdf)]
    )
    assert result.exit_code == 0, result.output

    page_count = get_pdf_page_count(output_pdf)
    assert page_count == 6, f"Expected 6 pages, got {page_count}"
