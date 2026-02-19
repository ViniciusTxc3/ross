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
    # Example 21 - Features of Eigenvalues and Eigenvectors - Hydrodynamic Bearings

    This example is based on Example 5.9.6 from {cite}`friswell2010dynamics`.
    Example 7 from the documentation uses the `BearingFluidFlow` class to create a hydrodynamic bearing.

    Here we are going to use the `CylindricalBearing` class, which is implemented based on {cite}`friswell2010dynamics`.

    Hydrodynamic Bearings. Repeat the analysis of Example 5.9.1
    when the bearings are replaced with hydrodynamic bearings. The oil-film bear
    ings have a diameter of 100 mm, are 30 mm long, and each supports a static load
    of 525 N, which represents half of the weight of the rotor. The radial clearance in
    the bearings is 0.1 mm and the oil film has a viscosity of 0.1 Pa s. These bearings
    have the same characteristics as Example 5.5.1.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import plotly.graph_objects as go
    from IPython.display import display

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return display, rs


@app.cell
def _(rs):
    Q_ = rs.Q_
    return (Q_,)


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.2e9, rho=7810)
    return (steel,)


@app.cell
def _(Q_, rs, steel):
    L = 0.25
    N = 6
    idl = 0
    odl = 0.05

    shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for i in range(N)]
    bearings = [
        rs.CylindricalBearing(
            n=0,
            speed=Q_(list(range(0, 5000, 50)), "RPM"),
            weight=525,
            bearing_length=Q_(30, "mm"),
            journal_diameter=Q_(100, "mm"),
            radial_clearance=Q_(0.1, "mm"),
            oil_viscosity=0.1,
        ),
        rs.CylindricalBearing(
            n=len(shaft),
            speed=Q_(list(range(0, 5000, 50)), "RPM"),
            weight=525,
            bearing_length=Q_(30, "mm"),
            journal_diameter=Q_(100, "mm"),
            radial_clearance=Q_(0.1, "mm"),
            oil_viscosity=0.1,
        ),
    ]
    disks = [
        rs.DiskElement.from_geometry(
            n=2, material=steel, width=0.07, i_d=odl, o_d=0.28, scale_factor="mass"
        ),
        rs.DiskElement.from_geometry(
            n=4, material=steel, width=0.07, i_d=odl, o_d=0.35, scale_factor="mass"
        ),
    ]

    rotor = rs.Rotor(shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings)
    rotor.plot_rotor()
    return (rotor,)


@app.cell
def _(Q_, rotor):
    campbell = rotor.run_campbell(speed_range=Q_(list(range(0, 4500, 50)), "RPM"))
    return (campbell,)


@app.cell
def _(campbell):
    campbell.plot(frequency_units="RPM")
    return


@app.cell
def _(Q_, rotor):
    modal = rotor.run_modal(speed=Q_(4000, "RPM"))
    return (modal,)


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
