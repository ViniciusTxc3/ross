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
    Example 12 - Example of impact phenomena in rotor-casing dynamical systems.
    =====

    In this example, we use the rotor seen in Example 10 for demonstrating the results obtained when we have vibrations due to contact between a rotor and a casing or stator for example.
    """)
    return


app._unparsable_cell(
    r"""
    import numpy as np

    import ross as rs
    from ross.faults import *
    from ross.units import Q_
    from ross.probe import Probe

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    """,
    name="_"
)


@app.cell
def _(np, rs):
    """Create example rotor with given number of elements."""
    steel2 = rs.Material(name="Steel", rho=7850, E=2.17e11, Poisson=0.2992610837438423)
    #  Rotor with 6 DoFs, with internal damping, with 10 shaft elements, 2 disks and 2 bearings.
    i_d = 0
    o_d = 0.019
    n = 33

    # fmt: off
    L = np.array(
            [0  ,  25,  64, 104, 124, 143, 175, 207, 239, 271,
             303, 335, 345, 355, 380, 408, 436, 466, 496, 526,
             556, 586, 614, 647, 657, 667, 702, 737, 772, 807,
             842, 862, 881, 914]
             )/ 1000
    # fmt: on

    L = [L[i] - L[i - 1] for i in range(1, len(L))]

    shaft_elem = [
        rs.ShaftElement(
            material=steel2,
            L=l,
            idl=i_d,
            odl=o_d,
            idr=i_d,
            odr=o_d,
            alpha=8.0501,
            beta=1.0e-5,
            rotary_inertia=True,
            shear_effects=True,
        )
        for l in L
    ]

    Id = 0.003844540885417
    Ip = 0.007513248437500

    disk0 = rs.DiskElement(n=12, m=2.6375, Id=Id, Ip=Ip)
    disk1 = rs.DiskElement(n=24, m=2.6375, Id=Id, Ip=Ip)

    kxx1 = 4.40e5
    kyy1 = 4.6114e5
    kzz = 0
    cxx1 = 27.4
    cyy1 = 2.505
    czz = 0
    kxx2 = 9.50e5
    kyy2 = 1.09e8
    cxx2 = 50.4
    cyy2 = 100.4553

    bearing0 = rs.BearingElement(
        n=4, kxx=kxx1, kyy=kyy1, cxx=cxx1, cyy=cyy1, kzz=kzz, czz=czz
    )
    bearing1 = rs.BearingElement(
        n=31, kxx=kxx2, kyy=kyy2, cxx=cxx2, cyy=cyy2, kzz=kzz, czz=czz
    )

    rotor = rs.Rotor(shaft_elem, [disk0, disk1], [bearing0, bearing1])
    return (rotor,)


@app.cell
def _(Probe, np):
    """Inserting a mass and phase unbalance and defining the local response."""
    mass_unb = [2e-4, 0]
    phase_unb = [-np.pi / 2, 0]
    node_unb = [12, 24]
    probe1 = Probe(14, 0)
    probe2 = Probe(22, 0)
    return mass_unb, node_unb, phase_unb, probe1, probe2


@app.cell
def _(Q_, mass_unb, node_unb, np, phase_unb, rotor):
    """Calculate the response when a rotor makes contact with a casing or stator."""
    results = rotor.run_rubbing(
        distance=7.95e-5,
        contact_stiffness=1.1e6,
        contact_damping=40,
        friction_coeff=0.3,
        n=12,
        speed=Q_(1200, "RPM"),
        node=node_unb,
        unbalance_magnitude=mass_unb,
        unbalance_phase=phase_unb,
        t=np.arange(0, 5, 0.0001),
        model_reduction={"num_modes": 12},  # Pseudo-modal method, optional
    )
    return (results,)


@app.cell
def _(probe1, probe2, results):
    """Plots the time response for the two given probes."""
    results.plot_1d([probe1, probe2]).show()
    return


@app.cell
def _(Q_, probe1, probe2, results):
    """Plots the frequency response for the two given probes."""
    results.plot_dfft(
        [probe1, probe2], frequency_range=Q_((0, 100), "Hz"), yaxis_type="log"
    ).show()
    return


if __name__ == "__main__":
    app.run()
