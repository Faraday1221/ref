# Causal AI

https://www.robertosazuwaness.com/causal-ai-book/

### new project setup cheatsheet

```sh
mkdir causal_ai_book
uv init
uv python install 3.11
uv python pin 3.11
uv venv
source .venv/bin/activate
uv add --dev ipython
uv add --dev ruff

# manually configured .vscode/settings.json for ruff
# manual ruff settings in pyproject.toml
# consider config from: https://docs.astral.sh/ruff/configuration/

# .gitignore from gitignore.io

uv add torch torchvision pyro-ppl pgmpy

# deactivate venv
deactivate
```
