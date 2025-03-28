import os, re, io
import urllib.request
import requests

import openai
openai.api_key = os.environ.get('OPENAI_API_KEY')


# PDF Library
import PyPDF2

# Sumy Library
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# Sumy Summarizers Algorithms
from sumy.summarizers.luhn import LuhnSummarizer as Luhn
from sumy.summarizers.text_rank import TextRankSummarizer as TextRank
from sumy.summarizers.edmundson import EdmundsonSummarizer as Edmundson
from sumy.summarizers.lsa import LsaSummarizer as LSA

# Sumy Stemmers
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words




def extract_pdf(url):

    # Download the PDF from the URL
    response = requests.get(url)
    raw_data = response.content
    print('PDF downloaded successfully\n')

    # Use PyPDF2 to extract the text from the PDF
    text_pages = []
    page_count = 0
    with io.BytesIO(raw_data) as data:
        # Create a PDF object
        pdf = PyPDF2.PdfReader(data)

        # Extract the text from each page and add it to the text_pages list
        for page in pdf.pages:
            text_pages.append(page.extract_text())
            page_count += 1

    return text_pages, page_count

#----------------------------------------------#----------------------------------------------
def sumi_options(url):

    # Download & extract the PDF from the URL
    text_pages, page_count = extract_pdf(url)

    summary = []
    
    for page in text_pages:

        # Configuration for Summarizer
        LANGUAGE = "english"
        SENTENCES_COUNT = 5

        # Create a plaintext parser and stemmer for a given language
        parser = PlaintextParser.from_string(page, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        
        # Luhn Method
        print("\n====== Luhn ======")
        summarizerLuhn = Luhn(stemmer)
        summarizerLuhn.stop_words = get_stop_words(LANGUAGE)

        for sentenceLuhn in summarizerLuhn(parser.document, SENTENCES_COUNT):
            print(sentenceLuhn, "\n")


        # TextRank Method
        print("====== TextRank ======")
        summarizerTR = TextRank(stemmer)
        summarizerTR.stop_words = get_stop_words(LANGUAGE)

        for sentenceTR in summarizerTR(parser.document, SENTENCES_COUNT):
            print(sentenceTR, "\n")


        # LSA Method
        print("====== LSA ======")
        summarizerLSA = LSA(stemmer)
        summarizerLSA.stop_words = get_stop_words(LANGUAGE)

        for sentenceLSA in summarizerLSA(parser.document, SENTENCES_COUNT):
            print(sentenceTR, "\n")


        #for sentence in summarizer(page,SENTENCES_COUNT):
            #page_sum += str(sentence)

        #summary.append(page_sum)


    return

#----------------------------------------------#----------------------------------------------

def sumi_default(url):

    # Download & extract the PDF from the URL
    text_pages, page_count = extract_pdf(url)

    summary = []
    
    for page in text_pages:

        # Configuration for Summarizer
        LANGUAGE = "english"
        SENTENCES_COUNT = 5

        parser = PlaintextParser.from_string(page, Tokenizer(LANGUAGE))

        # Initialize the stemmer, then summarizer, then stop words
        stemmer = Stemmer(LANGUAGE)
        summarizer = LSA(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        page_sum = ""

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            page_sum += str(sentence)
            print('-----------------default-----------------')
            print(sentence)
            print()

        summary.append(page_sum)

    return summary


def sumi_sumi(url):

    # Download & extract the PDF from the URL
    text_pages, page_count = extract_pdf(url)

    summary = []
    
    for page in text_pages:

        # Configuration for Summarizer
        LANGUAGE = "english"
        SENTENCES_COUNT = 5

        parser = PlaintextParser.from_string(page, Tokenizer(LANGUAGE))

        # Initialize the stemmer, then summarizer, then stop words
        stemmer = Stemmer(LANGUAGE)
        summarizer = TextRank(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        page_sum = ""

        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            page_sum += str(sentence)
            print()
            print(sentence)
            print()

        summary.append(page_sum)

    return summary

#----------------------------------------------#----------------------------------------------
def x(text):
    count = 0
    for t in text:
        print(count)
        print(t)
        count += 1
        print()
        
def openai_api(text):
    # Configuration
    model_engine = "text-davinci-003"
    temperature = 0.9 # Deterministic (0.0) to Random (1.0)
    choices = 1

    # Prompt Design
    prompt = f"{text}\
            \n\
            \n\
            Write the above into a profesional essay.\n"

    # Call the API and get the response
    response = openai.Completion.create(
        engine=model_engine, 
        prompt=prompt, 
        max_tokens=1024, 
        temperature=temperature,
        n=choices
        )
    
    print(response["choices"][0]["text"])


if __name__ == "__main__":
    #url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))

    url = "https://arxiv.org/pdf/astro-ph/9912320v1.pdf"
    #text = sumi_options(url)
    #text = sumi_default(url)
    text = sumi_sumi(url)



