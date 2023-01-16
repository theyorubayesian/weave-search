from jina import (
    Client,
    Document,
    DocumentArray
)

if __name__ == '__main__':
    c = Client(host='grpc://0.0.0.0:54321')

    # Test: Adding Documents from terms
    # da = c.post('/add_documents_from_terms', inputs=DocumentArray([Document(text="apoptosis")]))
    
    # Test: Finding documents
    da = c.post("/find_documents", inputs=DocumentArray([Document(text="Several proteins are secreted by Mtb that block different pathways leading to complete arrest")]))
    print(da[0].text)