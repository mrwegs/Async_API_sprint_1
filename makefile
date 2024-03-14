run: venv
	# .venv/bin/python3.11 -m src.entrypoint
	python3 -m src.entrypoint

venv: .venv/touchfile

.venv/touchfile: requirements.txt
	python3 -m venv .venv
	pip install -r requirements.txt
	touch .venv/touchfile
	. .venv/bin/activate

clean:
	rm -rf .venv/
	rm -rf .ruff_cache/
	rm -rf src/__pycache__/
	rm -rf .pytest_cache/
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete

restart:
	docker-compose down && docker-compose up -d --build