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
    # Example 24 - A Tapared Shaft

    This example is based on Example 5.9.10 from {cite}`friswell2010dynamics`.

    A Tapered Shaft. Consider a tapered shaft of length 1.5 m and
    a diameter that changes linearly from 25 to 40 mm. A disk of diameter 250 mm
    and thickness 40 mm is placed at the center of the shaft, and short bearings
    of stiffness 10 MN/m and damping 1 kNs/m are attached at the ends of the
    shaft. The Young’s modulus and mass density are 211 GN/mz and 7,810 kg/m3,
    respectively. Estimate the first pair of natural frequencies of this machine at
    3,000 rev/min using a stepped shaft diameter and elements of uniform diameter
    and by using tapered elements.
    """)
    return


@app.cell
def _():
    import ross as rs
    import numpy as np
    import plotly.graph_objects as go
    from IPython.display import display

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return display, go, np, rs


@app.cell
def _(rs):
    Q_ = rs.Q_
    return (Q_,)


@app.cell
def _(rs):
    steel = rs.Material("steel", E=211e9, G_s=81.2e9, rho=7810)
    return (steel,)


@app.cell
def _(Q_, display, np, rs, steel):
    shaft_length = 1.5
    diameter_left = 0.025
    diameter_right = 0.04
    min_elements = 4
    max_elements = 30
    step = 2
    num_simulations = (max_elements - min_elements) // step
    results = np.zeros((2, num_simulations))
    results_tapared = np.zeros((2, num_simulations))
    for (_i, N) in enumerate(range(min_elements, max_elements, step)):
        L = shaft_length / N
        odl_array = np.linspace(diameter_left, diameter_right, N + 1)[:-1]
        idl_array = np.zeros_like(odl_array)
        odr_array = np.linspace(diameter_left, diameter_right, N + 1)[1:]
        idr_array = np.zeros_like(odr_array)
        id_array = np.zeros(N)
        od_array = np.mean(np.array([odl_array, odr_array]), axis=0)
        shaft = []
        shaft_tapared = []
        for n in range(N):
            shaft.append(rs.ShaftElement(n=n, L=L, idl=id_array[n], odl=od_array[n], material=steel))
            shaft_tapared.append(rs.ShaftElement(n=n, L=L, idl=idl_array[n], idr=idr_array[n], odl=odl_array[n], odr=odr_array[n], material=steel))
        bearings = [rs.BearingElement(n=0, kxx=10000000.0, cxx=1000.0, scale_factor=2), rs.BearingElement(n=N, kxx=10000000.0, cxx=1000.0, scale_factor=2)]
        disks = [rs.DiskElement.from_geometry(n=N // 2, material=steel, width=0.04, i_d=0.0, o_d=0.25)]
        rotor = rs.Rotor(shaft_elements=shaft, disk_elements=disks, bearing_elements=bearings)
        rotor_tapared = rs.Rotor(shaft_elements=shaft_tapared, disk_elements=disks, bearing_elements=bearings)
        modal = rotor.run_modal(speed=Q_(3000, 'RPM'))
        modal_tapared = rotor_tapared.run_modal(speed=Q_(3000, 'RPM'))
        results[:, _i] = Q_(modal.wd[:2], 'rad/s').to('Hz').m
        results_tapared[:, _i] = Q_(modal_tapared.wd[:2], 'rad/s').to('Hz').m
        if N == 6:
            display(rotor.plot_rotor(nodes=2, title=dict(text='Uniform shaft elements')))
            display(rotor_tapared.plot_rotor(nodes=2, title=dict(text='Tapared shaft elements')))
    return max_elements, min_elements, results, results_tapared, step


@app.cell
def _(go, max_elements, min_elements, results, results_tapared, step):
    fig = go.Figure()
    N_eigen = 2
    for _i in range(N_eigen):
        fig.add_trace(go.Scatter(x=list(range(min_elements, max_elements, step)), y=results[_i, :], line=dict(dash='dash'), name=f'Uniform Elements - Mode {_i}'))
        fig.add_trace(go.Scatter(x=list(range(min_elements, max_elements, step)), y=results_tapared[_i, :], name=f'Tapared Elements - Mode {_i}'))
    fig.update_layout(xaxis=dict(title='Number of Elements'), yaxis=dict(title='Natural Frequency (Hz)'))
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
