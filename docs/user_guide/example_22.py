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
    # Example 22 - Features of Eigenvalues and Eigenvectors - The Effect o f Axial Load and Follower Torque

    This example is based on Example 5.9.7 from {cite}`friswell2010dynamics`.

    The Effect o f Axial Load and Follower Torque. Investigate the
    effect on the model of Example 5.9.1 of axial loads of —10,10, and 100 kN and
    torques of 50 and 100 kNm.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import pandas as pd
    from IPython.display import display

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return display, pd, rs


@app.cell
def _(rs):
    Q_ = rs.Q_
    return (Q_,)


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.2e9, rho=7810)
    return (steel,)


@app.cell
def _(Q_, display, pd, rs, steel):
    L = 0.25
    N = 6
    idl = 0
    odl = 0.05
    num_freq = 6

    bearings = [
        rs.BearingElement(n=0, kxx=1e6, cxx=0, scale_factor=2),
        rs.BearingElement(n=N, kxx=1e6, cxx=0, scale_factor=2),
    ]
    disks = [
        rs.DiskElement.from_geometry(
            n=2, material=steel, width=0.07, i_d=odl, o_d=0.28, scale_factor="mass"
        ),
        rs.DiskElement.from_geometry(
            n=4, material=steel, width=0.07, i_d=odl, o_d=0.35, scale_factor="mass"
        ),
    ]

    results = pd.DataFrame(
        {"speed": [0 for _ in range(num_freq)] + [4000 for _ in range(num_freq)]}
    )

    for speed in Q_([0, 4000], "RPM"):
        for axial in Q_([0, 10, 100, -10], "kN"):
            shaft = [
                rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel, axial_force=axial)
                for i in range(N)
            ]
            rotor = rs.Rotor(
                shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings
            )

            modal = rotor.run_modal(speed=speed)

            results.loc[results.speed == speed.m, f"Axial Load {axial.m}"] = (
                Q_(modal.wd[:6], "rad/s").to("Hz").m
            )

        for torque in Q_([50, 100], "kN*m"):
            shaft = [
                rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel, torque=torque)
                for i in range(N)
            ]
            rotor = rs.Rotor(
                shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings
            )

            modal = rotor.run_modal(speed=speed)

            results.loc[results.speed == speed.m, f"Torque {torque.m}"] = (
                Q_(modal.wd[:6], "rad/s").to("Hz").m
            )

    display(rotor.plot_rotor())
    display(results)
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
