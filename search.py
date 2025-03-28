import requests
import urllib, urllib.request
import xml.etree.ElementTree as ET

def arxivSearch(query):
    
    # Set the base URL for the arXiv API
    base_url = "http://export.arxiv.org/api/query?"

    # Set the search parameters for the query
    search_params = {
        "search_query": query,  # the query itself
        "start": 0,  # the index of the first result to return
        "max_results": 5,  # the maximum number of results to return
    }

    # Encode the search parameters as a query string
    query_string = urllib.parse.urlencode(search_params)

    # Create the full URL by concatenating the base URL and the query string
    url = base_url + query_string

    # API call
    data = urllib.request.urlopen(url)
    papers = data.read().decode('utf-8')

    return papers

def responseXML(papers):
    # Parse the XML response
    root = ET.fromstring(papers)
    ns = { 'r':'http://www.w3.org/2005/Atom'}

    all_papers = list()
    entries = root.findall('r:entry',namespaces=ns)
    for entry in entries:
        authors = []
        for name in entry.findall('{*}author/{*}name'):
            authors.append(name.text)
        all_papers.append({
            l.tag[l.tag.index('}')+1:]: {
                'text': l.text,
                'attrib': l.attrib,
                'names': authors
            } for l in entry
        })

    return all_papers

