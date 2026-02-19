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
    Example 9 - Hydrodynamic Journal Bearings (using Fluid Flow methods)
    =====
    In this example, we use the hydrodynamic bearing seen in Example 5.5.1 from {cite}`friswell2010dynamics`.

    It is the same bearing of Example 7, only this time we stick to the methods provided by the Fluid Flow subpackage of ROSS. We instantiate a Pressure Matrix object with the data given by the Example 5.5.1 from the book: The oil-film bearing has a diameter of 100 mm, is 30 mm long, and supports a static load of 525 N. The radial clearance is 0.1 mm and the oil film has a viscosity of 0.1 Pa s. When instantiated, a Pressure Matrix must be given either the eccentricity, or load of the bearing, or both. The one not parameter not given is them calculated based on the other one.
    """)
    return


@app.cell
def _():
    from ross.bearings import fluid_flow as flow
    from ross.bearings.fluid_flow_geometry import (
        sommerfeld_number,
        modified_sommerfeld_number,
    )
    from ross.bearings.fluid_flow_graphics import plot_eccentricity, plot_pressure_theta
    from ross.bearings.fluid_flow_coefficients import (
        calculate_stiffness_and_damping_coefficients,
    )

    import numpy as np
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return (
        calculate_stiffness_and_damping_coefficients,
        flow,
        modified_sommerfeld_number,
        plot_eccentricity,
        plot_pressure_theta,
        sommerfeld_number,
    )


@app.cell
def _(flow):
    # Instantiating a Pressure Matrix
    nz = 8
    ntheta = 128
    length = 0.03
    omega = 157.1
    p_in = 0.0
    p_out = 0.0
    radius_rotor = 0.0499
    radius_stator = 0.05
    load = 525
    visc = 0.1
    rho = 860.0
    my_fluid_flow = flow.FluidFlow(
        nz,
        ntheta,
        length,
        omega,
        p_in,
        p_out,
        radius_rotor,
        radius_stator,
        visc,
        rho,
        load=load,
    )
    return my_fluid_flow, nz


@app.cell
def _(my_fluid_flow):
    # Getting the eccentricity

    my_fluid_flow.eccentricity
    return


@app.cell
def _(modified_sommerfeld_number, my_fluid_flow, sommerfeld_number):
    # Calculating the modified sommerfeld number and the sommerfeld number

    modified_s = modified_sommerfeld_number(
        my_fluid_flow.radius_stator,
        my_fluid_flow.omega,
        my_fluid_flow.viscosity,
        my_fluid_flow.length,
        my_fluid_flow.load,
        my_fluid_flow.radial_clearance,
    )

    sommerfeld_number(modified_s, my_fluid_flow.radius_stator, my_fluid_flow.length)
    return


@app.cell
def _(my_fluid_flow, plot_eccentricity):
    # Plotting the eccentricity

    plot_eccentricity(my_fluid_flow, scale_factor=0.5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The graphic above plots two circles: one representing the stator and one representing the rotor, considering the eccentricity. In this case, since the space between the stator and the rotor is very small, it is not seen in the graphic.
    """)
    return


@app.cell
def _(calculate_stiffness_and_damping_coefficients, my_fluid_flow):
    # Getting the stiffness and damping matrices

    K, C = calculate_stiffness_and_damping_coefficients(my_fluid_flow)
    return C, K


@app.cell
def _(C, K):
    print(f"Kxx, Kxy, Kyx, Kyy = {K}")
    print(f"Cxx, Cxy, Cyx, Cyy = {C}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The stiffness and damping matrices can be calculated analytically using the methods above.
    """)
    return


@app.cell
def _(my_fluid_flow, nz):
    # Calculating pressure matrix

    my_fluid_flow.calculate_pressure_matrix_numerical()[int(nz / 2)]
    return


@app.cell
def _(my_fluid_flow, nz, plot_pressure_theta):
    # Plotting pressure along theta in a chosen z

    plot_pressure_theta(my_fluid_flow, z=int(nz / 2))
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
