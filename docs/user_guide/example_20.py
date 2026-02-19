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
    # Example 20 - Features of Eigenvalues and Eigenvectors - Cross-Coupling in the Bearings

    This example is based on Example 5.9.4 from {cite}`friswell2010dynamics`.

    Cross-Coupling in the Bearings. This system is the same as that of
    Example 5.9.1 except that some coupling is introduced in the bearings between
    the x and y directions. T he bearings have direct stiffnesses of 1 MN/m and cross
    coupling stiffnesses of 0.5 MN/m.
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
def _(rs, steel):
    L = 0.25
    N = 6
    idl = 0
    odl = 0.05

    shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for i in range(N)]
    bearings = [
        rs.BearingElement(
            n=0, kxx=1e6, kyy=1e6, kxy=0.5e6, kyx=0.5e6, cxx=0, scale_factor=2
        ),
        rs.BearingElement(
            n=len(shaft), kxx=1e6, kyy=1e6, kxy=0.5e6, kyx=0.5e6, cxx=0, scale_factor=2
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
    campbell = rotor.run_campbell(
        speed_range=Q_(list(range(0, 4500, 50)), "RPM"), frequencies=7
    )
    return (campbell,)


@app.cell
def _(campbell):
    campbell.plot(frequency_units="RPM")
    return


@app.cell
def _(Q_, rotor):
    modal = rotor.run_modal(speed=Q_(4000, "RPM"), num_modes=14)
    return (modal,)


@app.cell
def _(display, modal):
    for _mode in range(7):
        display(modal.plot_mode_3d(_mode, frequency_units='Hz'))
    return


@app.cell
def _(display, modal):
    for _mode in range(7):
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
