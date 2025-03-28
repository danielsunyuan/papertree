import os
import time
import requests

# Flask Framwork
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Import Modules from other files
from gpt3 import essayAI, chatAI
from helpers import sumi, pdf_sumi
from search import arxivSearch, responseXML

import urllib, urllib.request

# Configure application
app = Flask(__name__)

root_dir = os.path.dirname(os.path.abspath(__file__))

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#-----------------------------------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    
    return render_template("index.html")
    

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == 'GET':
            return render_template("upload.html")

#--------------------------------------------------------- SEARCH --------------------------------------------
@app.route('/search', methods=['GET', 'POST'])
def search():

    try:
        # Get the query from the form
        query = request.args.get("search")
        print(f'query = {query}')

        # Perform the search
        papers = arxivSearch(query)
        
        # Extract the data from the XML response
        all_papers = responseXML(papers)

        # Render the template and pass the extracted data to it
        return render_template('search.html', response=all_papers)

    except KeyError:
        # Handle the case where the query is not present in the form data
        return render_template("index.html", response='Invalid Search')


@app.route('/summary', methods=['GET','POST'])
def summary():
    if request.method == 'POST':
        # Get the url and title from the request form
        url = request.form.get('url')
        title = request.form.get('title')

        # Sumi the url
        print('starting SUMI')
        sumied = sumi(url)
        print(sumied)

        try:
            # Perform the summarization
            print('starting AI')
            essay = essayAI(sumied)
            print(essay)

            # Dictionary to hold the paper data
            paper = {
                "title": title,
                "link": url,
                "summary": essay
            }

            # Render the summary template
            return render_template("summary.html", paper=paper)

        except Exception as e:
            return redirect('/error')


    elif request.method == 'GET':

        return redirect('/')


#--------------------------------------------------------- PDF UPLOAD --------------------------------------------
@app.route('/process_pdf', methods=['POST'])
def process_pdf():

    if request.method == 'POST':

        # Get the uploaded PDF file from the request
        pdf_file = request.files['file']

        # Read the PDF file and extract the text
        print('starting SUMI')
        text = pdf_sumi(pdf_file)
        print(text)
        
        try:
            # Perform the summarization
            print('starting AI')
            essay = essayAI(text)
            print(essay)

            # Dictionary to hold the paper data
            paper = {
                "title": "Summary:",
                "link": "",
                "summary": essay
            }

            # Render the summary template
            return render_template("summary.html", paper=paper)

        except Exception as e:
            return redirect('/error')

        return render_template("upload.html", response=response)

    elif request.method == 'GET':

        return redirect("/")


@app.route('/chat', methods=['POST'])
def chat():

    # Get the user's input from the request
    user_input = request.json["user_input"]

    # Get the user's input from the request
    paper_summary = request.json["paper_summary"]

    # Get the chatbot's response
    AIresponse = chatAI(user_input, paper_summary)

    # Return the chatbot's response in JSON format
    return jsonify(AIresponse=AIresponse)


#-----------------------------------------------------------------------------------------------------    

@app.route('/test', methods=['GET'])
def test():

    return render_template("test.html")


if __name__ == '__main__':
        #port = int(os.environ.get("PORT", 5000))
        #app.run(host='0.0.0.0', port=port, debug=True)
        #app.run(host='127.0.0.1', port=8080, debug=True)
        app.run()