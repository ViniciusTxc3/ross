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
    Example 8 - Overhung rotor.
    =========
    In this example, we use the rotor seen in Example 5.9.9 from {cite}`friswell2010dynamics`.

    The shaft is $1.5m$ long and the diameter is $50 mm$ with a disk of diameter $350mm$ and thickness $70 mm$. The two bearings, have a stiffness of $10 MN/m$ in each direction. The shaft and disk are made of steel. Damping is neglected.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return np, rs


@app.cell
def _(rs):
    shaft_elements = []
    disk_elements = []
    bearing_seal_elements = []
    steel = rs.steel

    bearing_seal_elements.append(rs.BearingElement(n=0, kxx=10e6, kyy=10e6, cxx=0, cyy=0))
    bearing_seal_elements.append(rs.BearingElement(n=1, kxx=10e6, kyy=10e6, cxx=0, cyy=0))

    shaft_elements.append(rs.ShaftElement(material=steel, n=0, L=1, odl=0.05, idl=0))
    shaft_elements.append(rs.ShaftElement(material=steel, n=1, L=0.5, odl=0.05, idl=0))

    disk_elements.append(
        rs.DiskElement.from_geometry(n=2, i_d=0.05, o_d=0.35, width=0.07, material=steel)
    )

    # Moment approach
    overhung_rotor = rs.Rotor(
        shaft_elements=shaft_elements,
        bearing_elements=bearing_seal_elements,
        disk_elements=disk_elements,
    )
    # from section approach
    leng_data = [1.0, 0.5]

    overhung_from_section_rotor = rs.Rotor.from_section(
        brg_seal_data=bearing_seal_elements,
        disk_data=disk_elements,
        leng_data=leng_data,
        idl_data=[0, 0],
        odl_data=[0.05, 0.05],
        material_data=steel,
    )
    overhung_from_section_rotor.plot_rotor()
    return (overhung_from_section_rotor,)


@app.cell
def _(np, overhung_from_section_rotor):
    modal = overhung_from_section_rotor.run_modal(0)

    print("From section approach =", modal.wn / (2 * np.pi))
    return


@app.cell
def _(np, overhung_from_section_rotor):
    overhung_from_section_rotor.run_campbell(np.linspace(0, 4000 * np.pi / 30, 50)).plot()
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
