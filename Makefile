.PHONY: init-weave-search start-weaviate

init-weave-search:
	jina flow --uses src/weave_search/flow.yml

start-weaviate:
	docker compose up
