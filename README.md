# pubmed-gpt

Use gpt to summarize articles from pubmed.


## Install

To install, download the source code and run:

    pip install .

In the top-level directory.

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