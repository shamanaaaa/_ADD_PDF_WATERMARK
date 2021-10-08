from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import datetime
import os
import time


input_path = "input"
export_path = "output"

while True:
    def create_canvas(height):
        today = datetime.now().strftime("%d.%m.%Y")
        c = canvas.Canvas('watermark.pdf')
        c.setFontSize(10)
        c.setFillColorRGB(1, 0, 0)
        c.setFont('Helvetica-Bold', 20)
        c.drawString(5, height - 17, f"Electronic invoice from: {today}")
        c.save()


    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            output_file = PdfFileWriter()

            with (open(input_path + '/' + file, "rb")) as f:
                input_file = PdfFileReader(f)
                page_count = input_file.getNumPages()

                for page_number in range(page_count):
                    if page_number == 0:
                        pdf_height = input_file.flattenedPages[0]["/MediaBox"][3]
                        create_canvas(int(pdf_height))
                        watermark = PdfFileReader(open("watermark.pdf", "rb"))
                        input_page = input_file.getPage(page_number)
                        input_page.mergePage(watermark.getPage(0))
                        output_file.addPage(input_page)
                        output_path = export_path + '/' + file.split('.pdf')[0] + '.pdf'
                    else:
                        input_page = input_file.getPage(page_number)
                        output_file.addPage(input_page)

                    with open(output_path, "wb") as outputStream:
                        output_file.write(outputStream)

    for file in os.listdir(input_path):
        os.remove(input_path + '/' + file)

    time.sleep(10)
