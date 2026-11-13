# Install python
.PHONY: install-python
install-python:
	uv sync

.PHONY: install-gem
install-gem:
	rbenv local 3.3.6
	bundle config set --local path 'vendor/bundle'
	bundle install

.PHONY: serve
serve:
	bundle exec jekyll serve -l -H localhost
	
.PHONY: build-publications
build-publications:
	uv run python ./markdown_generator/pubsFromBib.py
## Clean files
.PHONY: clean
clean:
	rm -f .coverage
	rm -rf `find . -name __pycache__`
	rm -rf `find . -name .ipynb_checkpoints`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf .ipynb_checkpoints
	rm -rf .venv
	rm -rf vendor
	rm -rf .bundle
	rm -rf .ruby-lsp
	rm Gemfile.lock

