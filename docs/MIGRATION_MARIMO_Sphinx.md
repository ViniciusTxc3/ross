# Migração de Notebooks Jupyter (.ipynb) para Marimo com Integração Sphinx

Este documento detalha o processo passo a passo para substituir os notebooks `.ipynb` existentes em `docs/user_guide` pela biblioteca [marimo](https://marimo.io) e integrá-los à documentação Sphinx do projeto ROSS.

---

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Etapa 1: Instalação](#3-etapa-1-instalação)
4. [Etapa 2: Conversão dos Notebooks](#4-etapa-2-conversão-dos-notebooks)
5. [Etapa 3: Configuração do Sphinx](#5-etapa-3-configuração-do-sphinx)
6. [Etapa 4: Adaptação dos Documentos](#6-etapa-4-adaptação-dos-documentos)
7. [Etapa 5: Reorganização do User Guide](#7-etapa-5-reorganização-do-user-guide)
8. [Etapa 6: Validação e Testes](#8-etapa-6-validação-e-testes)
9. [Etapa 7: Considerações sobre Dependências](#9-etapa-7-considerações-sobre-dependências)
10. [Referências](#10-referências)

---

## 1. Visão Geral

### Situação Atual

- **Documentação:** Sphinx com extensão `myst-nb`
- **Notebooks:** 47 arquivos `.ipynb` em `docs/user_guide`
- **Formato:** MyST Markdown com `{toctree}` referenciando notebooks diretamente

### Situação Desejada

- **Notebooks:** Arquivos `.py` no formato marimo
- **Integração:** Extensão `sphinx-marimo` para embedar notebooks interativos (WASM)
- **Formato:** Diretivas RST `.. marimo::` para incorporar os notebooks na documentação

### Diferenças Importantes

| Aspecto | Jupyter (.ipynb) | Marimo (.py) |
|---------|------------------|--------------|
| Formato | JSON | Python puro |
| Execução | Células independentes | Reativa (grafo de dependências) |
| Outputs | Persistidos no arquivo | Calculados em tempo de execução |
| Versionamento | Difícil (JSON) | Mais simples (texto) |

---

## 2. Pré-requisitos

- **Python:** 3.8 ou superior
- **Sphinx:** 4.0 ou superior
- **Marimo:** 0.1.0 ou superior
- **Ambiente:** Virtual environment ativado com dependências do ROSS instaladas

---

## 3. Etapa 1: Instalação

### 3.1. Instalar marimo

```bash
pip install marimo
```

### 3.2. Instalar sphinx-marimo

```bash
pip install sphinx-marimo
```

### 3.3. Atualizar requirements.txt da documentação

Adicionar ao arquivo `docs/requirements.txt`:

```
marimo
sphinx-marimo
```

### 3.4. Verificar instalação

```bash
marimo --version
python -c "import sphinx_marimo; print('sphinx-marimo OK')"
```

---

## 4. Etapa 2: Conversão dos Notebooks

### 4.1. Comando de conversão individual

Para converter um único notebook:

```bash
cd docs/user_guide
marimo convert example_1.ipynb -o example_1.py
```

**Parâmetros:**
- `example_1.ipynb` — arquivo de entrada (Jupyter notebook)
- `-o example_1.py` — arquivo de saída (notebook marimo)

### 4.2. Conversão em lote — PowerShell (Windows)

```powershell
cd docs/user_guide
Get-ChildItem -Filter "*.ipynb" | ForEach-Object {
    $outputName = $_.BaseName + ".py"
    marimo convert $_.Name -o $outputName
    Write-Host "Convertido: $($_.Name) -> $outputName"
}
```

### 4.3. Conversão em lote — Bash (Linux/macOS)

```bash
cd docs/user_guide
for f in *.ipynb; do
    marimo convert "$f" -o "${f%.ipynb}.py"
    echo "Convertido: $f -> ${f%.ipynb}.py"
done
```

### 4.4. Conversão silenciosa (CI/scripts)

```bash
marimo -q -y convert notebook.ipynb -o notebook.py
```

- `-q` — quiet (suprime output)
- `-y` — yes (aceita prompts automaticamente)

### 4.5. Comportamento da conversão

- **Outputs:** São removidos durante a conversão (marimo recalcula em tempo de execução)
- **Estrutura:** Células de código viram funções decoradas com `@app.cell`
- **Markdown:** Células markdown são convertidas em strings/`mo.md()`

### 4.6. Atenção à execução reativa

Marimo usa **execução reativa** — quando uma variável muda, todas as células que dependem dela são reexecutadas. Código que:

- Modifica variáveis em múltiplas células
- Usa estado mutável compartilhado
- Depende de ordem de execução manual

pode precisar de refatoração após a conversão.

---

## 5. Etapa 3: Configuração do Sphinx

### 5.1. Editar conf.py — Adicionar extensão

No arquivo `docs/conf.py`, na lista `extensions`:

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_marimo",      # Nova extensão
    # "myst_nb",         # Remover se não for mais usar .ipynb
    "sphinxcontrib.bibtex",
    "sphinx_copybutton",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx_design",
    "numpydoc",
    "sphinxcontrib.googleanalytics",
]
```

### 5.2. Configurações do sphinx-marimo

Adicionar após as extensões:

```python
# --- Configuração sphinx-marimo ---
marimo_notebook_dir = "user_guide"       # Diretório dos notebooks .py
marimo_default_height = "600px"          # Altura padrão do iframe
marimo_default_width = "100%"            # Largura padrão do iframe
marimo_click_to_load = "compact"         # "compact", "overlay" ou False
marimo_load_button_text = "Carregar Notebook Interativo"
```

### 5.3. Opções de marimo_click_to_load

| Valor | Descrição |
|-------|-----------|
| `False` | Notebooks carregam imediatamente (pode impactar performance) |
| `True` ou `"overlay"` | Overlay em tela cheia com botão centralizado |
| `"compact"` | Botão compacto que expande ao clicar (recomendado para vários notebooks) |

### 5.4. Ajustar source_suffix (opcional)

Se todos os `.ipynb` forem migrados, remover do `source_suffix`:

```python
source_suffix = [".rst", ".md"]  # Remove .ipynb
```

Manter `.ipynb` se houver documentos híbridos durante a transição.

---

## 6. Etapa 4: Adaptação dos Documentos

### 6.1. Sintaxe da diretiva marimo

Em arquivos RST (`.rst`):

```rst
.. marimo:: user_guide/example_1.py
   :height: 700px
   :width: 100%
   :click-to-load: compact
   :load-button-text: Executar Exemplo 1
```

### 6.2. Opções da diretiva

| Opção | Descrição | Padrão |
|-------|-----------|--------|
| `:height:` | Altura do iframe | `marimo_default_height` |
| `:width:` | Largura do iframe | `marimo_default_width` |
| `:click-to-load:` | Modo de carregamento (compact/overlay/false) | Config global |
| `:load-button-text:` | Texto do botão | Config global |

### 6.3. Usar marimo em MyST Markdown

Se precisar manter `.md`, inclua RST via fenced block:

````markdown
# Exemplo 1

```{rst}
.. marimo:: user_guide/example_1.py
   :height: 600px
```
````

Requer que `myst_nb` ou extensão MyST suporte `{rst}`.

---

## 7. Etapa 5: Reorganização do User Guide

### 7.1. Estrutura atual (user_guide.md)

```markdown
```{toctree}
:maxdepth: 1
:caption: Tutorials
tutorial_part_1
tutorial_part_2_1
...
```
```

### 7.2. Estratégia A: Arquivos RST individuais

Criar um `.rst` por notebook, por exemplo `docs/user_guide/tutorial_part_1.rst`:

```rst
Tutorial Parte 1
================

.. marimo:: user_guide/tutorial_part_1.py
   :height: 700px
   :click-to-load: compact
```

E no `user_guide.rst` principal:

```rst
User Guide
==========

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   user_guide/tutorial_part_1
   user_guide/tutorial_part_2_1
   user_guide/tutorial_part_2_2
   user_guide/tutorial_part_3
   user_guide/tutorial_part_4
   user_guide/tutorial_part_5

.. toctree::
   :maxdepth: 1
   :caption: Examples

   user_guide/example_1
   user_guide/example_2
   ...
```

### 7.3. Estratégia B: Página única com seções

Um único arquivo com todas as diretivas:

```rst
User Guide
==========

Tutorials
---------

.. marimo:: user_guide/tutorial_part_1.py
.. marimo:: user_guide/tutorial_part_2_1.py
...

Examples
--------

.. marimo:: user_guide/example_1.py
.. marimo:: user_guide/example_2.py
...
```

### 7.4. Ordem recomendada de migração

1. Tutoriais (tutorial_part_1 a tutorial_part_5)
2. Exemplos simples (example_1 a example_10)
3. Exemplos restantes (example_11 a example_32)
4. Fluid Flow (fluid_flow_*.ipynb)

---

## 8. Etapa 6: Validação e Testes

### 8.1. Validar notebooks convertidos

Abrir cada notebook no editor marimo:

```bash
marimo edit docs/user_guide/example_1.py
```

Verificar:
- Código executa sem erros
- Gráficos/visualizações aparecem
- Não há dependências circulares

### 8.2. Verificar sintaxe marimo

```bash
marimo check docs/user_guide/*.py
marimo check --fix docs/user_guide/*.py  # Corrigir automaticamente
```

### 8.3. Build da documentação

```bash
cd docs
make html
```

Ou no Windows:

```bash
cd docs
.\make.bat html
```

### 8.4. Inspecionar output

Abrir `docs/_build/html/index.html` e navegar até os notebooks. Verificar:
- Notebooks carregam (ou botão aparece)
- Layout está correto
- Interatividade funciona (se aplicável)

---

## 9. Etapa 7: Considerações sobre Dependências

### 9.1. WASM e Pyodide

O sphinx-marimo exporta notebooks para **HTML/WASM** rodando no browser via Pyodide. Nem todos os pacotes Python são compatíveis:

- **ross:** Provavelmente não suportado (NumPy/SciPy customizados)
- **numpy:** Parcialmente suportado
- **scipy:** Parcialmente suportado
- **plotly:** Suportado

### 9.2. Opções de estratégia

| Estratégia | Prós | Contras |
|------------|------|---------|
| **WASM (padrão)** | Execução no browser, sem backend | Dependências limitadas |
| **Execução estática** | Usar myst-nb para .ipynb executados | Perde interatividade |
| **Híbrido** | Exemplos simples em marimo, complexos em myst-nb | Mais complexo de manter |
| **Servidor** | Notebooks rodam via marimo run em servidor | Exige infraestrutura |

### 9.3. Para o ROSS

Considerar manter **myst-nb** para notebooks que usam ross, numpy avançado ou scipy, e usar **sphinx-marimo** apenas para exemplos mais simples ou tutoriais conceituais que usem bibliotecas compatíveis com Pyodide.

---

## 10. Referências

- [Marimo — Documentação Oficial](https://docs.marimo.io/)
- [Marimo CLI — Comando convert](https://docs.marimo.io/cli)
- [sphinx-marimo — GitHub](https://github.com/koaning/sphinx-marimo)
- [Marimo — Publicação com MkDocs](https://docs.marimo.io/guides/publishing/mkdocs)
- [Pyodide — Pacotes disponíveis](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)

---

*Documento criado para o projeto ROSS — Rotordynamic Open-Source Software*
