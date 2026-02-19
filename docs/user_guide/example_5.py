import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Example 5 - Cross-coupled bearings.
    =====
    In this example, we use the rotor seen in Example 5.9.4 from {cite}`friswell2010dynamics`.

    This system is the same as that of
    Example 3, except that some coupling is introduced in the bearings between the x and y directions. The bearings have direct stiffnesses of $1 MN/m$ and cross-coupling stiffnesses of $0.5 MN/m$.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return np, rs


@app.cell
def _(rs):
    # Classic Instantiation of the rotor
    shaft_elements = []
    _bearing_seal_elements = []
    _disk_elements = []
    Steel = rs.steel
    for i in range(6):
        shaft_elements.append(rs.ShaftElement(L=0.25, material=Steel, n=i, idl=0, odl=0.05))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=Steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=4, material=Steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, kxy=500000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=6, kxx=1000000.0, kyy=1000000.0, kxy=500000.0, cxx=0, cyy=0))
    rotor594c = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=_disk_elements)
    rotor594c.plot_rotor()
    return Steel, rotor594c


@app.cell
def _(Steel, rs):
    # From_section class method instantiation.
    _bearing_seal_elements = []
    _disk_elements = []
    shaft_length_data = 3 * [0.5]
    i_d = 3 * [0]
    o_d = 3 * [0.05]
    _disk_elements.append(rs.DiskElement.from_geometry(n=1, material=Steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=Steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=3, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    rotor594fs = rs.Rotor.from_section(brg_seal_data=_bearing_seal_elements, disk_data=_disk_elements, leng_data=shaft_length_data, idl_data=i_d, odl_data=o_d, material_data=Steel)
    rotor594fs.plot_rotor()
    return (rotor594fs,)


@app.cell
def _(rotor594c, rotor594fs):
    # Obtaining results for w=0 (wn is in rad/s)
    _modal594c = rotor594c.run_modal(0)
    modal594fs = rotor594fs.run_modal(0)
    print('Normal Instantiation =', _modal594c.wn)
    print('\n')
    print('From Section Instantiation =', modal594fs.wn)
    return


@app.cell
def _(np, rotor594c):
    # Obtaining results for w=4000RPM (wn is in rad/s)
    _modal594c = rotor594c.run_modal(4000 * np.pi / 30)
    print('Normal Instantiation =', _modal594c.wn)
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
