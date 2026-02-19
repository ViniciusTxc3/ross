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
    # Tutorial - Time and Frequency Analyzes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the third part of a basic tutorial on how to use ROSS (rotordynamics open-source software). In this tutorial, you will learn how to run time and frequency analyzes with your **rotor model**.

    To get results, we always have to use one of the `.run_` methods available for a rotor object. These methods will return objects that store the analysis results and that also have plot methods available. These methods will use the plotly library to make graphs common to a rotordynamic analysis.

    We can also use units when plotting results. For example, for a unbalance response plot we have the `amplitude_units` argument and we can choose between any length unit available in pint such as ‘meter’, ‘inch’, etc.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor model

    Again, let's recover the rotor model built in the previous tutorial.
    """)
    return


@app.cell
def _():
    import ross as rs
    from ross.units import Q_
    from ross.probe import Probe
    import numpy as np

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return Probe, Q_, np, rs


@app.cell
def _(rs):
    rotor3 = rs.compressor_example()
    rotor3.plot_rotor(nodes=5)
    return (rotor3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor Analyses

    There're some methods, most of them with the prefix `run_` you can use to run the rotordynamics analyses. For Most of the methods, you can use the command `.plot()` to display a graphical visualization of the results (e.g `run_freq_response().plot()`).

    ROSS offers the following analyses:
    - Frequency response
    - Unbalance response
    - Time response
    - Undamped Critical Speed Map

    ### Plotly library
    ROSS uses **Plotly** for plotting results. All the figures can be stored and manipulated following Plotly API.

    The following sections presents the results and how to return the Plotly Figures.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.1 Frequency Response

    ROSS' method to calculate the Frequency Response Function is `run_freq_response()`. This method returns the magnitude and phase in the frequency domain. The response is calculated for each node from the rotor model.

    When plotting the results, you can choose to plot:
    - **amplitude vs frequency**: `plot_magnitude()`
    - **phase vs frequency**: `plot_phase()`
    - **polar plot of amplitude vs phase**: `plot_polar_bode()`
    - **all**: `plot()`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.1 Clustering points

    The number of solution points is an important parameter to determine the computational cost of the simulation. Besides the classical method, using `numpy.linspace`, which creates an evenly spaced array over a specified interval, ROSS offers an automatic method to create an `speed_range` array.

    The method `clustering_points` generates an automatic array to run frequency response analyses. The frequency points are calculated based on the damped natural frequencies and their respective damping ratios. The greater the damping ratio, the more spread the points are. If the damping ratio, for a given critical speed, is smaller than 0.005, it is redefined to be 0.005 (for this method only).

    The main goal of this feature is getting a more accurate amplitude value for the respective critical frequencies and nearby frequency points.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.2 Running frequency response

    To run the this analysis, use the command `run_freq_response()`. You can give a specific `speed_range` or let the program run with the default options. In this case, no arguments are needed to input.

    First, let's run an example with a "user-defined" `speed_range`. Setting an array to `speed_range` will disable all the frequency spacing parameters.
    """)
    return


@app.cell
def _(np, rotor3):
    samples = 61
    speed_range = np.linspace(315, 1150, samples)  # rads/s
    results1 = rotor3.run_freq_response(speed_range=speed_range)
    return (results1,)


@app.cell
def _(results1):
    results1.speed_range.size
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's run an example using _clustering points_ array.
    """)
    return


@app.cell
def _():
    # results1_2 = rotor2.run_freq_response(cluster_points=True, num_points=5, num_modes=12)
    return


@app.cell
def _():
    # results1_2.speed_range.size
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the next section we'll check the difference between both results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1.3 Plotting results - Bode Plot

    We can plot the frequency response selecting the input and output degree of freedom.

    - Input is the degree of freedom to be excited;
    - Output is the degree of freedom to be observed.

    Each shaft node has 6 local degrees of freedom (dof) $[x, y, z, \alpha, \beta, \theta]$, and each degree of freedom has it own index:
    - $x$ &rarr; index 0
    - $y$ &rarr; index 1
    - $z$ &rarr; index 2
    - $\alpha$ &rarr; index 3
    - $\beta$ &rarr; index 4
    - $\theta$ &rarr; index 5

    To select a DoF to input and a DoF to the output, we have to use the following correlation:

    $global\_dof = node\_number \cdot  dof\_per\_node + dof\_index$

    For example:
    node 26, global dof $y$:
    """)
    return


@app.cell
def _(results1, rotor3):
    _node = 26
    global_dof = _node * rotor3.number_dof + 1
    plot = results1.plot(inp=global_dof, out=global_dof)
    # converting the first plot yaxis to log scale
    # plot = results1.plot(inp=global_dof, out=global_dof)
    # plot.update_yaxes(type="log", row=1, col=1)
    # plot
    plot
    return


@app.cell
def _():
    # plot1_2 = results1_2.plot(inp=global_dof, out=global_dof)
    # plot1_2

    # # converting the first plot yaxis to log scale
    # plot1_2 = results1_2.plot(inp=global_dof, out=global_dof)
    # plot1_2.update_yaxes(type="log", row=1, col=1)
    # plot1_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.2 Unbalance Response


    ROSS' method to simulate the reponse to an unbalance is `run_unbalance_response()`. This method returns the unbalanced response in the frequency domain for a given magnitide and phase of the unbalance, the node where it's applied and a frequency range.

    ROSS takes the magnitude and phase and converts to a complex force array applied to the given node:

    $$
    force = \left(\begin{array}{cc}
    F \cdot e^{j\delta}\\
    -jF \cdot e^{j\delta}\\
    0\\
    0
    \end{array}\right)
    $$

    where:
    - $F$ is the unbalance magnitude;
    - $\delta$ is the unbalance phase;
    - $j$ is the complex number notation;

    When plotting the results, you can choose to plot the:
    - Bode plot options for a single degree of freedom:
        - amplitude vs frequency: `plot_magnitude()`
        - phase vs frequency: `plot_phase()`
        - polar plot of amplitude vs phase: `plot_polar_bode()`
        - all: `plot()`
    - Deflected shape plot options:
        - deflected shape 2d: `plot_deflected_shape_2d()`
        - deflected shape 3d: `plot_deflected_shape_3d()`
        - bending moment: `plot_bending_moment()`
        - all: `plot_deflected_shape()`

    `run_unbalance_response()` is also able to work with clustering points ( _see section 7.4.1_ ).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.1 Running unbalance response

    To run the Unbalance Response, use the command `.unbalance_response()`

    In this following example, we can obtain the response for a given unbalance and its respective phase in a selected node. Notice that it's possible to add multiple unbalances instantiating node, magnitude and phase as lists.

    The method returns the force response array (complex values), the displacement magnitude (absolute value of the forced response) and the phase of the forced response.

    Let's run an example with 2 unbalances in phase, trying to excite the first and the third natural vibration mode.
    ```text
    Unbalance1: node = 29
                magnitude = 0.003
                phase = 0
    Unbalance2: node = 33
                magnitude = 0.002
                phase = 0
    ```
    """)
    return


@app.cell
def _(np, rotor3):
    n1 = 29
    m1 = 0.003
    _p1 = 0
    n2 = 33
    m2 = 0.002
    _p2 = 0
    frequency_range = np.linspace(315, 1150, 101)
    results2 = rotor3.run_unbalance_response([n1, n2], [m1, m2], [_p1, _p2], frequency_range)
    return (results2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.2 Plotting results - Bode Plot

    To display the bode plot, use the command `.plot(probe)`

    Where `probe` is a list of Probe objects that allows you to choose not only the node where to observe the response, but also the orientation.

    Probe orientation equals 0° refers to `+X` direction (DoFX), and probe orientation equals 90° (or $\frac{\pi}{2} rad$) refers to `+Y` direction (DoFY).

    You can insert multiple probes at once.
    """)
    return


@app.cell
def _(Probe, Q_, results2):
    # probe = Probe(probe_node, probe_orientation)
    _probe1 = Probe(15, Q_(45, 'deg'))  # node 15, orientation 45°
    _probe2 = Probe(35, Q_(45, 'deg'))  # node 35, orientation 45°
    # converting the first plot yaxis to log scale
    # plot2 = results2.plot(probe=[probe1, probe2], probe_units="rad")
    # plot2.update_yaxes(type="log", row=1, col=1)
    # plot2
    results2.plot(probe=[_probe1, _probe2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2.3 Plotting results - Deflected shape

    To display the deflected shape configuration, use the command `.plot_deflected_shape()`
    """)
    return


@app.cell
def _(results2):
    results2.plot_deflected_shape(speed=649)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.3 Time Response

    ROSS' method to calculate displacements due a force in time domain is `run_time_response()`. This function will take a rotor object and plot its time response given a force and a time array.

    There are two ways to obtain the numerical solution:
    - one by solving the system of equations in state space, and
    - the other by numerical integration using the Newmark method.

    The force input must be a matrix $M \times N$, where:
    - $M$ is the size of the time array;
    - $N$ is the rotor's number of DoFs (you can access this value via attribute `.ndof`).

    Each row from the matrix represents a node, and each column represents a time step.

    Time Response allows you to plot the response for:
    - a list of probes
    - an orbit for a given node (2d plot)
    - all the nodes orbits (3d plot)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3.1 Running time response in state space

    To run the Time Response, use the command `.run_time_response()`.

    Building the force matrix is not trivial. We recommend creating a matrix of zeros using *numpy.zeros()* and then, adding terms to the matrix.

    #### 1.3.1.1 Considering harmonic force
    In this examples, let's create an harmonic force on node 26, in $x$ and $y$ directions (remember index notation from Frequency Response (section 7.4.2). We'll plot results from 0 to 16 seconds of simulation.
    """)
    return


@app.cell
def _(np, rotor3):
    time_samples = 1001
    t = np.linspace(0, 16, time_samples)
    speed = 600.0
    _node = 26
    F = np.zeros((time_samples, rotor3.ndof))
    F[:, _node * rotor3.number_dof + 0] = 10 * np.cos(2 * t)
    F[:, _node * rotor3.number_dof + 1] = 10 * np.sin(2 * t)
    # component on direction x
    # component on direction y
    response3 = rotor3.run_time_response(speed, F, t)
    return (response3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 1.3.1.2 Plotting results

    There 3 (three) different options to plot the time response:
    - `.plot_1d()`: plot time response for given probes.
    - `.plot_2d()`: plot orbit of a selected node of a rotor system.
    - `.plot_3d()`: plot orbits for each node on the rotor system in a 3D view.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Ploting time response for list of probes
    """)
    return


@app.cell
def _(Probe, Q_, response3):
    _probe1 = Probe(3, 0)  # node 3, orientation 0° (X dir.)
    _probe2 = Probe(3, Q_(90, 'deg'))  # node 3, orientation 90°(Y dir.)
    response3.plot_1d(probe=[_probe1, _probe2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Ploting orbit response for a single node
    """)
    return


@app.cell
def _(response3):
    response3.plot_2d(node=26)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Ploting orbit response for all nodes
    """)
    return


@app.cell
def _(response3):
    response3.plot_3d()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 1.3.1.3 Considering coded force methods

    In this example, we consider two forces of excitation:
    - Unbalance Force ($F_{unb}$): The method `.unbalance_force_over_time()` calculates this time-varying force and returns a force array of shape `(ndof, len(t))`.

    - Weight ($W$): The method `.gravitational_force()` returns a static force array of shape `(ndof,)`, which must be expanded to match the time dimension.

    - Force Combination:
    $
    F(t) = F_{unb}(t) + W
    $
    """)
    return


@app.cell
def _(Probe, Q_, np, rotor3):
    _dt = 0.001
    t_1 = np.arange(0, 16, _dt)
    speed_1 = 600.0
    _node = 29
    _Funb = rotor3.unbalance_force_over_time(node=[_node], magnitude=[0.003], phase=[0], omega=speed_1, t=t_1)
    W = rotor3.gravitational_force(direction='y')
    F_1 = (_Funb + W[:, np.newaxis]).T
    response3_2 = rotor3.run_time_response(speed_1, F_1, t_1)
    response3_2.plot_dfft(probe=[Probe(_node, 0), Probe(_node, Q_(90, 'deg'))], frequency_units='rad/s')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3.2 Running time response with Newmark method

    To run the Time Response in this case, use the command `.run_time_response()` with the argument `method="newmark"`.

    One of the advantages of this method is that we can consider an array of rotor velocities as a function of time, rather than just a constant velocity. Additionally, we can pass a callable function as an argument that returns an array of forces to be added to the right-hand side of the system of equations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 1.3.2.1 Considering speed variation

    To illustrate this, let’s now consider just an unbalance force applied at node 29, with a run-up to 600 rad/s over 3 seconds.
    """)
    return


@app.cell
def _(Probe, Q_, np, rotor3):
    _dt = 0.001
    t_2 = np.arange(0, 3, _dt)
    speed_2 = np.linspace(0, 600.0, len(t_2))
    _node = 29
    _Funb = rotor3.unbalance_force_over_time(node=[_node], magnitude=[0.003], phase=[0], omega=speed_2, t=t_2)
    F_2 = _Funb.T
    response3_n1 = rotor3.run_time_response(speed_2, F_2, t_2, method='newmark')
    response3_n1.plot_1d(probe=[Probe(_node, 0), Probe(_node, Q_(90, 'deg'))])
    return F_2, speed_2, t_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 1.3.2.3 Custom external forces with `add_to_RHS`

    The `add_to_RHS` argument allows the user to dynamically modify the external force array applied to the rotor during time integration. In addition to a predefined force array $F$, an additional contribution can be introduced at each time step through a custom function, for example `calc_force`.

    This function is called automatically at every time step of the simulation and receives the following arguments:
    - **step**: Current step index in the simulation.
    - **time_step**: Current simulation time.
    - **disp_resp**: Displacement response at the current step (useful if the force depends on displacement).
    - **velc_resp**: Velocity response at the current step.
    - **accl_resp**: Acceleration response at the current step.

    The function must return the additional force array for that time step. This enables the implementation of forces that are nonlinear or state-dependent (e.g. feedback control, impact forces).


    For example:
    """)
    return


@app.cell
def _(F_2, rotor3, speed_2, t_2):
    def calc_force(step, time_step, disp_resp, velc_resp, accl_resp):
        damping_force = -0.01 * velc_resp  # Example: Add a damping-dependent force
        return damping_force
    response3_n2 = rotor3.run_time_response(speed_2, F_2, t_2, method='newmark', add_to_RHS=calc_force)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.4 Harmonic Balance Method (HBM)
    The Harmonic Balance Method (HBM) enables the computation of steady-state periodic responses of rotor systems subjected to harmonic excitations.
    Unlike traditional time-domain integration methods, HBM determines the system response directly in the frequency domain, providing an efficient and accurate approach for steady-state vibration analysis.

    To run the Harmonic Balance Method, use the command `.run_harmonic_balance_response()`.

    This routine computes the steady-state harmonic response and provides post-processing tools for:
    - Frequency-domain analysis;
    - Time-domain reconstruction.

    Compared to the conventional `.run_time_response()` approach, the execution time of `.run_harmonic_balance_response()` is significantly reduced, since it avoids numerical integration over time. This emphasizes the computational efficiency of the Harmonic Balance approach for steady-state analyses.

    The current implementation follows the methodology proposed by {cite}`cunha2025`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4.1 Running

    Consider a rotor system subjected to the following harmonic excitation forces:

    $$
    F_{x,29}(t) = A_1 \cos(\omega t + p_1) + A_2 \cos(2\omega t + p_2) + A_3 \cos(3\omega t + p_3),
    $$

    $$
    F_{y,29}(t) = A_1 \sin(\omega t + p_1) + A_2 \sin(2\omega t + p_2) + A_3 \sin(3\omega t + p_3),
    $$

    $$
    F_{x,33}(t) = m \, e \, \omega^2 \cos(\omega t),
    $$

    $$
    F_{y,33}(t) = m \, e \, \omega^2 \sin(\omega t).
    $$

    These expressions represent a combination of multi-harmonic excitations applied at node 29, and a classical unbalance excitation applied at node 33, where $\omega$ is rotational angular frequency (rad/s), $t$ is time (s), $A$ is force amplitude (N), $p$ is phase angle (rad), $m$ is unbalance mass (kg), and $e$ is eccentricity of the unbalance (m).
    """)
    return


@app.cell
def _(np, rotor3, rs):
    speed_3 = 200.0
    t_3 = np.arange(0, 10, 0.0001)
    (A1, A2, A3) = (1.0, 10.0, 5.0)
    (_p1, _p2, p3) = (0.0, 0.0, 0.0)
    (m, e) = (0.2, 0.01)
    probe = rs.Probe(15, rs.Q_(45, 'deg'))
    hb_results = rotor3.run_harmonic_balance_response(speed=speed_3, t=t_3, harmonic_forces=[{'node': 29, 'magnitudes': [A1, A2, A3], 'phases': [_p1, _p2, p3], 'harmonics': [1, 2, 3]}, {'node': 33, 'magnitudes': [m * e * speed_3 ** 2], 'phases': [0], 'harmonics': [1]}], n_harmonics=3)
    return hb_results, probe


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4.2 Plotting frequency-domain response
    """)
    return


@app.cell
def _(hb_results, probe):
    hb_fig = hb_results.plot([probe], frequency_units="Hz")
    hb_fig
    return (hb_fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4.3 Plotting deflected shape
    """)
    return


@app.cell
def _(hb_results):
    hb_results.plot_deflected_shape()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4.4 Time-domain reconstruction of the steady-state response
    """)
    return


@app.cell
def _(hb_results, probe):
    hb_time_resp = hb_results.get_time_response()
    hb_time_resp.plot_1d([probe])
    return (hb_time_resp,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4.5  Comparison – Harmonic Balance vs. DFFT Spectrum
    """)
    return


@app.cell
def _(hb_fig, hb_time_resp, rs):
    hb_time_resp.plot_dfft(
        probe=[rs.Probe(15, rs.Q_(45, "deg"), tag="DFFT")],
        frequency_units="Hz",
        frequency_range=(0, 100),
        yaxis_type="log",
        fig=hb_fig,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1.5 Undamped Critical Speed Map (UCS)
    This method will plot the undamped critical speed map for a given range of stiffness values. If the range is not provided, the bearing stiffness at rated speed will be used to create a range.

    Whether a synchronous analysis is desired, the method selects only the foward modes and the frequency of the first forward mode will be equal to the speed.

    To run the UCS Map, use the command `.plot_ucs()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.5.1 Running and plotting UCS Map

    In this example the UCS Map is calculated for a stiffness range from **10E6** to **10E11** N/m. The other options are left to default.
    """)
    return


@app.cell
def _(rotor3):
    stiff_range = (6, 11)
    ucs_results = rotor3.run_ucs(stiffness_range=stiff_range, num=20, num_modes=16)
    ucs_fig = ucs_results.plot()
    ucs_fig
    return


if __name__ == "__main__":
    app.run()
