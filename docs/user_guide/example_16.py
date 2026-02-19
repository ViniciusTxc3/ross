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
    # Example 16 - Look at different models of the disk-shaft interface

    In this example, we use the rotor seen in Example 5.8.3 from {cite}`friswell2010dynamics`
    and we make the same comparison looking at 4 different ways of modelling the shaft-disk interface:

    ```
    Consider a hollow shaft carrying a central disk and mounted on
    short, rigid bearings at each end. The shaft is 1.2 m long and it has an outside
    diameter of 80 mm and an inside diameter of 30 mm. The central disk has a diameter
    of 400 mm and a thickness of 80 mm. The shaft and disk have a modulus
    of elasticity of 200GN/m2 and a density of 7,800kg/m3. Poisson’s ratio is 0.27.
    This is the same as the rotor used in Example 5.8.1. The rotor, consisting of
    the shaft and central disk, spins at 3,000 rev/min. Investigate the effect of the
    shaft-disk interface models on the natural frequencies of the machine.
    ```
    """)
    return


@app.cell
def _():
    import ross as rs
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return (rs,)


@app.cell
def _(rs):
    Q_ = rs.Q_
    steel = rs.Material("steel", rho=7800, E=200e9, Poisson=0.27)
    return Q_, steel


@app.cell
def _():
    L = 0.2
    idl = 0.03
    odl = 0.08
    return L, idl, odl


@app.cell
def _(L, idl, odl, rs, steel):
    N = 6
    _shaft = [rs.ShaftElement(L=L, idl=idl, odl=odl, material=steel) for i in range(N)]
    _bearings = [rs.BearingElement(n=0, kxx=1e+20, cxx=0), rs.BearingElement(n=len(_shaft), kxx=1e+20, cxx=0)]
    _disks = [rs.DiskElement.from_geometry(n=3, material=steel, width=0.08, o_d=0.4, i_d=0.08)]
    rotor1 = rs.Rotor(shaft_elements=_shaft, disk_elements=_disks, bearing_elements=_bearings)
    rotor1.plot_rotor()
    return (rotor1,)


@app.cell
def _(L, idl, odl, rs, steel):
    _shaft = [rs.ShaftElement(n=0, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=1, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=2, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=3, L=0.04, idl=idl, odl=0.16, material=steel), rs.ShaftElement(n=4, L=0.04, idl=idl, odl=0.16, material=steel), rs.ShaftElement(n=5, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=6, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=7, L=L, idl=idl, odl=odl, material=steel)]
    _bearings = [rs.BearingElement(n=0, kxx=1e+20, cxx=0), rs.BearingElement(n=len(_shaft), kxx=1e+20, cxx=0)]
    _disks = [rs.DiskElement.from_geometry(n=4, material=steel, width=0.08, o_d=0.4, i_d=0.16)]
    rotor2 = rs.Rotor(shaft_elements=_shaft, disk_elements=_disks, bearing_elements=_bearings)
    rotor2.plot_rotor()
    return (rotor2,)


@app.cell
def _(L, idl, odl, rs, steel):
    _shaft = [rs.ShaftElement(n=0, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=1, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=2, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=3, L=0.04, idl=idl, odl=0.16, material=steel), rs.ShaftElement(n=4, L=0.04, idl=idl, odl=0.16, material=steel), rs.ShaftElement(n=5, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=6, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=7, L=L, idl=idl, odl=odl, material=steel)]
    _bearings = [rs.BearingElement(n=0, kxx=1e+20, cxx=0), rs.BearingElement(n=len(_shaft), kxx=1e+20, cxx=0)]
    _disks = [rs.DiskElement.from_geometry(n=3, material=steel, width=0.02, o_d=0.4, i_d=0.16), rs.DiskElement.from_geometry(n=4, material=steel, width=0.04, o_d=0.4, i_d=0.16), rs.DiskElement.from_geometry(n=5, material=steel, width=0.02, o_d=0.4, i_d=0.16)]
    rotor3 = rs.Rotor(shaft_elements=_shaft, disk_elements=_disks, bearing_elements=_bearings)
    rotor3.plot_rotor()
    return (rotor3,)


@app.cell
def _(L, idl, odl, rs, steel):
    _shaft = [rs.ShaftElement(n=0, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=1, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=2, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=3, L=0.08, idl=idl, odl=0.4, material=steel), rs.ShaftElement(n=4, L=0.16, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=5, L=L, idl=idl, odl=odl, material=steel), rs.ShaftElement(n=6, L=L, idl=idl, odl=odl, material=steel)]
    _bearings = [rs.BearingElement(n=0, kxx=1e+20, cxx=0), rs.BearingElement(n=len(_shaft), kxx=1e+20, cxx=0)]
    rotor4 = rs.Rotor(shaft_elements=_shaft, bearing_elements=_bearings)
    rotor4.plot_rotor()
    return (rotor4,)


@app.cell
def _(Q_, rotor1, rotor2, rotor3, rotor4, rs):
    for i, rotor in enumerate([rotor1, rotor2, rotor3, rotor4]):
        modal = rotor.run_modal(rs.Q_(3000, "RPM"))
        print(f"Rotor {i + 1}: {Q_(modal.wd, 'rad/s').to('Hz'):.4f}")
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
