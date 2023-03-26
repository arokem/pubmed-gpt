# pubmed-gpt

Use gpt to summarize articles from pubmed as a slide presentation. The goal of
this software is to find the top 8 articles on a topic in pubmed (based on
pubmed's "relevance" criterion) and ask GPT to summarize the abstract of each
article as a single slide, providing also a title slide and a summary slide,
which should hopefully synthesize the mess.


## Install

To install, download the source code and run:

    pip install .

In the top-level directory.


## Run

The software can be run by issuing:

    pmgpt

On the command line. To run this, you will need to get an [API key from OpenAI](https://platform.openai.com/account/api-keys).

The software will prompt you for a pubmed query (try "Glymphatic system" or
"Maiken Nedergaard", for example) and will then generate a (hopefully functioning) file
called "presentation.md" that should contain slides according to the
[remark](https://github.com/gnab/remark) format.

To view these slides, you can run:

    python -m http.server

And open a browser to http://localhost:8000/