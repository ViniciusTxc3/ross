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
    Example 7 - Hydrodynamic Bearings
    =====
    In this example, we use the rotor seen in Example 5.9.6 from {cite}`friswell2010dynamics`.

    Same rotor of Example 3, but the bearings are replaced with hydrodynamic bearings. In order to instantiate them, rather than giving the stiffness and damping data, we will calculate them using their hydrodynamic data, as provided by Example 5.5.1 from the book: The oil-film bearings have a diameter of 100 mm, are 30 mm long, and each supports a static load of 525 N, which represents half of the weight of the rotor. The radial clearance in the bearings is 0.1 mm and the oil film has a viscosity of 0.1 Pa s.
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

    Q_ = rs.Q_
    return Q_, np, rs


@app.cell
def _(np, rs):
    # Classic Instantiation of the rotor
    shaft_elements = []
    disk_elements = []
    steel = rs.materials.steel
    for i in range(6):
        shaft_elements.append(rs.ShaftElement(L=0.25, material=steel, n=i, idl=0, odl=0.05))
    disk_elements.append(rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28))
    disk_elements.append(rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.35))
    bearing = rs.BearingFluidFlow(n=0, nz=30, ntheta=20, length=0.03, omega=np.linspace(1, 5000, 5), p_in=0, p_out=0, radius_rotor=0.0499, radius_stator=0.05, visc=0.1, rho=860.0, load=525)
    _bearing_copy = rs.BearingElement(n=6, frequency=bearing.frequency, kxx=bearing.kxx, kxy=bearing.kxy, kyx=bearing.kyx, kyy=bearing.kyy, cxx=bearing.cxx, cxy=bearing.cxy, cyx=bearing.cyx, cyy=bearing.cyy)
    _bearing_seal_elements = [bearing, _bearing_copy]
    rotor = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=disk_elements)
    # copy bearing to decrease compute time and set node
    rotor.plot_rotor()
    return bearing, disk_elements, shaft_elements


@app.cell
def _(bearing, disk_elements, rs, shaft_elements):
    _bearing_copy = rs.BearingElement(n=6, frequency=bearing.frequency, kxx=bearing.kxx, kxy=bearing.kxy, kyx=bearing.kyx, kyy=bearing.kyy, cxx=bearing.cxx, cxy=bearing.cxy, cyx=bearing.cyx, cyy=bearing.cyy)
    _bearing_seal_elements = [bearing, _bearing_copy]
    rotor_1 = rs.Rotor(shaft_elements=shaft_elements, bearing_elements=_bearing_seal_elements, disk_elements=disk_elements)
    rotor_1.plot_rotor()
    return (rotor_1,)


@app.cell
def _(Q_, rotor_1):
    _campbell = rotor_1.run_campbell(speed_range=Q_(list(range(0, 4500, 50)), 'RPM'))
    return


@app.cell
def _(np, rotor_1):
    # Obtaining results for w=4000RPM
    modal = rotor_1.run_modal(4000 * np.pi / 30)
    print('Normal Instantiation =', modal.wn / (2 * np.pi))
    return (modal,)


@app.cell
def _(np, rotor_1):
    _campbell = rotor_1.run_campbell(np.linspace(0, 4000 * np.pi / 30, 50))
    _campbell.plot(frequency_units='RPM')
    return


@app.cell
def _(display, modal):
    for _mode in range(6):
        display(modal.plot_mode_3d(_mode, frequency_units='Hz'))
    return


@app.cell
def _(display, modal):
    for _mode in range(6):
        display(modal.plot_orbit(_mode, nodes=[2, 4]))
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
