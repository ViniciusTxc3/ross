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
    Example 13 - Uncertainties on bearings coefficients
    ==========================================
    In this example, we use the rotor seen in Example 5.9.4 from {cite}`friswell2010dynamics`.

    This system is the same as that of Example 3, except that now, we'll considerer some level of uncertainties on bearing direct coefficients (`kxx`, `kyy`, `cxx`, `cyy`).
    """)
    return


@app.cell
def _():
    import ross as rs
    import ross.stochastic as srs
    import numpy as np
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return np, rs, srs


@app.cell
def _(rs):
    # Deterministic Shaft Elements
    Steel = rs.steel
    shaft = [rs.ShaftElement(L=0.25, material=Steel, idl=0, odl=0.05) for i in range(6)]

    # Deterministic Disk Elements
    disk1 = rs.DiskElement.from_geometry(
        n=2,
        material=Steel,
        width=0.07,
        i_d=0.05,
        o_d=0.28,
    )

    disk2 = rs.DiskElement.from_geometry(
        n=4,
        material=Steel,
        width=0.07,
        i_d=0.05,
        o_d=0.35,
    )
    disks = [disk1, disk2]
    return disks, shaft


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example, let's consider an uniform distribuition for the coefficients. Because it's a demonstrative example, we'll not use too many samples, to avoid taking too long to run the simulation.

    We can use `numpy.random` package to generate random values for our variables.

    #### Stochastic Bearing Elements
    """)
    return


@app.cell
def _(np, srs):
    # random variables must have the same size
    kxx = np.random.uniform(low=1e6, high=3e6, size=50)
    cxx = np.random.uniform(low=1e2, high=2e2, size=50)

    bearing1 = srs.ST_BearingElement(n=0, kxx=kxx, cxx=cxx, is_random=["kxx", "cxx"])
    bearing2 = srs.ST_BearingElement(n=6, kxx=kxx, cxx=cxx, is_random=["kxx", "cxx"])
    bearings = [bearing1, bearing2]
    return (bearings,)


@app.cell
def _(bearings, disks, shaft, srs):
    # Building random instances for a rotor model

    rand_rotor = srs.ST_Rotor(
        shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings
    )

    # Number of samples
    print("Number of samples:", len(list(iter(rand_rotor))))
    return (rand_rotor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting a random sample

    We can use `numpy.random.choice` to take a random rotor object. Then, we can use the same functions than to `Rotor` class.
    """)
    return


@app.cell
def _(np, rand_rotor):
    sample = np.random.choice(list(iter(rand_rotor)))
    sample.plot_rotor()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Running Stochastic Campbell Diagram
    """)
    return


@app.cell
def _(np, rand_rotor):
    speed_range = np.linspace(0, 600, 31)
    camp = rand_rotor.run_campbell(speed_range)
    return (camp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting Stochastic Campbell Diagram
    """)
    return


@app.cell
def _(camp):
    # choose the desirable percentiles or confidence intervals
    camp.plot_nat_freq(conf_interval=[95], width=950, height=700)
    return


@app.cell
def _(camp):
    # choose the desirable percentiles or confidence intervals
    camp.plot_log_dec(conf_interval=[95], width=950, height=700)
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
