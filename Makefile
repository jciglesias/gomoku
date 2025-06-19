NAME = gomoku
SRC = gomoku.py
VENV = .venv

.PHONY: all $(NAME) clean fclean re

all:	venv $(NAME)

$(NAME):
	@echo "Run with: make run"

venv:	$(VENV)/bin/activate

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run:	venv
	$(VENV)/bin/python -m streamlit run $(SRC)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf $(VENV)

re: fclean all