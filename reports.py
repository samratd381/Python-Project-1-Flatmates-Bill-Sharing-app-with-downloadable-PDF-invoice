import webbrowser
import os
from multiprocessing.connection import Client

from fpdf import FPDF



class PdfReport:
    """
    Creates a PDF file that contains data about the flatmates such as their
    names, their due amount and the period of the bill.

    """
    def __init__(self,filename):

        self.filename = filename

    def generate(self, flatmate1 , flatmate2, bill):

        flatmate1_pay = str(round(flatmate1.pays(bill, flatmate2), 2))
        flatmate2_pay = str(round(flatmate2.pays(bill, flatmate1), 2))


        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        #Add Image
        pdf.image(r"files/house.png", w=30, h=30)

        # insert Title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt="Flatmates Bill", border=1, align="C", ln=1)
        #insert Period label and value
        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=100, h=40, txt="Period:", border=1)
        pdf.cell(w=150, h=40, txt=bill.period, border=1, ln=1)

        #insert Name and the due amount of the first flatmate
        pdf.set_font(family='Times', size=12 )
        pdf.cell(w=100, h=25, txt=flatmate1.name, border=1)
        pdf.cell(w=150, h=25, txt=flatmate1_pay , border=1, ln=1)

        #insert Name and the due amount of the first flatmate
        pdf.cell(w=100, h=40, txt=flatmate2.name, border=1)
        pdf.cell(w=150, h=40, txt=flatmate2_pay , border=1, ln=1)

        #Change Directory to files , generate and open the pdf
        os.chdir("files")
        pdf.output(self.filename)
        webbrowser.open(self.filename)

# class FileSharer:
#
#     def __init__(self, filepath,api_key="AqpvYBwVYTamE8vx6DxZwz"):
#         self.filepath = filepath
#         self.api_key = api_key
#
#     def share(self):
#         client= Client(self.api_key)
#         new_filelink = client.upload(filepath = self.filepath)
#         return new_filelink.url
#
# from http.server import SimpleHTTPRequestHandler
# from socketserver import TCPServer
#
# class FileSharer:
#     def __init__(self, filepath):
#         self.filepath = filepath
#
#     def share(self):
#         server = TCPServer(("localhost", 8000), SimpleHTTPRequestHandler)
#         server.serve_forever()
#         return "File shared successfully."
import requests

class FileSharer:
    def __init__(self, filepath, api_key="AqpvYBwVYTamE8vx6DxZwz"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        url = "https://file.io"
        with open(self.filepath, "rb") as file:
            response = requests.post(url, files={"file": file})
        if response.status_code == 200:
            file_link = response.json()["link"]
            return f"File shared successfully. Download link: {file_link}"
        else:
            return "File sharing failed."
