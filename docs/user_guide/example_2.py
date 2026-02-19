import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
async def _():
    """No navegador (Pyodide), instala plotly via micropip antes dos imports."""
    import sys
    if "pyodide" in sys.modules:
        import micropip
        await micropip.install("plotly")
    _packages_ready = True
    return (_packages_ready,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Example 2 - Effect of varying slenderness ratio
    =========
    In this example, we use the rotor seen in Example 5.8.2 from {cite}`friswell2010dynamics`.
    """)
    return


@app.cell
def _(_packages_ready):
    try:
        import numpy as np
        import plotly.graph_objects as go
        import ross as rs
        import plotly.io as pio
        pio.renderers.default = "notebook"
        _deps_ok = True
    except ModuleNotFoundError:
        _deps_ok = False
        np = go = rs = None
    return (go, np, rs, _deps_ok)


@app.cell
def _(mo, rs, _deps_ok):
    if not _deps_ok or rs is None:
        mo.md(
            r"""
            **Notebook no navegador (Pyodide):** A biblioteca **ROSS** não está disponível no browser.
            Para rodar com ROSS localmente (use **uv**): `uv run marimo edit docs/user_guide/example_2.py`
            """
        )
        steel = None
    else:
        steel = rs.materials.steel
    return (steel,)


@app.cell
def _():
    number_of_elements = [2, 3, 4, 5, 6, 7, 8]
    return (number_of_elements,)


@app.cell
def _(rs, steel, _deps_ok):
    if not _deps_ok or rs is None or steel is None:
        create_rotor = None
    else:
        def create_rotor(n_el, R, shear_effects=False, rotary_inertia=False):
            """Create example rotor with given number of elements and R ration."""
            L_total = 1
            D = R * L_total
            shaft = [rs.ShaftElement(1.0 / n_el, idl=0, odl=D, material=steel, shear_effects=shear_effects, rotary_inertia=rotary_inertia) for _i in range(n_el)]
            bearings = [rs.BearingElement(0, kxx=1000000000000000.0, cxx=0), rs.BearingElement(n_el, kxx=1000000000000000.0, cxx=0)]
            return rs.Rotor(shaft_elements=shaft, bearing_elements=bearings)
    return (create_rotor,)


@app.cell
def _(create_rotor, go, np, number_of_elements):
    if create_rotor is None or go is None or np is None:
        return
    _n_eigen = 8
    _R = 0.04
    rotor_80 = create_rotor(80, _R)
    modal_80 = rotor_80.run_modal(speed=0, num_modes=2 * _n_eigen)
    _errors = np.zeros([len(number_of_elements), _n_eigen])
    for (_i, _n_el) in enumerate(number_of_elements):
        _rotor = create_rotor(_n_el, _R)
        _modal = _rotor.run_modal(speed=0, num_modes=2 * _n_eigen)
        _errors[_i, :] = abs(100 * (_modal.wn[:_n_eigen] - modal_80.wn[:_n_eigen]) / modal_80.wn[:_n_eigen])
    _fig = go.Figure()
    for _i in range(_n_eigen):
        _fig.add_trace(go.Scatter(x=number_of_elements, y=_errors[:, _i], name=f'Mode {_i}'))
    _fig.update_layout(xaxis=dict(title='Number of elements'), yaxis=dict(title='Natural Frequency error(%)', type='log'))
    return


@app.cell
def _(create_rotor, go, np):
    if create_rotor is None or go is None or np is None:
        return
    _n_el = 6
    R_list = np.linspace(0.0001, 0.15, 10)
    _n_eigen = 6
    _errors = np.zeros([len(R_list), _n_eigen])
    for (_i, _R) in enumerate(R_list):
        rotor_ref = create_rotor(100, _R, shear_effects=True, rotary_inertia=True)
        modal_ref = rotor_ref.run_modal(speed=0)
        _rotor = create_rotor(_n_el, _R)
        _modal = _rotor.run_modal(speed=0, num_modes=2 * _n_eigen)
        _errors[_i, :] = abs(100 * (_modal.wn[:_n_eigen] - modal_ref.wn[:_n_eigen]) / modal_ref.wn[:_n_eigen])
    _fig = go.Figure()
    for _i in range(_n_eigen):
        _fig.add_trace(go.Scatter(x=R_list, y=_errors[:, _i], name=f'Mode {_i}'))
    _fig.update_layout(xaxis=dict(title='Slenderness ratio'), yaxis=dict(title='Natural Frequency error(%)', type='log'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    ```{bibliography}
    :filter: docname in docnames
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
