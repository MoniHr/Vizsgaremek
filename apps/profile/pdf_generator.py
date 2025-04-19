import os.path

import pdfkit


class PdfGenerator:
    __wkhtmltopdf = "/usr/local/bin/wkhtmltopdf"

    def __init__(self):
        self.__params = {
            # 'header-spacing': 3,
            # 'footer-spacing': 3,
            # 'margin-left': margin,
            # 'margin-right': margin,
            # 'no-outline': True,
            # 'dpi': 96,
            # 'disable-smart-shrinking': True
        }

    def generate(self, html_content: str):
        if not os.path.exists(self.__wkhtmltopdf):
            raise Exception("wkhtmltopdf not installed!")

        out = pdfkit.from_string(html_content, options=self.__params)
        return out
