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
    # Example 32 - Response to Forces Applied through Auxiliary Bearings
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This example is based on Example 6.3.3 page 264 from {cite}`friswell2010dynamics`.

    The rotor-bearing system described in Example 6.3.1 (and shown in Figure 6.18 - Page 253) rotates at 3,000 rev/min. Each bearing has a stiffness of 1 MN/m and a damping of 100 Ns/m in both the x and y directions. For test purposes, the rotor is excited via an auxiliary bearing that is attached to the rotor at midspan. Determine the response of the disk at node 3  to forces acting on an auxiliary bearing. The system is modeled using six elements, giving 28 degrees of freedom. The forces at the auxiliary bearing are (a) a rotating out-of-balance of 0.0001 kg.m, and (b) a harmonic force of 10 N.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    from ross import Probe
    from ross.units import Q_

    import plotly.graph_objects as go

    return Probe, Q_, go, np, rs


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.1e9, rho=7810)
    return (steel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating Rotor
    """)
    return


@app.cell
def _(rs, steel):
    # Shaft parameters
    shaft_length = 1.5  # meters
    shaft_diameter = 0.05  # meters
    n_elements = 6
    L_elem = shaft_length / n_elements

    shaft_elements = [
        rs.ShaftElement(
            L=L_elem,
            idl=0.0,
            odl=shaft_diameter,
            material=steel,
            shear_effects=True,
            rotary_inertia=True,
            gyroscopic=True,
        )
        for _ in range(n_elements)
    ]

    # Disk parameters
    disk1 = rs.DiskElement.from_geometry(
        n=2,
        material=steel,
        width=0.070,
        i_d=shaft_diameter,
        o_d=0.280,
    )
    disk2 = rs.DiskElement.from_geometry(
        n=4,
        material=steel,
        width=0.070,
        i_d=shaft_diameter,
        o_d=0.350,
    )


    # Bearings at ends (nodes 0 and 6)
    kxx = 1e6  # N/m
    cxx = 100  # Ns/m
    bearing1 = rs.BearingElement(
        n=0,
        kxx=kxx,
        kyy=kxx,
        cxx=cxx,
    )
    bearing2 = rs.BearingElement(
        n=6,
        kxx=kxx,
        kyy=kxx,
        cxx=cxx,
    )

    # Assemble rotor
    rotor = rs.Rotor(
        shaft_elements=shaft_elements,
        disk_elements=[disk1, disk2],
        bearing_elements=[bearing1, bearing2],
    )
    rotor.plot_rotor()
    return (rotor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Response for a rotating out-of-balance
    """)
    return


@app.cell
def _(Probe, Q_, np, rotor):
    # Unbalance excitation at midspan (node 3)
    unbalance_response = rotor.run_unbalance_response(
        node=3,
        unbalance_magnitude=0.0001,
        unbalance_phase=0,
        frequency=Q_(np.linspace(0, 4000, 1000), "RPM"),
    )

    fig2 = unbalance_response.plot_magnitude(
        probe=[Probe(2, Q_(90, "deg"))], yaxis=dict(type="log"), frequency_units="RPM"
    )
    fig2.update_layout(yaxis_range=[-8, -2])
    fig2.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Response due to vertical a harmonic excitation at the auxiliary bearing
    """)
    return


@app.cell
def _(Q_, go, np, rotor):
    F0 = 10
    node = 3
    probe = 2

    speed_range = Q_([100, 500, 1000, 2000, 3000], "RPM")
    frequency_range = Q_(np.linspace(0, 65, 1000), "Hz").to_base_units().m
    t = np.arange(0, 10, 0.001)

    num_dof = rotor.number_dof

    fig = go.Figure()

    for speed in speed_range:
        probe_resp = []

        for w in frequency_range:
            # Create vertical harmonic force
            F = np.zeros((len(t), rotor.ndof))

            dofy = num_dof * node + 1
            F[:, dofy] += F0 * np.sin(w * t)

            # Run time response
            time_resp = rotor.run_time_response(speed, F, t)

            # Extract response for the probe
            response = time_resp.yout

            init_step = int(2 * len(t) / 3)

            dofx = num_dof * probe
            dofy = num_dof * probe + 1

            x = response[init_step:, dofx] * 0
            y = response[init_step:, dofy]

            lateral_max = max(max(abs(x)), max(abs(y)))
            probe_resp.append(lateral_max)

        # Adding the response to figure
        fig.add_trace(
            go.Scatter(
                x=Q_(frequency_range, "rad/s").to("Hz").m,
                y=np.array(probe_resp),
                mode="lines",
                name=f"{speed.to('RPM').m} RPM",
                line=dict(width=2),
            )
        )
    return (fig,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting response
    """)
    return


@app.cell
def _(fig):
    fig.update_layout(
        xaxis=dict(title="Frequency (Hz)"),
        yaxis=dict(
            title="Amplitude (m)",
            type="log",
            range=[-8, -2],
            exponentformat="power",
        ),
        legend=dict(
            title=dict(text="Rotor Speed"),
        ),
    )

    fig.show()
    return


if __name__ == "__main__":
    app.run()
