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
    Tutorial - Active Magnetic Bearings
    ======================
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tutorial provides a comprehensive guide on how to model, simulate, and analyze Active Magnetic Bearings (AMBs) using ROSS.

    ## Section 1: Introduction and Working Principle

    **Active Magnetic Bearings (AMBs)** are support mechanisms that levitate a rotating shaft using electromagnetic forces, eliminating physical contact between the rotor and the stator.

    ### 1.1 Working Principle

    An AMB system operates as a closed-loop feedback control system consisting of three main components:

    1. **Sensors:** Measure the radial displacement of the rotor ($x$).
    2. **Controller:** Processes the displacement signal and calculates the necessary current correction ($i$) to maintain the rotor's position (setpoint).
    3. **Actuators (Electromagnets):** Receive the current and generate the magnetic force required to pull the rotor back to the center.

    ### 1.2 Mathematical Model

    In ROSS, the electromagnetic force $F$ is linearized around a nominal operating point (bias current $i_0$ and nominal gap $g_0$). The force equation is generally described by:

    $$
     F = K_i \; i + K_s \; x
    $$

    Where:

    - $K_i$ is the **current stiffness** (Force/Current factor).
    - $K_s$ is the **negative electromagnetic stiffness** (Force/Displacement factor), representing the inherent instability of the magnetic attraction.

    ## Section 2: Declaring a Magnetic Bearing in ROSS

    To use an AMB in ROSS, you must instantiate the `MagneticBearingElement` class. You need to provide physical parameters of the electromagnet and the gains for the PID controller.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    n_node = 4
    # Physical parameters of the actuator
    g0 = 0.001  # Node where the bearing is located
    i0 = 1.0  # Nominal air gap (m)
    ag = 0.0001  # Bias current (A)
    nw = 200  # Pole area (m²)
    _alpha = np.pi / 8  # Number of windings
    _Kp = 1500  # Pole angle (rad)
    _Kd = 10
    # PID Controller gains
    _Ki = 100  # Proportional gain
    # Instantiation
    amb = rs.MagneticBearingElement(n=n_node, g0=g0, i0=i0, ag=ag, nw=nw, alpha=_alpha, kp_pid=_Kp, kd_pid=_Kd, ki_pid=_Ki, tag='AMB_1')  # Derivative gain  # Integral gain
    return np, rs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 3: Evaluating Time Response

    Since AMBs are active control systems that calculate forces based on instantaneous states, **numerical integration must be performed using the Newmark method**.

    When `method="newmark"` is selected, ROSS calls the `magnetic_bearing_controller` loop at every time step. This calculates the error, updates the controller state, and applies the resulting magnetic force to the rotor.

    **Important:** If you use other methods (like modal integration), the AMB forces might not be updated correctly as they depend on the feedback loop.
    """)
    return


@app.cell
def _(rs):
    rotor = rs.rotor_amb_example()
    # 1. Create the rotor with the AMB element
    rotor.plot_rotor(nodes=999).show()
    return (rotor,)


@app.cell
def _(np, rotor, rs):
    # Define the node to observe (e.g., node 0)
    obs_node = 12
    force_node = 28
    speed = 500.0
    # 2. Define simulation parameters
    t = np.arange(0, 3, 0.001)  # rad/s
    _F = np.zeros((len(t), rotor.ndof))  # Time vector
    index = np.nonzero(t > 0.5)[0][0]  # External force vector (e.g., 0 for free response)
    _F[index, rotor.number_dof * force_node + 1] = 10
    # Impulse force in y-axis at 0.5 seconds
    response = rotor.run_time_response(speed, _F, t, method='newmark')
    probe_y = rs.Probe(node=obs_node, angle=np.pi / 2)
    _fig = response.plot_1d(probe=[probe_y])
    # 3. Run time response explicitly using Newmark
    # This ensures the AMB control loop is active at every step
    # 4. Plot time response (1D)
    # Define a probe at the desired node with a specific angle (π/2 rad = Y axis)
    # Pass the probe as a list to the plot_1d method
    _fig.show()
    return (t,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 4: Collecting Forces and Control Currents

    During the `run_time_response` (with Newmark), ROSS stores the internal states of the magnetic bearing. These include the control currents calculated by the PID and the resulting magnetic forces applied to the shaft.

    These data are stored as attributes within the `MagneticBearingElement` object itself after the simulation finishes.
    """)
    return


@app.cell
def _(rotor, t):
    import plotly.graph_objects as go
    amb_element = rotor.bearing_elements[0]
    # Access the specific bearing element from the rotor object
    currents_x = amb_element.control_signal[0]
    currents_y = amb_element.control_signal[1]
    # Retrieve data (stored as lists for each time step)
    # The structure is {amb_element}.{signal_name}[axis_index]
    # Axis index: 0 for x, 1 for y.
    forces_x = amb_element.magnetic_force_xy[0]
    # 1. Control Signal (Currents in Amperes)
    forces_y = amb_element.magnetic_force_xy[1]
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=t, y=currents_x, mode='lines', name='Courent X axis'))
    # 2. Magnetic Forces (Newtons)
    _fig.update_layout(title='Control current - X axis', xaxis_title='Time (s)', yaxis_title='Current (A)', width=800, height=600)
    # Plotting
    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 5: Sensitivity Analysis (ISO 14839)

    ### 5.1 Definition and ISO Standard

    The sensitivity function $S(j\omega)$ determines the robustness of the control system. According to **ISO 14839-3**, the sensitivity is the ratio of the sensor output to a disturbance added to the sensor signal. It represents how much a disturbance is amplified by the feedback loop.

    $$
    S(j\omega) = \frac{1}{1 + G(j\omega)H(j\omega)}
    $$

    The ISO standard classifies the stability margin based on the **peak sensitivity value ($S_{max}$)**:

    - **Zone A ($S_{max} < 3.0$):** Unrestricted operation (approx 9.5 dB).
    - **Zone B ($3.0 < S_{max} < 4.0$):** Restricted operation.
    - **Zone C ($S_{max} > 4.0$):** Evaluation required, potential instability.

    ### 5.2 Simulation Procedure in ROSS

    To calculate the sensitivity function, ROSS performs a specific time-domain simulation:

    1. A **Logarithmic Chirp Signal** (sweeping sine wave) is injected as a disturbance into the control loop at the AMB sensor location.
    2. The system response (displacement) is recorded.
    3. A Frequency Response Function (FRF) is computed between the **Output (Disturbed Signal)** and the **Input (Excitation Signal)**.
    """)
    return


@app.cell
def _(rotor):
    # Run sensitivity analysis
    # This automatically performs the chirp injection and FFT computation
    sensitivity_results = rotor.run_amb_sensitivity(
        speed=0,
        t_max=45,  # Duration must be long enough for the chirp
        dt=1e-3,  # Time step
        disturbance_amplitude=1e-5,
        disturbance_min_frequency=0.001,  # Hz
        disturbance_max_frequency=150,
        amb_tags=["Magnetic Bearing 0"],
        verbose=0,
    );
    return (sensitivity_results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5.3 The `SensitivityResults` Object

    The `run_amb_sensitivity` method returns a `SensitivityResults` object. Below is a summary of its attributes and methods.

    #### Attributes Table

    | Attribute | Type | Description |
    | --- | --- | --- |
    | `sensitivities` | `dict` | Dictionary containing the complex Sensitivity FRF ($S(j\omega)$) for each AMB and axis ($x$, $y$). |
    | `sensitivities_abs` | `dict` | The magnitude (absolute value) of the sensitivity function. |
    | `sensitivities_phase` | `dict` | The phase angle of the sensitivity function. |
    | `sensitivities_frequencies` | `np.ndarray` | The frequency vector (in Hz) corresponding to the sensitivity arrays. |
    | `max_abs_sensitivities` | `dict` | The peak sensitivity value ($S_{max}$) for each AMB/axis. Used for ISO classification. |
    | `sensitivity_run_time_results` | `dict` | Contains raw time-domain arrays: `excitation_signal` (chirp), `disturbed_signal` (input to controller), and `sensor_signal`. |
    | `sensitivity_compute_dofs` | `dict` | Mapping of AMB tags to their corresponding Degree of Freedom indices. |

    #### Accessing Results Data

    The attributes within the `SensitivityResults` object (such as `max_abs_sensitivities`, `sensitivities`, `sensitivities_abs`, and `sensitivities_phase`) are organized as **nested dictionaries**. This structure allows you to easily retrieve data for a specific magnetic bearing and a specific axis.

    **Structure Hierarchy:**

    1. **First Level Key:** The AMB tag (string), exactly as defined when creating the `MagneticBearingElement`.
    2. **Second Level Key:** The axis (string), either `"x"` or `"y"`.
    3. **Value:** The corresponding data (scalar for max sensitivity, or array for FRFs).

    **Visual Representation:**

    ```python
    sensitivity_results.max_abs_sensitivities = {
        "AMB_Tag_1": {
            "x": <scalar_value>,
            "y": <scalar_value>
        },
        "AMB_Tag_2": {
            "x": <scalar_value>,
            "y": <scalar_value>
        }
        # ...
    }
    ```

    **Example: Retrieving Maximum Sensitivity**

    The following example demonstrates how to programmatically access the maximum absolute sensitivity ($S_{max}$) for a specific axis of a specific bearing to check against ISO limits.
    """)
    return


@app.cell
def _(sensitivity_results):
    # Assume 'sensitivity_results' is the object returned by rotor.run_amb_sensitivity()

    # 1. Define the target Bearing Tag and Axis
    target_amb_tag = (
        "Magnetic Bearing 0"  # Must match the 'tag' used in MagneticBearingElement
    )
    target_axis = "x"

    # 2. Access the nested dictionary
    s_max = sensitivity_results.max_abs_sensitivities[target_amb_tag][target_axis]

    print(f"Peak Sensitivity for {target_amb_tag} ({target_axis}-axis): {s_max:.4f}")

    # 3. Check against ISO 14839-3 Zone A limit
    if s_max < 3.0:
        print("Result: Zone A (Unrestricted Operation)")
    else:
        print("Result: Zone B or C (Evaluation required)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plotting Methods

    **`.plot()`**

    Displays the Bode plot (Magnitude and Phase) of the sensitivity function. This is the primary tool to check compliance with ISO 14839.
    """)
    return


@app.cell
def _(sensitivity_results):
    # Plot Bode diagram of Sensitivity
    fig_bode = sensitivity_results.plot(
        frequency_units="Hz",
        magnitude_scale="decibel",  # Useful to check margins in dB
        xaxis_type="log",
    )
    fig_bode.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`.plot_time_results()`**

    Displays the raw time-domain signals used to calculate the sensitivity. This is useful for debugging to ensure the chirp signal was applied correctly and the system remained stable during the test.
    """)
    return


@app.cell
def _(sensitivity_results):
    # Plot the Chirp injection and system response
    fig_time = sensitivity_results.plot_time_results()
    fig_time.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 6: Implementing Complex Controllers (Cascade)

    ROSS supports arbitrary transfer functions using the `python-control` library. You can combine controllers (e.g., in series/cascade) by multiplying their transfer functions.

    **Example:** A PID controller cascaded with a **Lead Compensator** (to improve phase margin).
    """)
    return


@app.cell
def _(rs):
    import control as ct
    s = rs.MagneticBearingElement.s
    (_Kp, _Ki, _Kd) = (1500, 100, 10)
    TF_PID = _Kp + _Ki / s + _Kd * s
    _alpha = 3.0
    T = 0.001
    TF_Lead = (_alpha * T * s + 1) / (T * s + 1)
    TF_Combined = TF_PID * TF_Lead
    amb_cascade = rs.MagneticBearingElement(n=4, g0=0.001, i0=1.0, ag=0.0001, nw=200, controller_transfer_function=TF_Combined, tag='AMB_Cascade')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ROSS handles the discretization and state-space conversion of `TF_Combined` automatically during the simulation.

    It is worth noting that, if necessary, the `MagneticBearingElement` can still be defined by specifying only the `kp_pid`, `ki_pid`, and `kd_pid` parameters.


    ### 6.1 Auxiliary Methods for Defining and Evaluating Transfer Functions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Conventions and returned types

    All “controller builder” functions return **python-control transfer functions** (`control.TransferFunction`), except where noted:

    * `pid(...)` → `TransferFunction`
    * `lead_lag(...)` → `TransferFunction`
    * `second_order(...)` → `TransferFunction`
    * `low_pass_filter(...)` → `TransferFunction`
    * `notch_filter(...)` → `TransferFunction`
    * `lqg(...)` → `TransferFunction` (converted from state-space to TF internally)
    * `combine(*args)` → product of transfer functions (series connection)
    """)
    return


@app.cell
def _():
    from ross.bearings.magnetic.controllers import pid, lqg, lead_lag, second_order, low_pass_filter, notch_filter, combine, plot_frequency_response

    return (
        combine,
        lead_lag,
        low_pass_filter,
        lqg,
        notch_filter,
        pid,
        plot_frequency_response,
        second_order,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below, each of the auxiliary methods introduced above is described in detail.

    **`pid(k_p, k_i, k_d, n_f=10000)`**

    Builds a PID controller with a **filtered derivative** term.

    * `k_p` *(float)*: proportional gain
    * `k_i` *(float)*: integral gain
    * `k_d` *(float)*: derivative gain
    * `n_f` *(float, optional)*: derivative filter “corner” scaling (higher → closer to ideal derivative without filtering)
    """)
    return


@app.cell
def _(pid):
    C = pid(k_p=3.0, k_i=5.0, k_d=0.02, n_f=300)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`lqg(A, B, C, Q_lqr, R_lqr, Q_kalman, R_kalman)`**

    Builds an **LQG controller** (LQR state feedback + Kalman filter) and returns it as a transfer function.

    * `A`, `B`, `C`: system matrices (array-like). Converted to `float` numpy arrays.
    * `Q_lqr`, `R_lqr`: LQR weighting matrices.
    * `Q_kalman`, `R_kalman`: process/measurement noise covariances for the Kalman filter design.

    **Notes / tips**

    * Dimensions must match python-control expectations, where `n`, `m`, and `p` are, respectively, the number of states, controls, and outputs.:
      * `A` is `(n, n)`, `B` is `(n, m)`, `C` is `(p, n)`
      * `Q_lqr` is `(n, n)`, `R_lqr` is `(m, m)`
      * `Q_kalman` is `(n, n)`, `R_kalman` is `(p, p)`
    """)
    return


@app.cell
def _(lqg, np):
    A = [[0, 1], [-2, -0.5]]
    B = [[0], [1]]
    C_1 = [[1, 0]]
    Q_lqr = np.diag([10, 1])
    R_lqr = np.array([[1]])
    Q_kalman = np.diag([0.1, 0.1])
    R_kalman = np.array([[0.5]])
    C_lqg = lqg(A, B, C_1, Q_lqr, R_lqr, Q_kalman, R_kalman)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`lead_lag(tau, alpha, k=1.0)`**

    Creates a first-order lead/lag compensator:

    $$C(s)=\frac{k(\tau s + 1)}{\alpha \tau s + 1}$$

    * `tau` *(float)*: time constant
    * `alpha` *(float)*: pole/zero separation factor
      * **Lead** is typically `0 < alpha < 1` (pole farther left than zero)
      * **Lag** is typically `alpha > 1` (pole closer to origin than zero)
    * `k` *(float, optional)*: gain multiplier
    """)
    return


@app.cell
def _(lead_lag):
    C_lead = lead_lag(tau=0.02, alpha=0.1, k=2.0)
    C_lag  = lead_lag(tau=0.5, alpha=5.0, k=1.0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`second_order(b2, b1, b0, a1, a0)`**

    Creates a generic second-order transfer function:

    $$H(s)=\frac{b_2 s^2 + b_1 s + b_0}{s^2 + a_1 s + a_0}$$
    """)
    return


@app.cell
def _(second_order):
    H = second_order(b2=1, b1=0.2, b0=10, a1=0.5, a0=25)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`low_pass_filter(w_c, k=1.0)`**

    First-order low-pass filter:

    $$F(s)=\frac{k\,\omega_c}{s + \omega_c}$$

    * `w_c` *(float)*: cutoff frequency in rad/s
    * `k` *(float, optional)*: DC gain factor
    """)
    return


@app.cell
def _(low_pass_filter):
    _F = low_pass_filter(w_c=200, k=1.0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`notch_filter(w_n, zeta_z, zeta_p, k=1.0)`**

    Second-order notch filter (zeros and poles around the same natural frequency):

    $$N(s)=k\frac{s^2 + 2\zeta_z\omega_n s + \omega_n^2}{s^2 + 2\zeta_p\omega_n s + \omega_n^2}$$

    * `w_n` *(float)*: notch center frequency (rad/s)
    * `zeta_z` *(float)*: zero damping (controls notch depth/shape)
    * `zeta_p` *(float)*: pole damping (controls bandwidth/sharpness)
    * `k` *(float, optional)*: gain multiplier
    """)
    return


@app.cell
def _(notch_filter):
    N = notch_filter(w_n=120, zeta_z=0.01, zeta_p=0.2, k=1.0)
    return (N,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`combine(*args)`**

    Multiplies transfer functions in series.

    * `*args`: any number of `control.TransferFunction` objects
    """)
    return


@app.cell
def _(combine, lead_lag, low_pass_filter, notch_filter, pid):
    C_2 = combine(pid(2, 1, 0.02, n_f=200), lead_lag(0.03, 0.1), notch_filter(120, 0.02, 0.2), low_pass_filter(400))
    return (C_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`plot_frequency_response(*systems, **kwargs)`**

    Plots magnitude (dB) and phase (degrees) for one or more systems using Plotly.

    * `*systems`: one or more LTI systems compatible with `ct.frequency_response(...)` (`control.TransferFunction` or `control.StateSpace`)
    * `w_min` *(float, default=1e-2)*: minimum frequency (rad/s)
    * `w_max` *(float, default=1e3)*: maximum frequency (rad/s)
    * `n_points` *(int, default=1000)*: number of log-spaced frequency points
    * `title` *(str, default="Frequency Response")*: plot title
    * `legends` *(list[str] | None)*: legend labels; must match number of systems
    """)
    return


@app.cell
def _(C_2, N, plot_frequency_response):
    plot_frequency_response(C_2, N, C_2 * N, legends=['Controller', 'Filter', 'Combined'], w_min=0.1, w_max=100000.0, n_points=1500, title='Bode (Controller / Filter / Combined)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 7: Equivalent Stiffness Calculation

    For linear frequency-domain analyses (e.g., `run_modal`, `run_campbell`, `run_ucs`), ROSS cannot evaluate the discrete time-domain controller states directly. Instead, the `MagneticBearingElement` computes **frequency-dependent equivalent coefficients** that represent the closed-loop AMB behavior in the form of an equivalent stiffness and damping.

    With the updated implementation, the **displacement sensor gain** (`k_sense`, in V/m) and the **power amplifier gain** (`k_amp`, in V/A) are explicitly included in the loop gain used to build these equivalent coefficients.

    Internally, the element performs:

    1. Build (or retrieve) the continuous-time controller transfer function $C(s)$ (PID with derivative filter or a custom transfer function).
    2. Evaluate its frequency response $C(j\omega)$ over a frequency grid $\omega$ (rad/s).
    3. Split the response into real and imaginary parts:
       $
       C(j\omega)=\Re\{C(j\omega)\} + j \, \Im\{C(j\omega)\}
       $
    4. Map these parts into equivalent stiffness and damping using the electromagnetic constants:
       * $K_s$: negative electromagnetic stiffness (from force linearization)
       * $K_i$: current-to-force gain (from force linearization)

    ### Equivalent stiffness

    The equivalent stiffness includes the open-loop negative stiffness $K_s$ plus the real part of the controller contribution scaled by the sensor and amplifier gains:

    $$K_{eq}(\omega) = K_s + K_i , k_{amp}, k_{sense},\Re\{C(j\omega)\}$$

    ### Equivalent damping

    The equivalent damping is formed from the imaginary part of the controller contribution, scaled by the same gains and divided by $\omega$:

    $$
    C_{eq}(\omega) = \frac{K_i , k_{amp}, k_{sense}}{\omega},\Im\{C(j\omega\}
    $$

    ### Notes on implementation details

    * In the code, $C(j\omega)$ is obtained from `control.frequency_response()`, stored as `Hjw`, and then:

      * `C_real = Hjw.real`
      * `C_imag = Hjw.imag`
    * The arrays are computed as:
      $$
      k_{eq} = K_s + K_i,k_{amp},k_{sense},C_{real}
      \qquad
      c_{eq} = K_i,k_{amp},k_{sense},C_{imag},\frac{1}{\omega}
      $$
    * After that, the element transforms the isotropic equivalent coefficients ${k_{eq}, c_{eq}}$ into the rotor $x\text{–}y$ coordinates using the rotation defined by `sensors_axis_rotation`, producing $k_{xx}, k_{xy}, k_{yx}, k_{yy}$ and $c_{xx}, c_{xy}, c_{yx}, c_{yy}$.

    These frequency-dependent arrays are stored in the element. During calls like `run_modal` (at a given speed), ROSS interpolates the coefficients at the required excitation frequencies to assemble the global stiffness and damping matrices for the rotor model.
    """)
    return


if __name__ == "__main__":
    app.run()
