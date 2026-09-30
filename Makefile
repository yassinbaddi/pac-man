
run:
	@PYGAME_HIDE_SUPPORT_PROMPT=1 uv run --active python3 main.py config.json

clean:
	rm -rf */__pycache__ __pycache__

.PHONY: run clean
