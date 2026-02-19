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
    Example 14 - Uncertainties on material properties
    ========================================
    In this example, we use the rotor seen in Example 5.9.4 from {cite}`friswell2010dynamics`.

    This system is the same as that of Example 3, but now we'll work with uncertainties on material properties, representing a fault in the shaft. We will apply the uncertainties at the central elements.
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
def _(np, rs, srs):
    # Deterministic Shaft Elements
    Steel = rs.steel
    shaft = [rs.ShaftElement(L=0.25, material=Steel, idl=0, odl=0.05) for i in range(4)]

    # Material with random properties
    size = 50
    E = np.random.uniform(low=190e9, high=210e9, size=size)
    rho = np.random.uniform(low=7000, high=7810, size=size)
    G_s = np.random.uniform(low=70.5e9, high=81.2e9, size=size)
    rand_mat = srs.ST_Material(name="Steel", rho=rho, E=E, G_s=G_s)

    # Stochastic Shaft Elements
    rand_el = srs.ST_ShaftElement(
        L=0.25,
        idl=0,
        odl=0.05,
        material=rand_mat,
        is_random=["material"],
    )

    # Inserting stochastic elements to the shaft elements list
    shaft.insert(2, rand_el)
    shaft.insert(3, rand_el)

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
def _(rs):
    # random variables must have the same size
    bearing1 = rs.BearingElement(n=0, kxx=1e6, cxx=2e2)
    bearing2 = rs.BearingElement(n=6, kxx=1e6, cxx=2e2)
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
    fig = sample.plot_rotor()
    fig.show()
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
    fig1 = camp.plot_nat_freq(conf_interval=[95], width=950, height=700)
    fig1.show()
    return


@app.cell
def _(camp):
    # choose the desirable percentiles or confidence intervals
    fig2 = camp.plot_log_dec(conf_interval=[95], width=950, height=700)
    fig2.show()
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
