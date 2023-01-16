# Weave-Search

This is a minimal implementation of a semantic search engine built on biomedical data from [Reactome](https://reactome.org/). It uses [jina.ai](https://jina.ai/) for MLOps & [Weaviate] as its vector search engine.  You can find a basic exploration of the biomedical data in [explore.ipynb](notebooks/explore.ipynb). Each document is embedded using a Sentence Transformer executor with the finetuned version of [BioBERT](https://huggingface.co/gsarti/biobert-nli) available here: [gsarti/biobert-nli](https://huggingface.co/gsarti/biobert-nli).

![Weave-Search Flow](flow.svg)

## Installation

These instructions are for local development. This project has not been tested in production.

* You'll need Docker installed in order to run the Weaviate. See [Get Docker](https://docs.docker.com/get-docker/).

* Create a conda environment

```bash
conda create -n weave_search python=3.9
conda activate weave_search
```

* Install the version of `Pytorch==1.9.0` compatible with your CUDA version. See [Pytorch: Installation](https://pytorch.org/get-started/previous-versions/#v1101).

* Install other requirements

```bash
pip install -r requirements.txt
```

* Hack away! 🔨🔨

## Setup

* Ensure that you have completed the installation instructions above.

* Start the Weaviate service with configurations specified in [compose.yml](compose.yml) and used in [config.yml](src/weave_search/semantic_search/config.yml).

```bash
make start-weaviate
```

* Start the jina server

```bash
make init-weave-search
```

* Two main endpoints are exposed by the server: `/add_documents_from_terms` and `/find_documents`. Example requests are made to both endpoints in [client.py](client.py).

    1. Add documents from terms: Pull documents related to a term from Reactome, encode it `summation` field and add it to the running database.

    ```python
    from jina import (
        Client,
        Document,
        DocumentArray
    )
    c = Client(host='grpc://0.0.0.0:54321')

    terms = ["apoptosis", "alzheimer", "lung cancer", "apoptosis"]
    da = c.post('/add_documents_from_terms', inputs=DocumentArray([Document(text=term) for term in terms]))
    print(da.texts)
    ```

    2. Finding documents

    ```python
    da = c.post("/find_documents", inputs=DocumentArray([Document(text="Several proteins are secreted by Mtb that block different pathways leading to complete arrest")]))
    print(da[0].text)
    ```

## Next Steps

* Implement [filtering](https://docarray.jina.ai/advanced/document-store/weaviate/#filtering) and [sorting](https://docarray.jina.ai/advanced/document-store/weaviate/#sorting) for the `/find_documents` endpoint.

* Include additional attributes for documents returned by the `/find_documents` endpoint.
