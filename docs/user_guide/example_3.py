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
    Example 3 - Isotropic Bearings, asymmetrical rotor.
    ===========

    In this example, we use the rotor seen in Example 5.9.1 from {cite}`friswell2010dynamics`.
    A 1.5-m-long shaft, with a diameter of $0.05 m$. The disks are keyed to the shaft at $0.5$ and $1 m$ from
    one end. The left disk is $0.07 m$ thick with a diameter of $0.28 m$; the right disk
    is $0.07 m$ thick with a diameter of $0.35 m$. For the shaft, $E = 211 GN/m^2$ and
    $G = 81.2 GN/m^2$. There is no internal shaft damping. For both the shaft and the
    disks, $\rho = 7,810 kg/m^3$. The shaft is supported by identical bearings at its ends.

    These bearings are isotropic and have a stiffness of $1 MN/m$ in both the x and
    y directions. The bearings contribute no additional stiffness to the rotational
    degrees of freedom and there is no damping or cross-coupling in the bearings.
    """)
    return


@app.cell
def _():
    import ross as rs
    from ross.materials import steel
    import numpy as np
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return np, rs, steel


@app.cell
def _(rs, steel):
    # Classic Instantiation of the rotor
    shaft_elements = []
    _bearing_seal_elements = []
    _disk_elements = []
    for i in range(6):
        shaft_elements.append(rs.ShaftElement(L=0.25, material=steel, n=i, idl=0, odl=0.05))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=6, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    rotor591c = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=_disk_elements)
    rotor591c.plot_rotor()
    return (rotor591c,)


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
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    _bearing_seal_elements.append(rs.BearingElement(n=3, kxx=1000000.0, kyy=1000000.0, cxx=0, cyy=0))
    rotor591fs = rs.Rotor.from_section(brg_seal_data=_bearing_seal_elements, disk_data=_disk_elements, leng_data=shaft_length_data, idl_data=i_d, odl_data=o_d, material_data=steel)
    rotor591fs.plot_rotor()
    return (rotor591fs,)


@app.cell
def _(np, rotor591c, rotor591fs):
    # Obtaining results (wn is in rad/s)
    fig = rotor591c.run_campbell(np.linspace(0, 4000 * np.pi / 30, 50), frequencies=7).plot(
        frequency_units="rad/s"
    )
    fig.show()

    print("Normal Instantiation =", rotor591c.run_modal(speed=2000 * np.pi / 30).wn)
    print("\n")
    print("From Section Instantiation =", rotor591fs.run_modal(speed=2000 * np.pi / 30).wn)
    return


@app.cell
def _(np, rotor591c):
    # Obtaining modal results for w=4000RPM (wn is in rad/s)
    speed = 4000 * np.pi / 30
    modal591c = rotor591c.run_modal(speed, num_modes=14)

    print("Normal Instantiation =", modal591c.wn)
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
