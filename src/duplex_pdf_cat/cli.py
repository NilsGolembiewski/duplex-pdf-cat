import click
from pypdf import PdfReader, PdfWriter


def process_pdf(input_path: str, writer: PdfWriter) -> None:
    """
    Read a PDF file, ensure it has an even number of pages by adding a blank page if necessary,
    and append all its pages to the provided PdfWriter instance.

    Args:
        input_path (str): Path to the input PDF file.
        writer (PdfWriter): A PdfWriter instance to which pages are appended.
    """
    reader = PdfReader(input_path)
    pages = reader.pages
    # Append each page to the writer
    for page in pages:
        writer.add_page(page)
    # If the PDF has an odd number of pages, add a blank page
    if len(pages) % 2 != 0:
        last_page = pages[-1]
        width = last_page.mediabox.width
        height = last_page.mediabox.height
        writer.add_blank_page(width=width, height=height)


@click.command()
@click.option(
    '--output', '-o',
    required=True,
    type=click.Path(writable=True),
    help="Path to the output concatenated PDF file."
)
@click.argument(
    'input_files',
    nargs=-1,
    type=click.Path(exists=True),
)
def main(output: str, input_files: tuple) -> None:
    """
    Concatenate multiple PDF files into a single PDF suitable for duplex printing.

    For each input PDF, if it has an odd number of pages, a blank page is added.
    Then, all PDFs are concatenated into one output file.
    """
    if not input_files:
        click.echo("No input files provided.")
        return

    writer = PdfWriter()

    for input_file in input_files:
        click.echo(f"Processing {input_file}...")
        process_pdf(input_file, writer)

    with open(output, "wb") as out_file:
        writer.write(out_file)

    click.echo(f"Concatenated PDF written to {output}")


if __name__ == '__main__':
    main()
