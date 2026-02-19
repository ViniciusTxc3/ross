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
    # Example 28 - Rigid rotor on isotropic bearings
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This example is based on Example 6.2.1 page 239 from {cite}`friswell2010dynamics`.

    A uniform rigid rotor is shown in figure 3.8. The rotor has length of 0.5 m and a diameter of 0.2 m, and it is made from steel with a density of 7810 kg/m³. The rotor is supported at the ends by bearings. The horizontal and vertical stiffness are 1 MN/m at bearing 1 and 1.3 MN/m at bearing 2. The damping values in the horizontal and vertical supports are 10 Ns/m at bearing 1 and 13 Ns/m at bearing 2. This rotor is the same as that described in Example 3.5.3(b). Find the response to a mass eccentricity of 0.1 mm and plot the Campbell diagram.
    """)
    return


@app.cell
def _():
    import ross as rs
    import plotly.graph_objects as go
    import plotly.io as pio
    import numpy as np

    Q_ = rs.Q_
    pio.renderers.default = "notebook"
    return Q_, np, rs


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.2e9, rho=7810)
    return (steel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating rotor
    """)
    return


@app.cell
def _(rs, steel):
    N = 6
    L = 0.5 / N
    idl = 0
    odl = 0.2

    shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for i in range(N)]
    bearings = [
        rs.BearingElement(n=0, kxx=1e6, kyy=1.5e6, cxx=20, cyy=30),
        rs.BearingElement(n=6, kxx=1.3e6, kyy=1.8e6, cxx=26, cyy=36),
    ]
    disks = []

    rotor = rs.Rotor(shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings)
    rotor.plot_rotor()
    return odl, rotor


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Campbell Diagram
    """)
    return


@app.cell
def _(Q_, np, rotor):
    fig = rotor.run_campbell(speed_range=Q_(list(range(0, 3500, 50)), "RPM"), frequencies=4)
    fig.plot().show()
    print(
        "Wn [Hz] at 0 rpm =",
        np.round((rotor.run_modal(speed=0 * np.pi / 30, num_modes=8).wn) / (2 * np.pi), 2),
    )
    return


@app.cell
def _(rotor):
    # Calculating equivalent unbalance mass
    e = 0.1e-3
    shaft_radius = 0.1
    m_unb = (rotor.m * e) / shaft_radius

    print(f"Rotor mass = {round(rotor.m, 2)} kg")
    print(f"Unbalance mass = {round(m_unb, 2)} kg")
    return (m_unb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bode Plot
    """)
    return


@app.cell
def _(Q_, m_unb, np, odl, rotor):
    n1 = 3  # position of the unbalance mass in the center of the rotor
    m1 = m_unb * (odl / 2)
    p1 = 0  # unbalance mass phase
    _speed = Q_(np.linspace(0, 3500, 60), 'RPM')
    results_case1 = rotor.run_unbalance_response([n1], [m1], [p1], _speed)
    return (results_case1,)


@app.cell
def _(results_case1):
    probe1 = (3, 0)
    results_case1.plot(
        probe=[probe1],
        probe_units="degrees",
        frequency_units="RPM",
        amplitude_units="µm pkpk",
        phase_units="degrees",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Mode Shapes
    """)
    return


@app.cell
def _(np, rotor):
    _speed = 3500 * np.pi / 30
    modal = rotor.run_modal(_speed)
    for i in np.arange(0, 3.1, 1):
        modal.plot_mode_3d(mode=int(i), frequency_units='RPM').show()
    return (modal,)


@app.cell
def _(display, modal):
    for mode in range(4):
        display(modal.plot_orbit(mode, nodes=[0, 3, 6]))
    return


if __name__ == "__main__":
    app.run()
