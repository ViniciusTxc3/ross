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
    # Example 25 - Coaxial rotor

    This example is based on Example 6.8.1 from {cite}`friswell2010dynamics`.

    Consider the model of a simple overhung rotor, 1.5 m long with bearings at 0.0 m and 1.0 m, and shown in Figure 6.49. The bearings are short in that they present insignificant angular stiffness to the shaft, but they present finite translational stiffness. The shaft is 25 mm in diameter and the disk at the overhung end is 250 mm in diameter and 40 mm thick. The shaft and disk are made of steel, and a mass density p = 7,810 kg/m3, a modulus of elasticity E = 211 GPa, and a Poisson’s ratio of 0.3 are assumed. Several different variants of this system are considered in which the differences lie in the bearing (and bearing-support) properties, shown in Table 6.3, and the steady rotational speed of the shaft. Calculate the eigenvalues for various rotor spin speeds and estimate the critical speeds for unbalance excitation.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import plotly.graph_objects as go
    import pandas as pd

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"

    Q_ = rs.Q_
    rs.__version__
    return Q_, np, pd, rs


@app.cell
def _(rs):
    # Material
    steel = rs.Material("steel", E=211e9, Poisson=0.3, rho=7810)
    return (steel,)


@app.cell
def _(Q_, rs, steel):
    # Cylindrical shaft elements
    L = 6 * [250]
    i_d = 6 * [0]
    o_d = 6 * [25]
    shaft_elements = [rs.ShaftElement(n=_i, L=Q_(l, 'mm'), idl=Q_(id1, 'mm'), odl=Q_(od1, 'mm'), material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for (_i, l, id1, od1) in zip(range(len(L)), L, i_d, o_d)]
    print('Number os shaft elements: %d.' % len(shaft_elements))
    return (shaft_elements,)


@app.cell
def _(Q_, rs):
    # Creating a disk element
    disk_elements = [
        rs.DiskElement(
            n=6,
            m=Q_(15.3, "kg"),
            Id=Q_(0.062, "kg * m**2"),
            Ip=Q_(0.120, "kg * m**2"),
            scale_factor=6,
        )
    ]
    return (disk_elements,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Characteristic roots computed for a number of configurations
    """)
    return


@app.cell
def _(Q_, disk_elements, np, pd, rs, shaft_elements):
    """
        Table 6.3 - Bearing and Support characteristics
    """
    cases = {1: [10, 10, 0, 0], 2: [10, 20, 0, 0], 3: [10, 20, 60, 60], 4: [10, 20, 400, 400], 5: [0.2, 0.4, 0, 0]}
    '\n    Bearing configurations from table 6.4\n'
    configurations = [[0, 1, 1], [0, 2, 2], [0, 2, 3], [0, 2, 4], [0, 5, 5], [1000.0, 1, 1], [1000.0, 2, 3], [2000.0, 2, 3], [3000.0, 2, 3]]
    data = []
    bearing_pairs = []
    pd.options.display.float_format = '{:.3f}'.format
    for _i in configurations:
        (speed, left, rigth) = _i
        bearing_elements = [rs.BearingElement(n=0, kxx=cases[left][0] * 1000000.0, kyy=cases[left][1] * 1000000.0, cxx=cases[left][2] * 1000.0, cyy=cases[left][3] * 1000.0, scale_factor=6), rs.BearingElement(n=4, kxx=cases[rigth][0] * 1000000.0, kyy=cases[rigth][1] * 1000000.0, cxx=cases[rigth][2] * 1000.0, cyy=cases[rigth][3] * 1000.0, scale_factor=6)]
        rotor = rs.Rotor(shaft_elements, disk_elements, bearing_elements)
        bearing_pairs.append(bearing_elements)
        _modal = rotor.run_modal(speed=Q_(speed, 'RPM'))
        roots = []
        for root in _modal.evalues:
            if np.iscomplex(root):
                roots.append(root)
            if len(roots) == 4:
                break
        data.append({('Config:', 'Speed'): speed, ('Config:', 'Left'): left, ('Config:', 'Rigth'): rigth, ('Roots:', 'First'): roots[0], ('Roots:', 'Second'): roots[1], ('Roots:', 'Third'): roots[2], ('Roots:', 'Fourth'): roots[3]})
    multi_index = pd.MultiIndex.from_tuples([('Config:', 'Speed'), ('Config:', 'Left'), ('Config:', 'Rigth'), ('Roots:', 'First'), ('Roots:', 'Second'), ('Roots:', 'Third'), ('Roots:', 'Fourth')])
    df = pd.DataFrame(data, columns=multi_index)
    # Create empty lists to store data and bearing pairs
    # Configure Pandas to display only three decimal places
    # Use a for loop to generate data
    # Convert the list of dictionaries to a DataFrame
    # Display the DataFrame
    df  # Bearings instances  # Saving bearing pairs for later analysis  # Performing modal analysis  # Selection of the first 4 complex roots
    return (bearing_pairs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rotor Model
    """)
    return


@app.cell
def _(bearing_pairs, disk_elements, np, rs, shaft_elements):
    rotor_1 = rs.Rotor(shaft_elements, disk_elements, bearing_pairs[4])
    print('ROTOR DATA:\nRotor total mass = ', np.round(rotor_1.m, 2))
    print('Rotor center of gravity =', np.round(rotor_1.CG, 2))
    rotor_1.plot_rotor(width=500, height=400)
    return (rotor_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Campbell Diagram

    The following chart presents the Campbell diagram for a system where both the left and right bearings exhibit the characteristics of Case 5, as detailed in Table 6.3 on page 279 of [Fryswell, 2010](#References).

    The chart can be found in page 280 of the reference.
    """)
    return


@app.cell
def _(np, rotor_1):
    samples = 41
    max_spin = 400
    speed_range = np.linspace(0, max_spin, samples)
    campbell = rotor_1.run_campbell(speed_range, frequency_type='wn')
    _fig = campbell.plot(frequency_units='rpm', width=600, height=600)
    for _i in _fig.data:
        try:
            _i['y'] = _i['y'] / 60
        except:
            pass
    _fig.update_yaxes(title='Natural Frequencies (Hz)', range=[0, 90])
    _fig.update_xaxes(title='Rotor Spin Speed (rpm)', range=[0, max_spin * 60 / (2 * np.pi)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Modal Shapes

    Mode shapes for the critical speeds for the onverhung rotor. This example is based on Example 6.9.1 page 281 from [Fryswell, 2010](#References).

    Find the critical speeds and associated mode shapes for the
    system defined in Example 6.8.1 with bearing ccharacteristic case 5, defined in
    Table 6.3.
    """)
    return


@app.cell
def _(Q_, rotor_1):
    _modal = rotor_1.run_modal(speed=Q_(358.43, 'RPM'))
    _fig = _modal.plot_mode_3d(0, frequency_units='rpm', width=600, height=600)
    _fig.layout.title.text = 'FIRST CRITICAL SPEED' + _fig.layout.title.text
    _fig
    return


@app.cell
def _(Q_, rotor_1):
    _modal = rotor_1.run_modal(speed=Q_(389.35, 'RPM'))
    _fig = _modal.plot_mode_3d(1, frequency_units='rpm', width=600, height=600)
    _fig.layout.title.text = 'SECOND CRITICAL SPEED' + _fig.layout.title.text
    _fig
    return


@app.cell
def _(Q_, rotor_1):
    _modal = rotor_1.run_modal(speed=Q_(2123.79, 'RPM'))
    _fig = _modal.plot_mode_3d(2, frequency_units='rpm', width=600, height=600)
    _fig.layout.title.text = 'THIRD CRITICAL SPEED' + _fig.layout.title.text
    _fig
    return


@app.cell
def _(Q_, rotor_1):
    _modal = rotor_1.run_modal(speed=Q_(2659.1, 'RPM'))
    _fig = _modal.plot_mode_3d(3, frequency_units='rpm', width=600, height=600)
    _fig.layout.title.text = 'FOURTH CRITICAL SPEED' + _fig.layout.title.text
    _fig
    return


@app.cell
def _(Q_, rotor_1):
    _modal = rotor_1.run_modal(speed=Q_(3118.14, 'RPM'))
    _fig = _modal.plot_mode_3d(4, frequency_units='rpm', width=600, height=600)
    _fig.layout.title.text = 'FIFHT CRITICAL SPEED' + _fig.layout.title.text
    _fig
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
