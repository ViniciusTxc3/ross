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
    # Example 31 - Isotropic Bearings with Damping

    This example is based on Example 5.9.5 from {cite}friswell2010dynamics

    The isotropic bearing Example 5.9.1 (Example 17) is repeated but with damping in the bearings. The, _x_ and _y_ directions are uncoupled, with a translational stiffness of 1 MN/m and a damping of 3 kNs/m in each direction.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import pandas as pd

    from ross.units import Q_

    return Q_, np, pd, rs


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.2e9, rho=7810)
    return (steel,)


@app.cell
def _(rs, steel):
    L = 0.25
    N = 6
    idl = 0
    odl = 0.05

    shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for i in range(N)]

    bearings = [
        rs.BearingElement(n=0, kxx=1e6, kyy=1e6, cxx=3e3, cyy=3e3, scale_factor=2),
        rs.BearingElement(n=len(shaft), kxx=1e6, kyy=1e6, cxx=3e3, cyy=3e3, scale_factor=2),
    ]

    disks = [
        rs.DiskElement.from_geometry(
            n=2, material=steel, width=0.07, i_d=odl, o_d=0.28, scale_factor="mass"
        ),
        rs.DiskElement.from_geometry(
            n=4, material=steel, width=0.07, i_d=odl, o_d=0.35, scale_factor="mass"
        ),
    ]

    rotor = rs.Rotor(shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings)
    rotor.plot_rotor()
    return (rotor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Campbell Diagram
    """)
    return


@app.cell
def _(Q_, rotor):
    campbell = rotor.run_campbell(speed_range=Q_(list(range(0, 4500, 50)), "RPM"))
    return (campbell,)


@app.cell
def _(campbell):
    campbell.plot(frequency_units="RPM", frequencies=8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the Mode Shapes and Damped Natural Frequencies
    """)
    return


@app.cell
def _(Q_, rotor):
    modal = rotor.run_modal(speed=Q_(4000, "RPM"))
    return (modal,)


@app.cell
def _(display, modal):
    for mode in range(7):
        display(modal.plot_mode_3d(mode, frequency_units="Hz"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating table with eigenvalues, natural frequencies and damping ratios
    """)
    return


@app.cell
def _(Q_, display, np, pd, rotor):
    def modal_table(modal_results, rpm):
        eig = modal_results.evalues
        omega_n = np.abs(eig)
        omega_d = np.imag(eig)
        zeta = -np.real(eig) / omega_n
        fn = omega_n / (2 * np.pi)
        fd = omega_d / (2 * np.pi)

        return pd.DataFrame(
            {
                "Speed (RPM)": [rpm] * 8,
                "Root s (rad/s)": eig[:8],
                "Wn (Hz)": fn[:8],
                "Wd (Hz)": fd[:8],
                "Damping Ratio": zeta[:8],
            }
        )


    modal_0 = rotor.run_modal(speed=Q_(0, "RPM"))
    modal_4000 = rotor.run_modal(speed=Q_(4000, "RPM"))

    df_modal_0 = modal_table(modal_0, rpm=0)
    df_modal_4000 = modal_table(modal_4000, rpm=4000)
    df_combined = pd.concat([df_modal_0, df_modal_4000], ignore_index=True)

    display(df_combined)
    return


if __name__ == "__main__":
    app.run()
