from typing import Optional
import click
import http.server
import socketserver

from pymed import PubMed
import openai


def query_pubmed(topic: str, max_results: Optional[int] = 10) -> str:
    """
    Get abstracts for a topic from pubmed
    """
    pubmed = PubMed(tool="pmg", email="arokem@uw.edu")
    pm_results = list(pubmed.query(topic, max_results=max_results))
    abstracts = """ \n""".join([
    f"""Title: {aa.title}

    Authors: {", ".join([f"{author['firstname']} {author['lastname']}" for author in aa.authors])}

    Journal: {aa.journal}

    Abstract: {aa.abstract}
    """ for aa in pm_results])

    return abstracts


def query_gpt(
            topic: str,
            abstracts: str,
            model: Optional[str] = "gpt-3.5-turbo") -> str:
    """
    Query pubmed and then query gpt
    """
    query = f"""
    Please create a presentation that summarizes each of the following abstracts with at most 6 bullet points each. One slide for each of the articles. On each slide, include the title of the article, and the name of the authors. Avoid jargon.

    Add a slide for the title, which should be "{topic}" and a slide that summarizes all of the abstracts.
    {abstracts}"""

    response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": 'You are a helpful assistant. Your response should be a remark.js presentation in markdown format.'},
        {"role": "user", "content": query},
        ]
    )

    return response["choices"][0]["message"]["content"]


class _MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def serve(port: Optional[int] = 8000):
    with socketserver.TCPServer(("", port), _MyHttpRequestHandler) as httpd:
        print("Site served at port", port)
        httpd.serve_forever()


@click.command()
@click.option('--topic', prompt="Please enter topic to query",
              help='Topic to query')
@click.option('--apikey',
              default=None,
              envvar='OPENAI_API_KEY',
              help='OpenAI API key is required to query GPT')
def main(topic: str,
         apikey: str,
         model: Optional[str] = "gpt-3.5-turbo",
         tofile: Optional[str] = "presentation.md"):

    abstracts = query_pubmed(topic)

    openai.api_key = apikey
    response = query_gpt(
        topic,
        abstracts,
        model)

    with open(tofile, 'w') as f:
        f.write(response)

    serve()


if __name__ == "__main__":
    main()
