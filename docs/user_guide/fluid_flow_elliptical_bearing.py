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
    # Fluid-flow: Elliptical Bearing
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Study below is based on {cite}`mota2020`, where is the complete theory used by *FluidFlow*:

    The elliptical bearing or "lemon bearing", as it is also known, is a variation of the cylindrical bearing with axial groove and reduced clearance in one direction.

    ![alt text](../_static/img/img_examplo_ff_eliptical.png)
    <style type="text/css">
        img {
            width: 350px;
        }
    </style>

    <!-- <img src="https://docs.google.com/uc?id=1EMhfdEnZkAHdd-yfL8VqrNTprkuxHRus" width="350"/> -->

    For the inclusion of this new geometry, adaptations to the stator radius are necessary, as it will no longer be constant in $\theta$. As seen in the figure above, the new stator is composed of the arc $C_{1}$, with center in $O_{1}$, joined to the arc $C_{2}$, centered in $O_{2}$, both with radius $R_{o}$. In this new configuration, the centers are at a distance $\epsilon$ from the origin, called ellipticity.

    It is necessary to describe the stator from the origin. This new distance will be called $R_{o}^{*} $ and it varies along the angular position:

    $$R_o^* = \sqrt{R_o ^2 - \epsilon^2 \sin^2{\alpha}} + \epsilon \cos{\alpha}$$

    where
    $$\alpha =\begin{cases}
    \pi/2 + \theta \text{,}
    &\text{if} \quad \theta \in 1^{\circ} \text{quadrant} \\
    3\pi/2 + \theta \text{,}
    &\text{if} \quad \theta \in 2^{\circ} \text{quadrant} \\
    \theta - \pi/2 \text{,}
    &\text{if} \quad \theta \in 3^{\circ} \text{quadrant} \\
    5\pi/2 -\theta \text{,}
    &\text{if} \quad \theta \in 4^{\circ} \text{quadrant}
    \end{cases}$$
    .

    Another important parameter to be defined is the $ m $ preload which, in this text, will be established as:

    $$m = \dfrac{\epsilon}{F}$$

    where $\epsilon$ is the ellipticity and $F=R_{o}-R_{i}$ is the radial clearance.

    For $m=0$, the bearing becomes cylindrical, while for $m \rightarrow 1$ the stator arcs tend to touch the axis.
    """)
    return


@app.cell
def _():
    import ross
    from ross.bearings.fluid_flow_graphics import (
        plot_pressure_theta,
        plot_pressure_surface,
    )
    from ross.bearings.fluid_flow_coefficients import calculate_oil_film_force
    from ross.bearings.fluid_flow_coefficients import find_equilibrium_position
    from ross.bearings.fluid_flow_coefficients import (
        calculate_stiffness_and_damping_coefficients,
    )

    from ross.bearings.fluid_flow import fluid_flow_example3
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"

    my_fluid_flow_eliptical = fluid_flow_example3()

    fig1 = plot_pressure_theta(
        my_fluid_flow_eliptical, z=int(my_fluid_flow_eliptical.nz / 2)
    )
    fig1.show()
    fig2 = plot_pressure_surface(my_fluid_flow_eliptical)
    fig2.show()

    radial_force, tangential_force, force_x, force_y = calculate_oil_film_force(
        my_fluid_flow_eliptical
    )
    print("N=", radial_force)
    print("T=", tangential_force)
    print("fx=", force_x)
    print("fy=", force_y)

    find_equilibrium_position(my_fluid_flow_eliptical)
    print("(xi,yi)=", "(", my_fluid_flow_eliptical.xi, ",", my_fluid_flow_eliptical.yi, ")")
    radial_force, tangential_force, force_x, force_y = calculate_oil_film_force(
        my_fluid_flow_eliptical
    )
    print("fx, fy=", force_x, ",", force_y)

    K, C = calculate_stiffness_and_damping_coefficients(my_fluid_flow_eliptical)
    kxx, kxy, kyx, kyy = K[0], K[1], K[2], K[3]
    cxx, cxy, cyx, cyy = C[0], C[1], C[2], C[3]
    print("Stiffness coefficients:")
    print("kxx, kxy, kyx, kyy = ", kxx, kxy, kyx, kyy)
    print("Damping coefficients:")
    print("cxx, cxy, cyx, cyy", cxx, cxy, cyx, cyy)
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
