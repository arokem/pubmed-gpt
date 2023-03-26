from typing import Optional
import click
import uuid

from pymed import PubMed
import openai


def query_pubmed(topic: str, email: str, max_results: Optional[int]=5) -> str:
    """
    Get abstracts for a topic from pubmed
    """
    pubmed = PubMed(tool=f"pubmed-gpt-{uuid.uuid1()}", email=email)
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
    abstracts = query_pubmed(topic, email)

    query = f"""
    Please create a presentation that summarizes each of the following abstracts with at most 6 bullet points.

    Please create this in the remark.js markdown format, with one slide for each of the article below.

    On each slide, include the title of the article, the name of the authors and journal and a link to the article

    Add a slide for the title, which should be "{topic}" and a slide for summary that summarizes all of the abstracts.

    {abstracts}"""

    response = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "system", "content": f'You are a helpful assistant. Your response should be a remark.js presentation in markdown format.'},
        {"role": "user", "content": query},
        ]
    )

    return response["choices"][0]["message"]["content"]


@click.command()
@click.option('--topic', prompt="Please enter topic to query",
              help='Topic to query')
@click.option('--email',
              envvar='EMAIL',
              help='Email address is required to query pubmed')
@click.option('--apikey',
              default=None,
              envvar='OPENAI_API_KEY',
              help='OpenAI API key is required to query GPT')
def main(topic: str,
         email: str,
         apikey: str,
         model: Optional[str]="gpt-3.5-turbo",
         tofile: Optional[str]="presentation.md"):

    abstracts = query_pubmed(topic, email)

    openai.api_key = apikey
    response = query_gpt(
        topic,
        abstracts,
        model)

    with open(tofile, 'w') as f:
        f.write(response)


if __name__ == "__main__":
    main()
