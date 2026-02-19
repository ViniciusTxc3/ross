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
    # Tutorial - Static and Modal Analyzes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the second part of a basic tutorial on how to use ROSS (rotordynamics open-source software), a Python library for rotordynamic analysis. In this tutorial, you will learn how to run several rotordynamic analyzes with your **rotor model**.

    To get results, we always have to use one of the `.run_` methods available for a rotor object. These methods will return objects that store the analysis results and that also have plot methods available. These methods will use the plotly library to make graphs common to a rotordynamic analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor model

    First, let's recover the rotor model built in the previous tutorial.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio
    import plotly.graph_objects as go

    pio.renderers.default = "notebook"
    return np, rs


@app.cell
def _(rs):
    rotor3 = rs.compressor_example()
    node_increment = 5
    rotor3.plot_rotor(nodes=node_increment)
    return (rotor3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor Analyses

    In the last tutorial we have learnt how to create a rotor model with `Rotor` class. Now, we'll use the same class to run the simulation. There're some methods, most of them with the prefix `run_` you can use to run the rotordynamics analyses.

    For Most of the methods, you can use the command `.plot()` to display a graphical visualization of the results (e.g `run_campbel().plot()`, `run_modal().plot_mode_3d(mode)`).

    ROSS offers the following analyses:
    - Static analysis
    - Modal analysis
    - Campbell Diagram


    ### Plotly library
    ROSS uses **Plotly** for plotting results. All the figures can be stored and manipulated following Plotly API.

    The following sections presents the results and how to return the Plotly Figures.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1 Static Analysis

    This method runs the static analysis for the rotor. It calculate the static deformation due the gravity effects (shaft and disks weight). It also returns the bending moment and shearing force on each node, and you can return a free-body-diagram representation for the rotor, with the self weight, disks weight and reaction forces on bearings displayed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.1 Running static analysis

    To run the simulation, use the `.run_static()` method. You can define a variable to store the results.

    Storing the results, it's possible to return the following arrays:
    - `disk_forces_nodal`
    - `disk_forces_tag`
    - `bearing_forces_nodal`
    - `bearing_forces_tag`
    - `disp_y`
    - `Vx`
    - `Bm`
    """)
    return


@app.cell
def _(rotor3):
    static = rotor3.run_static()
    return (static,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning forces

    #### Disk forces
    - `.disk_forces_nodal`:
    Returns a dictionaty expliciting the node where the disk is located and the force value.

    - `.disk_forces_tag`:
    Returns a dictionaty expliciting the the disk tag is located and the force value.

    #### Bearing forces
    - `.bearing_forces_nodal`:
    Returns a dictionaty expliciting the node where the bearing is located and the force value.

    - `.bearing_forces_tag`:
    Returns a dictionaty expliciting the the bearing tag is located and the force value.
    """)
    return


@app.cell
def _(rotor3):
    print("Disk forces - nodes")
    print(rotor3.disk_forces_nodal)
    print("")
    print("Disk forces - tags")
    print(rotor3.disk_forces_tag)

    print("")
    print("Bearing forces - nodes")
    print(rotor3.bearing_forces_nodal)
    print("")
    print("Bearing forces - tags")
    print(rotor3.bearing_forces_tag)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Other attributes from static analysis
    - `.Vx`: Shearing force array
    - `.Bm`: Bending moment array
    - `.deformation` Displacement in Y direction
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.2 Plotting results

    With results stored, you can use some methods to plot the results. Currently, there're four plots you can retrieve from static analysis:

    - `.plot_free_body_diagram()`
    - `.plot_deformation()`
    - `.plot_shearing_force()`
    - `.plot_bending_moment()`


    #### Plotting free-body-diagram
    """)
    return


@app.cell
def _(static):
    static.plot_free_body_diagram()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting deformation
    """)
    return


@app.cell
def _(static):
    static.plot_deformation()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting shearing force diagram
    """)
    return


@app.cell
def _(static):
    static.plot_shearing_force()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting bending moment diagram
    """)
    return


@app.cell
def _(static):
    static.plot_bending_moment()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.2 Modal Analysis

    ROSS performs the modal analysis through method `run_modal()`.
    This method calculates natural frequencies, damping ratios and mode shapes.

    You must select a speed, which will be used as excitation frequency to calculate the system's eigenvalues and eigenvectors, and the number of eigenvalues and eigenvectors to be calculated is an optional argument (`num_modes`).

    After running the modal analysis, it's possible to return the following attributes:
    - eigenvalues (evalues);
    - eigenvectors (evectors);
    - damped natural frequencies (wd);
    - undamped natural frequencies (wn);
    - damping ratio (damping_ratio);
    - logarithmic decrement (log_dec).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.1 Running modal analysis

    To run the modal analysis, choose a speed to instantiate the method. For different speeds, change the the argument and run `run_modal()` once again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning undamped natural frequencies
    """)
    return


@app.cell
def _(rotor3):
    rotor_speed = 100.0  # rad/s
    modal = rotor3.run_modal(rotor_speed, num_modes=16)
    print(f"Undamped natural frequencies:\n {modal.wn}")
    return (modal,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning damped natural frequencies
    """)
    return


@app.cell
def _(modal):
    # modal.wd
    print(f"Damped natural frequencies:\n {modal.wd}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning the damping ratio
    """)
    return


@app.cell
def _(modal):
    # modal.damping_ratio
    print(f"Damping ratio for each mode:\n {modal.damping_ratio}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning logarithmic decrement
    """)
    return


@app.cell
def _(modal):
    # modal.log_dec
    print(f"Logarithmic decrement for each mode:\n {modal.log_dec}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.2 Plotting results

    Once `run_modal()` is completed, you can check for the rotor's mode shapes. You can plot each one of the modes calculated.

    Besides, there're two options for visualization:
    - `plot_mode_2d` - plotting 2D view
    - `plot_mode_3d` - plotting 3D view
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting 3D view

    Use the command `.plot_mode_3d(mode)`.
    """)
    return


@app.cell
def _(modal):
    mode = 5
    modal.plot_mode_3d(mode)
    return (mode,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting 2D view

    Use the command `.plot_mode_2d(mode)`.
    """)
    return


@app.cell
def _(modal, mode):
    modal.plot_mode_2d(mode)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Torsional analysis

    You can filter modes by the mode type attribute ("Lateral", "Axial", "Torsional"), for example:
    """)
    return


@app.cell
def _(modal):
    torsional_modes = [
        mode for mode, shape in enumerate(modal.shapes) if shape.mode_type == "Torsional"
    ]
    torsional_modes
    return (torsional_modes,)


@app.cell
def _(modal, torsional_modes):
    modal.plot_mode_3d(torsional_modes[0], animation=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.3 Campbell Diagram

    Also called "whirl speed map" in rotordynamics, ROSS calculate and plots the modes’ damped eigenvalues and the logarithmic decrement as a function of rotor speed.

    To run the Campbell Diagram, use the command `.run_campbell()`. The user must input an array of speeds, which will be iterated to calculate each point on the graph.

    This method returns the damped natural frequencies, logarithmic decrement and the whirl values (values indicating the whirl direction: backward or forward).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3.1 Running campbell diagram

    In this example the whirl speed map is calculated for a speed range from 0 to 1000 rad/s (~9550 RPM).

    Storing the results, it's possible to return the following arrays:
    - `wd`
    - `log_dec`
    - `whirl_values`

    Each value in these arrays is calculated for each speed value in `speed_range`
    """)
    return


@app.cell
def _(np, rotor3):
    samples = 31
    speed_range = np.linspace(315, 1150, samples)

    campbell = rotor3.run_campbell(speed_range)
    return (campbell,)


@app.cell
def _(campbell):
    # results for each frequency
    _frequency_index = 0
    print(campbell.wd[:, _frequency_index])
    return


@app.cell
def _(campbell):
    # results for each frequency
    _frequency_index = 1
    print(campbell.log_dec[:, _frequency_index])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3.2 Plotting results

    Now that the results are stored, use `.plot()` method to display the Campbell Diagram plot.

    For the Campbell Diagram, you can plot more than one harmonic. As default, the plot display only the 1x speed option.
    Input a list with more harmonics to display it at the graph.
    """)
    return


@app.cell
def _(campbell):
    campbell.plot(harmonics=[0.5, 1])
    return


if __name__ == "__main__":
    app.run()
