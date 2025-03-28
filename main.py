import os
import openai
import PyPDF2
import requests
from io import BytesIO

# Sumy Library
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

from sumy.summarizers.text_rank import TextRankSummarizer as TextRank
# from sumy.summarizers.luhn import LuhnSummarizer as Luhn
# from sumy.summarizers.lsa import LsaSummarizer as LSA

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter


def extractPDF(pdf):

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


def gpt3(text):
    # Configuration
    model_engine = "text-davinci-003"
    temperature = 0.5 # Deterministic (0.0) to Random (1.0)
    choices = 1

    # Send the concatenated response to the API
    prompt = f"SENTENCES: {text}\
        \n\
        \n\
        Write a science paper essay summary from the SENTENCES,\
        Essay length at least 400 words."

    # Call the API and get the response
    response = openai.Completion.create(
        engine=model_engine, 
        prompt=prompt, 
        max_tokens=1000, 
        temperature=temperature,
        n=choices
        )

    return response["choices"][0]["text"]


if __name__ == "__main__":

    usage = "usage: %prog [options]"
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", \
                    dest="file", \
                    type=str, \
                    help="Required: Path to PDF file")

    parser.add_argument("-u", "--url", \
                    dest="url", \
                    type=str, \
                    help="Required: url to PDF")

    args = parser.parse_args()

    if args.url:
        response = requests.get(args.url)
        raw_data = response.content
        text = extractPDF(raw_data)
        sumied = sumy(text)

    elif args.file:
        file_path = args.file
        with open(file_path, 'rb') as pdf:
            raw_data = pdf.read()
        text = extractPDF(raw_data)
        sumied = sumy(text)

    else:
        print("Please provide either an URL (-u) or a file path (-f) to a PDF")

    print(gpt3(sumied))