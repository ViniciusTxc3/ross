"""
Aplica patch no sphinx-marimo para usar --show-code no export html-wasm,
exibindo o código nos notebooks embutidos na documentação.

Execute após: pip install sphinx-marimo
Uso: python docs/tools/patch_sphinx_marimo_show_code.py
"""
import site
from pathlib import Path

try:
    import sphinx_marimo
except ImportError:
    print("sphinx-marimo não instalado. Execute: pip install sphinx-marimo")
    raise SystemExit(1)

builder_path = Path(sphinx_marimo.__file__).parent / "builder.py"
text = builder_path.read_text()

# Formato original (uma linha) do sphinx-marimo
old_one_line = '["marimo", "export", "html-wasm", str(notebook_path), "-o", str(output_path), "--force"]'
# Formato com quebra de linha
old_multiline = '"--force"],'
new_multiline = '"--force", "--show-code"],'
already_patched = "--show-code" in text and "html-wasm" in text

if already_patched:
    print("Patch já aplicado em", builder_path)
elif old_one_line in text:
    new_one_line = old_one_line.replace('"--force"]', '"--force", "--show-code"]')
    builder_path.write_text(text.replace(old_one_line, new_one_line))
    print("Patch aplicado em", builder_path)
elif old_multiline in text:
    builder_path.write_text(text.replace(old_multiline, new_multiline))
    print("Patch aplicado em", builder_path)
else:
    print("Não foi possível encontrar o trecho esperado em", builder_path)
    raise SystemExit(1)
