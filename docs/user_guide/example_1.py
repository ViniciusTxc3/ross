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
    Example 1 - Number of DOF influence in Natural Frequency
    =========
    In this example, we use the rotor seen in Example 5.8.1 from {cite}`friswell2010dynamics`. Which is a symmetric rotor with a single disk in the center. The shaft is hollow with an outside diameter of $80 mm$, an inside
    diameter of $30 mm$, and a length of $1.2 m$ and it is modeled using Euler-Bernoulli elements, with no internal shaft damping.
    The bearings are rigid and short and the disk has a diameter of $400 mm$ and a thickness
    of $80 mm$.
    The disk and shaft elements are made of steel.
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
            (Plotly é instalado automaticamente via micropip.) Para rodar este exemplo com ROSS localmente use **uv** (recomendado):  
            `uv run marimo edit docs/user_guide/example_1.py`
            """
        )
        steel = None
    else:
        steel = rs.materials.steel
    return (steel,)


@app.cell
def _():
    number_of_elements = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 40, 60]
    return (number_of_elements,)


@app.cell
def _(rs, steel, _deps_ok):
    if not _deps_ok or rs is None or steel is None:
        create_rotor = None
    else:
        def create_rotor(n_el):
            """Create example rotor with given number of elements."""
            shaft = [
                rs.ShaftElement(1.2 / (n_el), idl=0.03, odl=0.08, material=steel)
                for i in range(n_el)
            ]
            disks = [
                rs.DiskElement.from_geometry(
                    n=(n_el / 2), material=steel, width=0.08, i_d=0.08, o_d=0.4
                )
            ]
            bearings = [
                rs.BearingElement(0, kxx=1e15, cxx=0),
                rs.BearingElement(n_el, kxx=1e15, cxx=0),
            ]
            return rs.Rotor(shaft, disks, bearings)
    return (create_rotor,)


@app.cell
def _(create_rotor, go, np, number_of_elements):
    if create_rotor is None or go is None or np is None:
        analysis = None
    else:
        def analysis(speed):
            """Perform convergence analysis for a given speed."""
            n_eigen = 8
            rotor_80 = create_rotor(80)
            modal_80 = rotor_80.run_modal(speed, num_modes=2 * n_eigen)
            errors = np.zeros([len(number_of_elements), n_eigen])
            for i, n_el in enumerate(number_of_elements):
                rotor = create_rotor(n_el)
                modal = rotor.run_modal(speed, num_modes=2 * n_eigen)
                errors[i, :] = abs(
                    100 * (modal.wn[:n_eigen] - modal_80.wn[:n_eigen]) / modal_80.wn[:n_eigen]
                )
            fig = go.Figure()
            for i in range(8):
                fig.add_trace(
                    go.Scatter(x=number_of_elements, y=errors[:, i], name=f"Mode {i}")
                )
            fig.update_layout(
                xaxis=dict(title="Number of degrees of freedom"),
                yaxis=dict(type="log", title="Natural Frequency Error(%)"),
            )
            return fig
    return (analysis,)


@app.cell
def _(analysis):
    if analysis is not None:
        analysis(speed=0)
    return


@app.cell
def _(analysis, np):
    if analysis is not None and np is not None:
        analysis(speed=5000 * np.pi / 30)
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
