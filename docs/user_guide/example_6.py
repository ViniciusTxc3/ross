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
    Example 6 - Isotropic bearings with damping.
    =====
    In this example, we use the rotor seen in Example 5.9.5 from {cite}`friswell2010dynamics`.

    The isotropic bearing Example 3 is repeated but with damping in the bearings. The, x and y directions are
    uncoupled, with a translational stiffness of 1 MN/m and a damping of 3 kNs/m
    in each direction.
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
    for i in range(6):
        shaft_elements.append(rs.ShaftElement(L=0.25, material=steel, n=i, idl=0, odl=0.05))
    _disk_elements.append(rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28))
    _disk_elements.append(rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.35))
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=3000.0, cyy=3000.0))
    _bearing_seal_elements.append(rs.BearingElement(n=6, kxx=1000000.0, kyy=1000000.0, cxx=3000.0, cyy=3000.0))
    rotor595c = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=_disk_elements)
    rotor595c.plot_rotor()
    return rotor595c, steel


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
    _bearing_seal_elements.append(rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=3000.0, cyy=3000.0))
    _bearing_seal_elements.append(rs.BearingElement(n=3, kxx=1000000.0, kyy=1000000.0, cxx=3000.0, cyy=3000.0))
    rotor595fs = rs.Rotor.from_section(brg_seal_data=_bearing_seal_elements, disk_data=_disk_elements, leng_data=shaft_length_data, idl_data=i_d, odl_data=o_d, material_data=steel)
    rotor595fs.plot_rotor()
    return (rotor595fs,)


@app.cell
def _(np, rotor595c, rotor595fs):
    # Obtaining results for w=0
    _modal595c = rotor595c.run_modal(0)
    modal595fs = rotor595fs.run_modal(0)
    print('Normal Instantiation =', _modal595c.wn * 60 / (2 * np.pi), '[RPM]')
    print('\n')
    print('From Section Instantiation =', modal595fs.wn * 60 / (2 * np.pi), '[RPM]')
    return


@app.cell
def _(np, rotor595c):
    # Obtaining results for w=4000RPM
    _modal595c = rotor595c.run_modal(4000 * np.pi / 30, num_modes=14)
    print('Normal Instantiation =', _modal595c.wn * 60 / (2 * np.pi), '[RPM]')  # speed input in rad/s
    return


@app.cell
def _(np, rotor595c):
    # The input units must be according to your unit standard system
    campbell = rotor595c.run_campbell(np.linspace(0, 4000 * np.pi / 30, 50), frequencies=7)
    # Plotting frequency in RPM
    campbell.plot(frequency_units="RPM")
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
