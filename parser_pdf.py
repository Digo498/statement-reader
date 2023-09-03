import pdfplumber



def text_from_pdf(pdf_file, x_tolerance=2, init_y_top=440, reg_y_top=210):
    # Box format in (x_top, y_top, x_bot, y_bot)
    regular_page_box = (70, reg_y_top, 400, 730)
    initial_page_box = (70, init_y_top, 400, 730)

    text = ''
    # Open the PDF file
    with pdfplumber.open('statement.pdf') as pdf:
        for page in pdf.pages:
            if page.page_number == 1:
                rect = initial_page_box
            else:
                rect = regular_page_box

            # Extract text only from the specified rectangle
            text += page.crop(rect).extract_text(x_tolerance=x_tolerance)

    # Process the extracted text
    text = text.split('\n')
    return text 



