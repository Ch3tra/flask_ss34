import os
from datetime import datetime

import pdfkit as pdfkit
from flask import Blueprint, render_template, request, Response
from flask_login import login_required

poss = Blueprint('poss', __name__)


@poss.route('/pos')
@login_required
def pos():
    return render_template('admin/pos.html')


# Get the wkhtmltopdf path from environment variable or set a default value for Windows
if os.name == 'nt':  # Check if the OS is Windows
    wkhtmltopdf_path = os.getenv('WKHTMLTOPDF_PATH', 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
else:
    # For non-Windows systems, default path
    wkhtmltopdf_path = os.getenv('WKHTMLTOPDF_PATH', 'wkhtmltopdf')

# Set the path to the wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


@poss.route("/pdf")
def index_pdf():
    path = os.path.join(os.getcwd(), 'pdf', 'invoice.pdf')  # Use os.path.join for path concatenation
    if not os.path.exists(path):
        os.makedirs(os.path.join(os.getcwd(), 'pdf'))  # Create the directory using os.path.join

    data = [
        {'id': 1, 'name': 'កូកាកូឡា', 'qty': 20, 'price': 0.25},
        {'id': 1, 'name': 'sting', 'qty': 10, 'price': 0.25},
        {'id': 1, 'name': 'abc', 'qty': 3, 'price': 25},
        {'id': 1, 'name': 'Anchor', 'qty': 6, 'price': 25},
        {'id': 1, 'name': 'KRUD', 'qty': 4, 'price': 25},
        {'id': 1, 'name': 'VATANAK', 'qty': 1, 'price': 25},
        {'id': 1, 'name': 'DRAGON', 'qty': 2, 'price': 25},
    ]
    now = datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M")
    server_url = request.url_root
    html = render_template("invoice.html", data=data, now=created_at, server_url=server_url)
    options = {
        # A5:21*14.8cm
        'page-height': '21cm',
        'page-width': '14.8cm',
        'margin-top': '0.1in',
        'margin-right': '0in',
        'margin-bottom': '0.1in',
        'margin-left': '0in',
    }

    # Save the PDF to the specified path
    pdfkit.from_string(html, path, options=options, configuration=config)

    with open(path, 'rb') as pdf_file:
        pdf_preview = pdf_file.read()

    return Response(pdf_preview, mimetype="application/pdf")
