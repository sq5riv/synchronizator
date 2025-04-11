.PHONY: test

test: ## Run tests
	pytest --cov=src --cov-report=html
