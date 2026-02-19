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
    # Example 23 - An Overhung Rotor

    This example is based on Example 5.9.9 from {cite}`friswell2010dynamics`.

    An Overhung Rotor. Consider the overhung rotor shown in Figure 5.44.
    The shaft is 1.5m-long and the diameter is 50 mm with a disk of diameter
    350mm and thickness 70 mm. The two bearings, with positions given in
    Figure 5.44, have a stiffness of 10 MN/m in each direction. The shaft and disk
    are made of steel, with material properties E = 211 GN/m², G = 81.2 GN/m²
    and ρ = 7,810 kg/m3. Damping is neglected. Estimate the first six natural
    frequencies and mode shapes between 0 and 4,000 rev/min.
    """)
    return


@app.cell
def _():
    import ross as rs
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return (rs,)


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
        rs.BearingElement(n=0, kxx=1e7, cxx=0),
        rs.BearingElement(n=4, kxx=1e7, cxx=0),
    ]
    disks = [
        rs.DiskElement.from_geometry(
            n=N,
            material=steel,
            width=0.07,
            i_d=odl,
            o_d=0.35,
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
    campbell.plot(frequency_units="RPM", harmonics=[1, 2, 3])
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
