# Minimal makefile for Sphinx documentation
# Preferência: uv (recomendado pelo marimo) > venv > sphinx-build do PATH
#

SPHINXOPTS    =
SOURCEDIR     = .
BUILDDIR      = _build
SPHINXPROJ    = ross

# Detectar uv (recomendado pelo marimo: https://docs.marimo.io/guides/package_management/using_uv/)
UV_AVAILABLE  = $(shell command -v uv 2>/dev/null && echo 1)
# Fallback: venv do projeto
VENV_BIN      = $(if $(wildcard ../venv/bin/sphinx-build),../venv/bin/,)
# Comando de build: uv run usa o ambiente do projeto (deps instaladas com uv pip install -r docs/requirements.txt)
ifeq ($(UV_AVAILABLE),1)
  SPHINXBUILD = uv run --project .. sphinx-build
else
  SPHINXBUILD = $(VENV_BIN)sphinx-build
endif

# Com venv (sem uv), marimo no PATH para sphinx-marimo
export PATH := $(if $(VENV_BIN),$(abspath $(VENV_BIN)):$(PATH),$(PATH))

# Instalar deps da documentação com uv (recomendado pelo marimo) e aplicar patch --show-code
install-deps:
	cd .. && uv pip install -e . && uv pip install -r docs/requirements.txt
	cd .. && uv run python docs/tools/patch_sphinx_marimo_show_code.py

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile install-deps

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
