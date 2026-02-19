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
    Tutorial - MultiRotor System
    ======================
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a basic tutorial on how to use the `MultiRotor` class for rotordynamics analysis. Before starting this tutorial, be sure you're already familiar with ROSS library. What changes here is basically the part of building the model, since running the analyses will be practically the same as seen in the other tutorials.

    When two shafts are joined together by gears, coupling can occur between the lateral and torsional vibration. This interaction is modeled in ROSS based on {cite}`rao1998theoretical`. In this work, a typical spur gear pair is modeled as a pair of rigid disks connected by a spring and a damping, considering the pressure angle ($\alpha$) and the oritentation angle ($\varphi$) as shown in the following:

    <div style="text-align: center;">
        <img src="../_static/img/img_tutorial4_gearmesh.png" alt="Gear mesh" style="width: 450px; height: auto;">
        <br>
        <small>Figure 1: Global coordinate system of a spur gear pair (Yang et al., 2016).</small>
    </div>

    As you can see, an element not yet shown is needed to model the multi-rotor system, the `GearElement`. This new element resembles the `DiskElement` with added attributes, which will be shown next.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 1: GearElement Class

    The class `GearElement` allows you to create gear elements. It is a subclass of `DiskElement` that requires information related to its pitch diameter and pressure angle.

    ROSS offers 2 (two) ways to create a gear element:
    1. Inputing mass and inertia data
    2. Inputing geometrical and material data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1 Creating a single gear element

    In this tutorial, only an example of how to create a single element will be shown. However, the same procedures presented for the `DiskElement` in the first part of the <b>Tutorial</b> can be replicated here. The `GearElement` goes into the same list of disk elements when assembling the rotor.

    This example below shows how to instantiate a gear element according to the mass and inertia properties:
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import pandas as pd

    from ross.units import Q_

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio
    import plotly.graph_objects as go

    pio.renderers.default = "notebook"
    return Q_, np, pd, rs


@app.cell
def _(Q_, rs):
    gear = rs.GearElement(
        n=0,
        m=5,
        Id=0.002,
        Ip=0.004,
        n_teeth=20,
        pitch_diameter=0.5,
        pr_angle=Q_(22.5, "deg"),
        tag="Gear",
    )
    gear
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 2: MultiRotor Class

    `MultiRotor` is a subclass of `Rotor` class. It takes two rotors (driving and driven) as arguments and couple them with their gears. The object created has several methods that can be used to evaluate the dynamics of the model (they all start with the prefix `.run_`).

    To use this class, you must input the already instantiated rotors and each one need at least one gear element.

    The shaft elements are renumbered starting with the elements of the driving rotor.

    To assemble the matrices, the driving and driven matrices are joined.
    For the stiffness matrix, the coupling is considered at the nodes of the gears in contact.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1 Creating a spur geared two-shaft rotor system
    Let's create a simple model with two rotors connected by a pair of spur gears and supported by flexible bearings, as shown in Fig. 2. For more details on the description of the model, see the work of {cite}`rao1998theoretical`.

    <div style="text-align: center;">
        <img src="../_static/img/img_tutorial4_multirotor.png" alt="MultiRotor" style="width: 450px; height: auto;">
        <br>
        <small>Figure 2: Rotors connected by a pair of spur gears (Friswell et al., 2010).</small>
    </div>

    In Figure 2, the first node is 1 (one), but we must remember that in ROSS the node count starts at 0 (zero).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.1 Creating material
    """)
    return


@app.cell
def _(rs):
    # Creating material
    material = rs.Material(name="mat_steel", rho=7800, E=207e9, G_s=79.5e9)
    return (material,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.2 Creating the driving rotor
    """)
    return


@app.cell
def _(Q_, material, rs):
    # Rotor 1
    _L1 = [0.1, 4.24, 1.16, 0.3]
    d1 = [0.3, 0.3, 0.22, 0.22]
    _shaft1 = [rs.ShaftElement(L=_L1[i], idl=0.0, odl=d1[i], material=material, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(len(_L1))]
    generator = rs.DiskElement(n=1, m=525.7, Id=16.1, Ip=32.2)
    disk = rs.DiskElement(n=2, m=116.04, Id=3.115, Ip=6.23)
    gear1 = rs.GearElement(n=4, m=726.4, Id=56.95, Ip=113.9, n_teeth=328, base_diameter=0.5086 * 2, pr_angle=Q_(22.5, 'deg'), helix_angle=0)
    bearing1 = rs.BearingElement(n=0, kxx=183900000.0, kyy=200400000.0, cxx=3000.0)
    bearing2 = rs.BearingElement(n=3, kxx=183900000.0, kyy=200400000.0, cxx=3000.0)
    rotor1 = rs.Rotor(_shaft1, [generator, disk, gear1], [bearing1, bearing2])
    rotor1.plot_rotor()
    return (rotor1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.3 Creating the driven rotor
    """)
    return


@app.cell
def _(material, np, rs):
    # Rotor 2
    _L2 = [0.3, 5, 0.1]
    d2 = [0.15, 0.15, 0.15]
    _shaft2 = [rs.ShaftElement(L=_L2[i], idl=0.0, odl=d2[i], material=material, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(len(_L2))]
    base_radius = 0.03567
    _pressure_angle = rs.Q_(22.5, 'deg').to_base_units().m
    pitch_diameter = 2 * base_radius / np.cos(_pressure_angle)
    gear2 = rs.GearElement(n=0, m=5, Id=0.002, Ip=0.004, n_teeth=23, pitch_diameter=pitch_diameter, pr_angle=_pressure_angle, helix_angle=0)
    turbine = rs.DiskElement(n=2, m=7.45, Id=0.0745, Ip=0.149)
    bearing3 = rs.BearingElement(n=1, kxx=10100000.0, kyy=41600000.0, cxx=3000.0)
    bearing4 = rs.BearingElement(n=3, kxx=10100000.0, kyy=41600000.0, cxx=3000.0)
    rotor2 = rs.Rotor(_shaft2, [gear2, turbine], [bearing3, bearing4])
    rotor2.plot_rotor()
    return (rotor2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.4 Connecting rotors

    To build the multi-rotor model, we need to inform, in the following order:
    - the driving rotor,
    - the driven rotor,
    - the tuple with the pair of coupled nodes (first number corresponds to the gear node of the driving rotor, and the second of the driven rotor),
    - the gear ratio, and
    - the gear mesh stiffness.

    Finally, we can inform:
    - the orientation angle (if not defined, zero is adopted as the default),
    - the position of the driven rotor in relation to the driving rotor only for visualization in the plot ("above" or "below"), and
    - a tag.
    """)
    return


@app.cell
def _(rotor1, rotor2, rs):
    # Creating multi-rotor
    multirotor = rs.MultiRotor(
        rotor1,
        rotor2,
        coupled_nodes=(4, 0),
        gear_mesh_stiffness=1e8,
        orientation_angle=0,
        position="below",
    )

    multirotor.plot_rotor()
    return (multirotor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Running analyses
    We will run some analyses for the multi-rotor in this section and even compare results from the literature.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.2.1 Modal analysis

    Let's start with the modal analysis to obtain the natural frequencies for the coupled rotor when the generator runs at
    1500 RPM. Then we will compare the results with {cite}`friswell2010dynamics`.

    It is worth noting that in the analyses, we must always inform the respective speed of the driving rotor and not the driven one.
    """)
    return


@app.cell
def _(Q_, multirotor, np, pd):
    # Friswell et al. (2010) results for natural frequencies:
    Friswell_results = np.array(
        [
            11.641,
            12.284,
            17.268,
            18.458,
            23.956,
            37.681,
            49.889,
            50.861,
            56.248,
            57.752,
            59.188,
            63.113,
            74.203,
        ]
    )

    speed = Q_(1500, "RPM")
    frequencies = 13

    modal = multirotor.run_modal(speed, num_modes=frequencies * 2)
    wd = np.round(Q_(modal.wd, "rad/s").to("Hz").m, 5)

    print("Natural frequencies (Hz)")
    pd.DataFrame(
        {
            "Friswell et al.": Friswell_results,
            "ROSS": wd,
            "Error (%)": np.abs(wd - Friswell_results) / Friswell_results * 100,
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.2.2 Campbell diagram

    To obtain the Campbell diagram we can proceed in the same way as seen for a single rotor. Remember that the reference speeds / frequencies are in relation to the driving rotor.

    In the Campbell diagram below, the dashed lines show the shaft rotation speeds corresponding to the generator (blue, node 1) and turbine (yellow, node 7).
    """)
    return


@app.cell
def _(Q_, multirotor, np):
    frequency_range = Q_(np.arange(0, 5000, 100), "RPM")

    gear_ratio = multirotor.mesh.gear_ratio

    campbell = multirotor.run_campbell(frequency_range, frequencies=13)
    campbell.plot(frequency_units="Hz", harmonics=[1, round(gear_ratio, 3)]).show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.2.3 Time response

    Using the `run_time_response` function we can obtain the system response due to an unbalance at nodes 2 and 7. The same setup presented in the work of {cite}`yang2016general` was applied here for comparison purposes.
    """)
    return


@app.cell
def _(Q_, multirotor, np):
    nodes = [2, 7]
    unb_mag = [35.505e-3, 0.449e-3]
    unb_phase = [0, 0]

    dt = 1e-4
    t = np.arange(0, 1200, dt)
    speed1 = Q_(5000, "RPM").to_base_units().m  # Generator rotor speed

    # Unbalance force
    F = multirotor.unbalance_force_over_time(nodes, unb_mag, unb_phase, speed1, t)
    return F, speed1, t


@app.cell
def _(F, multirotor, speed1, t):
    # Time response
    time_resp = multirotor.run_time_response(speed1, F.T, t)
    amp_resp = time_resp.yout
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Due to computational cost limitations, the entire analysis performed for comparison is not included in this tutorial. However, by running the `run_time_response` function across the complete range of speeds, it is possible to obtain the following responses at nodes 2 and 7 as shown in the figures below:

    <div style="text-align: center;">
        <img src="../_static/img/img_tutorial4_node2.png" alt="MultiRotor" style="width: 40%; height: auto;">
        <img src="../_static/img/img_tutorial4_node7.png" alt="MultiRotor" style="width: 40%; height: auto;">
        <br>
        <small>Figure 3: Comparison of ROSS results with Yang et al. (2016) for the spur geared two-shaft rotor system.</small>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Creating a spur geared multi-shaft rotor system

    Let's create a more complex model with three connected rotors. More details of this example can be found in {cite}`yang2016general`.
    """)
    return


@app.cell
def _(Q_, material, rs):
    _L1 = [300, 92, 200, 200, 92, 300]
    r1 = [61.5, 75, 75, 75, 75, 61.5]
    _shaft1 = [rs.ShaftElement(L=_L1[i] * 0.001, idl=0.0, odl=r1[i] * 0.002, material=material, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(len(_L1))]
    D1 = rs.DiskElement(n=0, m=66.63, Id=0.431, Ip=0.735)
    D2 = rs.DiskElement(n=6, m=69.83, Id=0.542, Ip=0.884)
    cxx = 3000.0
    B1 = rs.BearingElement(n=2, kxx=550000000.0, kyy=670000000.0, cxx=cxx)
    B2 = rs.BearingElement(n=4, kxx=550000000.0, kyy=670000000.0, cxx=cxx)
    _pressure_angle = Q_(22.5, 'deg')
    G1 = rs.GearElement(n=3, m=14.37, Id=0.068, Ip=0.136, n_teeth=37, base_diameter=0.19, pr_angle=_pressure_angle)
    rotor1_1 = rs.Rotor(_shaft1, [D1, D2, G1], [B1, B2])
    _L2 = [80, 200, 200, 640]
    r2 = [160.5, 160.5, 130.5, 130.5]
    _shaft2 = [rs.ShaftElement(L=_L2[i] * 0.001, idl=0.0, odl=r2[i] * 0.002, material=material, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(len(_L2))]
    B3 = rs.BearingElement(n=1, kxx=3200000000.0, kyy=4600000000.0, cxx=cxx)
    B4 = rs.BearingElement(n=3, kxx=3200000000.0, kyy=4600000000.0, cxx=cxx)
    G2 = rs.GearElement(n=2, m=813.79, Id=52.36, Ip=104.72, n_teeth=244, base_diameter=1.23, pr_angle=_pressure_angle)
    rotor2_1 = rs.Rotor(_shaft2, [G2], [B3, B4])
    L3 = [300, 110, 200, 200, 110, 300]
    r3 = [64.5, 76.5, 76.5, 76.5, 76.5, 64.5]
    shaft3 = [rs.ShaftElement(L=L3[i] * 0.001, idl=0.0, odl=r3[i] * 0.002, material=material, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(len(_L1))]
    D3 = rs.DiskElement(n=0, m=95.06, Id=1.097, Ip=1.532)
    D4 = rs.DiskElement(n=6, m=96.22, Id=1.11, Ip=1.62)
    G3 = rs.GearElement(n=3, m=19.52, Id=0.098, Ip=0.195, n_teeth=47, base_diameter=0.24, pr_angle=_pressure_angle)
    B5 = rs.BearingElement(n=2, kxx=720000000.0, kyy=840000000.0, cxx=cxx)
    B6 = rs.BearingElement(n=4, kxx=720000000.0, kyy=840000000.0, cxx=cxx)
    rotor3 = rs.Rotor(shaft3, [D3, D4, G3], [B5, B6])
    return rotor1_1, rotor2_1, rotor3


@app.cell
def _(Q_, rotor1_1, rotor2_1, rs):
    # Connect rotor 1 with rotor 2 (driving rotor)
    multi_rotor1 = rs.MultiRotor(rotor2_1, rotor1_1, coupled_nodes=(2, 3), gear_mesh_stiffness=255000000.0, orientation_angle=Q_(270, 'deg'), position='above')
    return (multi_rotor1,)


@app.cell
def _(Q_, multi_rotor1, rotor3, rs):
    # Connect rotor 3 with rotor 2 in multi rotor
    psi = 90
    final_system = rs.MultiRotor(
        multi_rotor1,
        rotor3,
        coupled_nodes=(2, 3),
        gear_mesh_stiffness=2.6e8,
        orientation_angle=Q_(270 - psi, "deg"),
        position="below",
    )
    return (final_system,)


@app.cell
def _(final_system):
    final_system.plot_rotor()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we apply two unbalances with 92 g.mm in phase opposition at two ends of rotor 1 (nodes 5 and 11), while one unbalance with 294 g.mm at the middle of rotor 3 (node 15), we can obtain the following responses at node 15:


    <div style="text-align: center;">
        <img src="../_static/img/img_tutorial4_multi_compared.png" alt="MultiRotor" style="width: 40%; height: auto;">
        <br>
        <small>Figure 4: Comparison of ROSS results with Yang et al. (2016) for the spur geared multi-shaft rotor system.</small>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also vary the orientation angle between the rotors:

    <div style="text-align: center;">
        <img src="../_static/img/img_tutorial4_multi_all.png" alt="MultiRotor" style="width: 40%; height: auto;">
        <br>
        <small>Figure 5: Unbalance responses at node 15 with three orientation angles.</small>
    </div>
    """)
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
