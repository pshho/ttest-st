# Label normalizer

`normalizer.py` provides `normalize_label(text: str) -> str`. It lowercases
text, collapses runs of whitespace (including Unicode whitespace) to a single
space, and removes leading and trailing whitespace. It uses only the Python
standard library.

For example, `normalize_label("  HeLLo\t  WoRLD\n ")` returns `"hello world"`.

Run the tests from the repository root:

```sh
uv run --no-project python -m unittest discover -s paperclip_smoke -p 'test_*.py' -v
```

The tests cover mixed case and whitespace, empty input, whitespace-only input,
and Unicode text.
