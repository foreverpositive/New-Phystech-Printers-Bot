import os
import json
import textwrap
from fpdf import FPDF
from PIL import Image
import cups


def add_printers():
    with open('printers/printers.json', 'r', encoding='utf-8') as file:
        printers = json.load(file)

    for printer in printers.items():
        name = printer[0]
        location = printer[1]['Location']
        model = printer[1]['Model']
        domain = printer[1]['Domain']
        os.system(f'lpadmin -p "{name}" -L "{location}" -D "{model}" -E -v http://{domain}')


def pdf_from_text(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 11
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Helvetica', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename+'.pdf', 'F')

    return filename + '.pdf'


def pdf_from_images(images, filename):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=10)

    for image in images:
        pdf.add_page()
        img = Image.open(image)
        img = img.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
        pdf.image(img, x=0, y=0, h=297)

    pdf.output(filename+'.pdf', 'F')

    return filename + '.pdf'


def print_file(path, printer):
    conn = cups.Connection()
    # printers = conn.getPrinters()
    title = path.split('/')[-1]
    # printer = printer if list(printer.keys()) else list(printers.keys())[0]
    if os.path.isfile(path):
        conn.printFile(printer, path, title, {})
