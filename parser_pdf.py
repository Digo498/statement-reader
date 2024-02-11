import pdfplumber
import re


def text_from_pdf(pdf_file, x_tolerance=2, init_y_top=440, reg_y_top=210):
    """
    Extracts text from a PDF file within specified rectangular regions on each page.

    Args:
        pdf_file (str): The path to the PDF file to extract text from.
        x_tolerance (int): Tolerance for x-axis alignment when extracting text.
        init_y_top (int): The y-coordinate of the top of the rectangular region on the initial page.
        reg_y_top (int): The y-coordinate of the top of the rectangular region on regular pages.

    Returns:
        list: A list of text lines extracted from the PDF.
    """
    # Box format in (x_top, y_top, x_bot, y_bot)
    regular_page_box = (70, reg_y_top, 400, 730)
    initial_page_box = (70, init_y_top, 400, 730)

    text = ''
    # Open the PDF file
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.page_number == 1:
                rect = initial_page_box
            else:
                rect = regular_page_box

            # Extract text only from the specified rectangle
            text += page.crop(rect).extract_text(x_tolerance=x_tolerance)

    # Process the extracted text
    lines = text.split('\n')
    return lines 



def get_transactions(pdf_lines):
    """
    Extracts transaction data from a list of text lines.

    Args:
        pdf_lines (list): A list of text lines extracted from a PDF.

    Returns:
        list: A list of dictionaries, each containing transaction information.
    """

    transactions = []

    pattern = r'(\w{3}\s+\d{1,2})\s+(.+) (\d+\.\d+)'

    for i, line in enumerate(pdf_lines):
        match = re.match(pattern, line)
        # print(line)
        if match:
            date = match.group(1)
            transaction_type = match.group(2)
            amount = match.group(3)

            # Create a dictionary for the transaction and add it to the list
            transaction = {
                'Date': date,
                'Transaction Type': transaction_type,
                'Amount': amount,
                'Name': pdf_lines[i+1],
            }
            transactions.append(transaction)

    return transactions 

def main():
    print('Starting...')
    pdf_file = 'statement_short.pdf'

    lines = text_from_pdf(pdf_file, x_tolerance=2, init_y_top=440, reg_y_top=210)
    transactions = get_transactions(lines)

    # print(transactions)



main()
