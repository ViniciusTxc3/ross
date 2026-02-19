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
    Example 4 - Anisotropic Bearings.
    ====
    In this example, we use the rotor seen in Example 5.9.2 from {cite}`friswell2010dynamics`.

    Both bearings have a stiffness of 1 MN/m in the x direction and 0.8 MN/m in the
    y direction. Calculate the eigenvalues and mode shapes at 0 and 4,000 rev/min
    and plot the natural frequency map for rotational speeds up to 4,500 rev/min.
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
    steel = rs.steel
    for _i in range(6):
        shaft_elements.append(rs.ShaftElement(L=0.25, material=steel, n=_i, idl=0, odl=0.05))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=800000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=6, kxx=1000000.0, kyy=800000.0, cxx=0, cyy=0))
    rotor592c = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=_disk_elements)
    rotor592c.plot_rotor()
    return rotor592c, steel


@app.cell
def _(rs, steel):
    # From_section class method instantiation.
    _bearing_seal_elements = []
    _disk_elements = []
    shaft_length_data = 3 * [0.5]
    i_d = 3 * [0]
    o_d = 3 * [0.05]
    _disk_elements.append(rs.DiskElement.from_geometry(n=1, material=steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=800000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=3, kxx=1000000.0, kyy=800000.0, cxx=0, cyy=0))
    rotor592fs = rs.Rotor.from_section(brg_seal_data=_bearing_seal_elements, disk_data=_disk_elements, leng_data=shaft_length_data, idl_data=i_d, odl_data=o_d, material_data=steel)
    rotor592fs.plot_rotor()
    return (rotor592fs,)


@app.cell
def _(rotor592c, rotor592fs):
    # Obtaining results for speed = 150 rad/s (wn is in rad/s)

    modal592c = rotor592c.run_modal(150.0)
    modal592fs = rotor592fs.run_modal(150.0)

    print("Normal Instantiation =", modal592c.wn)
    print("\n")
    print("From Section Instantiation =", modal592fs.wn)
    return


@app.cell
def _(np, rotor592c):
    # Obtaining results for w=4000RPM (wn is in rad/s)
    speed = 4000 * np.pi / 30
    modal592c_1 = rotor592c.run_modal(speed, num_modes=14)
    print('Normal Instantiation =', modal592c_1.wn)
    return (modal592c_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Campbell Diagram
    """)
    return


@app.cell
def _(np, rotor592c):
    campbell = rotor592c.run_campbell(np.linspace(0, 4000 * np.pi / 30, 50), frequencies=7)
    # Plotting frequency in RPM
    fig = campbell.plot(frequency_units="RPM")
    fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Mode Shapes
    """)
    return


@app.cell
def _(modal592c_1):
    for _i in range(7):
        modal592c_1.plot_mode_3d(mode=int(_i)).show()
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
