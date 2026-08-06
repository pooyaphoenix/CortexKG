install:
	pip install -r requirements.txt

run:
	python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +