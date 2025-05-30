.PHONY: setup run clean

# Setup virtual environment and install dependencies
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Run the Flask application
run:
	PYTHONPATH=$PYTHONPATH:. python src/app.py

# Clean up virtual environment
clean:
	rm -rf venv

# Activate virtual environment (run this in your shell)
activate:
	@echo "Run this command in your shell:"
	@echo "source venv/bin/activate" 