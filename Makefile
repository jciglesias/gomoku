NAME = gomoku
SRC = gomoku.py
VENV = .venv

.PHONY: all $(NAME) clean fclean re

all:	$(NAME)

$(NAME):
	@echo "Run with: make run"

run:
	python3 -m streamlit run $(SRC)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf $(VENV)

re: fclean all