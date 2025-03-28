import os, re
import requests
import urllib.parse
from io import BytesIO

# PDF Library
import PyPDF2

# Sumy Library
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# from sumy.summarizers.luhn import LuhnSummarizer as Luhn
from sumy.summarizers.text_rank import TextRankSummarizer as TextRank
# from sumy.summarizers.lsa import LsaSummarizer as LSA

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# ----------------------------------------------------------------------------------------------------

def sumi(url):

    # Download the PDF from the URL
    response = requests.get(url)
    raw_data = response.content
    text = extract_pdf_file(raw_data)
    return sumy(text)

def pdf_sumi(pdf):

    pdf_bytes = pdf.read()
    text = extract_pdf_file(pdf_bytes)
    return sumy(text)

# ----------------------------------------------------------------------------------------------------

def sumy(text):

    # Configuration for Summarizer
    LANGUAGE = "english"
    SENTENCES_COUNT = 15

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    # Initialize the Summarisers
    summarizer = TextRank(stemmer)
    # summarizer = LSA(stemmer)
    # summarizer = Luhn(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    return summarizer(parser.document, SENTENCES_COUNT)

#------------------------------PDF Functions--------------------------------------------

def extract_pdf_file(pdf):

    # Use PyPDF2 to extract the text from the PDF
    text_pages = []
    with BytesIO(pdf) as data:
        pdf = PyPDF2.PdfReader(data)
        # Extract the text from each page and add it to the text_pages list
        for page in pdf.pages:
            text_pages.append(page.extract_text())
    
    # Join the list of text pages into a single string
    pdf_text = " ".join(text_pages)
    return pdf_text