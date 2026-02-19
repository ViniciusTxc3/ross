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
    ## Example 26 - Isotropic System

    This example is based on Example 6.3.1.a page 253 from {cite}`friswell2010dynamics`.

    The rotor system shown in Figure 6.18 consists of a shaft 1.5 m long with a 50 mm diameter supported by bearings at each end. Disks are mounted on the shaft at one-third and two-third spans. Each disk is 70 mm thick and the left and right disks are 280 and 350 mm in diameter, respectively. The shaft and disks have material properties E — 211 GPa, G = 81.1 GPa, and p — 7,810 kg/m3. Determine the response of the system at the disks due to an out-of-balance on the left disk of 0.001 kgm, if each bearing has a stiffness of 1 MN/m and a damping of 100 Ns/m in both the x and y directions. The natural frequencies and mode shapes for this rotor system are calculated.
    """)
    return


@app.cell
def _():
    import ross as rs
    import plotly.graph_objects as go
    import plotly.io as pio
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    pio.renderers.default = 'notebook'
    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    Q_ = rs.Q_
    return Q_, ScalarFormatter, go, np, plt, rs


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.1e9, rho=7810)
    return (steel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Defining bearings, shaft and disk elements and Creating isotropic rotor
    """)
    return


@app.cell
def _(rs, steel):
    N = 6
    L = 1.5 / N
    idl = 0
    odl = 0.05  # shaft diameter
    shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for _i in range(N)]
    bearings = [rs.BearingElement(n=0, kxx=1000000.0, kyy=1000000.0, cxx=100, cyy=100), rs.BearingElement(n=6, kxx=1000000.0, kyy=1000000.0, cxx=100, cyy=100)]
    disks = [rs.DiskElement.from_geometry(n=N / 3, material=steel, width=0.07, i_d=odl, o_d=0.28, scale_factor='mass'), rs.DiskElement.from_geometry(n=2 * N / 3, material=steel, width=0.07, i_d=odl, o_d=0.35, scale_factor='mass')]
    rotor = rs.Rotor(shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings)
    rotor.plot_rotor(width=750, height=500)
    return (rotor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Campbell Diagram
    """)
    return


@app.cell
def _(Q_, np, rotor):
    campbell = rotor.run_campbell(
        speed_range=Q_(np.linspace(0, 6500, 65), "RPM"), frequencies=7
    )
    return (campbell,)


@app.cell
def _(campbell):
    fig = campbell.plot(frequency_units='RPM', width=600, height=600)
    for _i in fig.data:
        try:
            _i['y'] = _i['y'] / 60
        except:
            pass
    fig.update_yaxes(title='Natural Frequencies (Hz)', range=[0, 150])
    fig.update_xaxes(title='Rotor Spin Speed (rpm)', range=[0, 6500])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Mode Shapes and Damped Natural Frequencies
    """)
    return


@app.cell
def _(Q_, rotor):
    _speed = Q_(3000, 'RPM')
    modal = rotor.run_modal(_speed, num_modes=14)
    for _i in range(7):
        modal.plot_mode_3d(mode=_i, frequency_units='Hz', damping_parameter='damping_ratio').show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating the out-of-balancing
    """)
    return


@app.cell
def _(Q_, np, rotor):
    n1 = 2  # out-of-balancing is positioned at the left disk
    m1 = 0.001  # amount of out-of-balancing expressed in kg*m
    p1 = 0  # ou-of-balancing mass phase position
    _speed = Q_(np.linspace(0, 4500, 2451), 'RPM')
    results_case1 = rotor.run_unbalance_response([n1], [m1], [p1], _speed)
    return m1, results_case1


@app.cell
def _(Q_, results_case1):
    _probe1 = (2, 0)
    _probe2 = (2, Q_(90, 'deg'))
    fig_1 = results_case1.plot(probe=[_probe1, _probe2], probe_units='degrees', frequency_units='RPM', amplitude_units='µm pkpk', phase_units='degrees')
    fig_1.update_layout(yaxis=dict(type='log'))
    return


@app.cell
def _(Q_, results_case1):
    _probe1 = (4, 0)
    _probe2 = (4, Q_(90, 'deg'))
    fig_2 = results_case1.plot(probe=[_probe1, _probe2], probe_units='degrees', frequency_units='RPM', amplitude_units='µm pkpk', phase_units='degrees')
    return (fig_2,)


@app.cell
def _(fig_2):
    # changing to log scale
    fig_2.update_layout(yaxis=dict(type='log'))  # title='Amplitude (µm pkpk)',  # range=[-9, -1]  # log range: 10^-9, 10^-1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Orbit using the Plotly library
    """)
    return


@app.cell
def _():
    #### Building the orbit at 496 RPM, 1346 RPM and 2596 RPM for nodes located at
    #### the right and left disks (node=2 and node=4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### At 496 RPM
    """)
    return


@app.cell
def _(m1, np, rotor):
    _speed = 496 * (2 * np.pi / 60)  # Q_(496, "RPM")
    time_samples = 1000001
    _node = 2  # out-of-balancing position
    _t = np.linspace(0, 43, time_samples)
    _F = np.zeros((time_samples, rotor.ndof))
    # Creating the out-of-balancing force input matrix
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    # harmonic force component on x axis
    # harmonic force component on y axis
    # Using the ROSS’ method to calculate displacements due a force in time domain: run_time_response().
    response3 = rotor.run_time_response(_speed, _F, _t)  # as out-of-balancing is a harmonic force
    return (response3,)


@app.cell
def _(go, np, response3):
    # Editing the ross plots in order to explicit the orbit whirl in node 2
    _orb2 = response3.plot_2d(node=2, width=500, height=500)
    _cutoff = int(1000 * 2.7)
    _x_new2 = _orb2.data[0].x[-_cutoff:]
    _y_new2 = _orb2.data[0].y[-_cutoff:]
    _starting_point2 = go.Scatter(x=[_x_new2[0]], y=[_y_new2[0]], marker={'size': 10, 'color': 'orange'}, showlegend=False, name='Starting Point2')
    _orb2_curve = go.Scatter(x=_x_new2, y=_y_new2, mode='lines', name='orb2', showlegend=False, line=dict(color='orange'))
    # Inserting the orbit starting point
    _orb4 = response3.plot_2d(node=4, width=500, height=500)
    _x_new4 = _orb4.data[0].x[-_cutoff:]
    _y_new4 = _orb4.data[0].y[-_cutoff:]
    _starting_point4 = go.Scatter(x=[_x_new4[0]], y=[_y_new4[0]], marker={'size': 10, 'color': '#636EFA'}, showlegend=False, name='Starting Point4')
    _max_amp = max(np.max(_x_new2), np.max(_y_new2), np.max(_x_new4), np.max(_y_new4))
    _orb4.update_xaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_yaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_traces(x=_x_new4, y=_y_new4, name='orb4')
    # Inserting the orbit of node 2
    _orb4.update_layout(title='Response at node 2 and 4 at 496 RPM')
    _orb4.add_trace(_starting_point4)
    _orb4.add_trace(_starting_point2)
    _orb4.add_trace(_orb2_curve)
    # Editing the ross plots in order to explicit the orbit whirl in node 4
    # Proper scaling x and y axis
    # Merging orbit at node 2 and node 4
    _orb4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### At 1346 RPM
    """)
    return


@app.cell
def _(m1, np, rotor):
    _speed = 1346 * (2 * np.pi / 60)
    time_samples_1 = 1000001
    _node = 2
    _t = np.linspace(0, 43, time_samples_1)
    _F = np.zeros((time_samples_1, rotor.ndof))
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    response3_1 = rotor.run_time_response(_speed, _F, _t)
    return (response3_1,)


@app.cell
def _(go, np, response3_1):
    _orb2 = response3_1.plot_2d(node=2, width=500, height=500)
    _cutoff = int(1000 * 1)
    _x_new2 = _orb2.data[0].x[-_cutoff:]
    _y_new2 = _orb2.data[0].y[-_cutoff:]
    _starting_point2 = go.Scatter(x=[_x_new2[0]], y=[_y_new2[0]], marker={'size': 10, 'color': 'orange'}, showlegend=False, name='Starting Point2')
    _orb2_curve = go.Scatter(x=_x_new2, y=_y_new2, mode='lines', name='orb2', showlegend=False, line=dict(color='orange'))
    _orb4 = response3_1.plot_2d(node=4, width=500, height=500)
    _x_new4 = _orb4.data[0].x[-_cutoff:]
    _y_new4 = _orb4.data[0].y[-_cutoff:]
    _starting_point4 = go.Scatter(x=[_x_new4[0]], y=[_y_new4[0]], marker={'size': 10, 'color': '#636EFA'}, showlegend=False, name='Starting Point4')
    _max_amp = max(np.max(_x_new2), np.max(_y_new2), np.max(_x_new4), np.max(_y_new4))
    _orb4.update_xaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_yaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_traces(x=_x_new4, y=_y_new4, name='orb4')
    _orb4.update_layout(title='Response at node 2 and 4 at 1346 RPM')
    _orb4.add_trace(_starting_point4)
    _orb4.add_trace(_starting_point2)
    _orb4.add_trace(_orb2_curve)
    _orb4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### At 2596 RPM
    """)
    return


@app.cell
def _(m1, np, rotor):
    _speed = 2596 * (2 * np.pi / 60)
    time_samples_2 = 1000001
    _node = 2
    _t = np.linspace(0, 43, time_samples_2)
    _F = np.zeros((time_samples_2, rotor.ndof))
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    response3_2 = rotor.run_time_response(_speed, _F, _t)
    return (response3_2,)


@app.cell
def _(go, np, response3_2):
    _orb2 = response3_2.plot_2d(node=2, width=500, height=500)
    _cutoff = int(1000 * 0.52)
    _x_new2 = _orb2.data[0].x[-_cutoff:]
    _y_new2 = _orb2.data[0].y[-_cutoff:]
    _starting_point2 = go.Scatter(x=[_x_new2[0]], y=[_y_new2[0]], marker={'size': 10, 'color': 'orange'}, showlegend=False, name='Starting Point2')
    _orb2_curve = go.Scatter(x=_x_new2, y=_y_new2, mode='lines', name='orb2', showlegend=False, line=dict(color='orange'))
    _orb4 = response3_2.plot_2d(node=4, width=500, height=500)
    _x_new4 = _orb4.data[0].x[-_cutoff:]
    _y_new4 = _orb4.data[0].y[-_cutoff:]
    _starting_point4 = go.Scatter(x=[_x_new4[0]], y=[_y_new4[0]], marker={'size': 10, 'color': '#636EFA'}, showlegend=False, name='Starting Point4')
    _max_amp = max(np.max(_x_new2), np.max(_y_new2), np.max(_x_new4), np.max(_y_new4))
    _orb4.update_xaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_yaxes(range=[-1.2 * _max_amp, 1.2 * _max_amp])
    _orb4.update_traces(x=_x_new4, y=_y_new4, name='orb4')
    _orb4.update_layout(title='Response at node 2 and 4 at 2596 RPM')
    _orb4.add_trace(_starting_point4)
    _orb4.add_trace(_starting_point2)
    _orb4.add_trace(_orb2_curve)
    _orb4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Orbit using the Matplotlib library
    """)
    return


@app.cell
def _(m1, np, rotor):
    _speed = 496 * (2 * np.pi / 60)
    time_samples_3 = 1000001
    _node = 2
    _t = np.linspace(0, 43, time_samples_3)
    _F = np.zeros((time_samples_3, rotor.ndof))
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    response3_3 = rotor.run_time_response(_speed, _F, _t)
    node_response = 2
    x1_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y1_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    t_vector = response3_3.t
    node_response = 4
    x2_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y2_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    _speed = 1346 * (2 * np.pi / 60)
    time_samples_3 = 1000001
    _node = 2
    _t = np.linspace(0, 43, time_samples_3)
    _F = np.zeros((time_samples_3, rotor.ndof))
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    response3_3 = rotor.run_time_response(_speed, _F, _t)
    node_response = 2
    x3_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y3_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    node_response = 4
    x4_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y4_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    _speed = 2596 * (2 * np.pi / 60)
    time_samples_3 = 1000001
    _node = 2
    _t = np.linspace(0, 43, time_samples_3)
    _F = np.zeros((time_samples_3, rotor.ndof))
    _F[:, rotor.number_dof * _node + 0] = m1 * _speed ** 2 * np.cos(_speed * _t)
    _F[:, rotor.number_dof * _node + 1] = m1 * _speed ** 2 * np.sin(_speed * _t)
    response3_3 = rotor.run_time_response(_speed, _F, _t)
    node_response = 2
    x5_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y5_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    node_response = 4
    x6_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 0]
    y6_axis_displacement = response3_3.yout[:, rotor.number_dof * node_response + 1]
    return (
        time_samples_3,
        x1_axis_displacement,
        x2_axis_displacement,
        x3_axis_displacement,
        x4_axis_displacement,
        x5_axis_displacement,
        x6_axis_displacement,
        y1_axis_displacement,
        y2_axis_displacement,
        y3_axis_displacement,
        y4_axis_displacement,
        y5_axis_displacement,
        y6_axis_displacement,
    )


@app.cell
def _(
    ScalarFormatter,
    plt,
    time_samples_3,
    x1_axis_displacement,
    x2_axis_displacement,
    x3_axis_displacement,
    x4_axis_displacement,
    x5_axis_displacement,
    x6_axis_displacement,
    y1_axis_displacement,
    y2_axis_displacement,
    y3_axis_displacement,
    y4_axis_displacement,
    y5_axis_displacement,
    y6_axis_displacement,
):
    (fig_3, (ax1, ax2, ax3)) = plt.subplots(1, 3, figsize=(13, 4))
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-6, -6))
    _cutoff = -int(time_samples_3 * 0.0027)
    ax1.plot(x1_axis_displacement[_cutoff:], y1_axis_displacement[_cutoff:], label='Orbit')
    ax1.plot(x1_axis_displacement[_cutoff:][0], y1_axis_displacement[_cutoff:][0], 'o', markersize=6, color='#636EFA')
    ax1.plot(x2_axis_displacement[_cutoff:], y2_axis_displacement[_cutoff:], label='Orbit')
    ax1.plot(x2_axis_displacement[_cutoff:][0], y2_axis_displacement[_cutoff:][0], 'o', markersize=6, color='#636EFA')
    ax1.set_title('496 RPM')
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)
    _cutoff = -int(time_samples_3 * 0.001)
    ax2.plot(x3_axis_displacement[_cutoff:], y3_axis_displacement[_cutoff:], label='Orbit')
    ax2.plot(x3_axis_displacement[_cutoff:][0], y3_axis_displacement[_cutoff:][0], 'o', markersize=10, color='#636EFA')
    ax2.plot(x4_axis_displacement[_cutoff:], y4_axis_displacement[_cutoff:], label='Orbit')
    ax2.plot(x4_axis_displacement[_cutoff:][0], y4_axis_displacement[_cutoff:][0], 'o', markersize=10, color='#636EFA')
    ax2.set_title('1346 RPM')
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)
    _cutoff = -int(time_samples_3 * 0.00052)
    ax3.plot(x5_axis_displacement[_cutoff:], y5_axis_displacement[_cutoff:], label='Orbit')
    ax3.plot(x5_axis_displacement[_cutoff:][0], y5_axis_displacement[_cutoff:][0], 'o', markersize=10, color='#636EFA')
    ax3.plot(x6_axis_displacement[_cutoff:], y6_axis_displacement[_cutoff:], label='Orbit')
    ax3.plot(x6_axis_displacement[_cutoff:][0], y6_axis_displacement[_cutoff:][0], 'o', markersize=10, color='#636EFA')
    ax3.set_title('2596 RPM')
    ax3.xaxis.set_major_formatter(formatter)
    ax3.yaxis.set_major_formatter(formatter)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### REFERENCES
    [1] M. I. Friswell, J. E. T. Penny, S. D. Garvey, and A. W. Lees, Dynamics of Rotating Machines. Cambridge: Cambridge University Press, 2010.
    """)
    return


if __name__ == "__main__":
    app.run()
