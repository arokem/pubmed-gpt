from typing import Optional
import click

from pymed import PubMed
import openai


def query_pubmed(topic: str, max_results: Optional[int] = 8) -> str:
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
    Please create a presentation that summarizes each of the following abstracts with at most 6 bullet points each. One slide for each of the articles. On each slide, you must include the title of the article, and the name of the authors. Avoid jargon.

    Add a first title slide, which must include only the title:"{topic}, as summarized by {model}".

    You must also include a slide that summarizes all of the abstracts.
    {abstracts}"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": 'You are a helpful assistant. Your answers must always be a presentation in the remarkjs markdown format.'},
            {"role": "user", "content": query},
        ]
    )

    return response["choices"][0]["message"]["content"]


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


if __name__ == "__main__":
    main()
