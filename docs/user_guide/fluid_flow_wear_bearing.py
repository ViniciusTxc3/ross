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
    # Fluid-flow: Wear Bearing
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **WEAR BEARINGS**

    Although lubrication reduces the friction between the metal surfaces of the bearing, these structures usually suffer wear after a long operating period or else due to a certain number of repetitions of the starting cycles.

    ![alt text](../_static/img/img_examplo_ff_wear.png)
    <style type="text/css">
        img {
            width: 350px;
        }
    </style>

    <!-- <img src="https://docs.google.com/uc?id=1ZGYl4aCO3WTx-hp_Bkh9PpQMEWCKOwsL" width="350"/> -->

    The wear geometry that will be used in the FluidFlow has been adapted from the version presented by MACHADO; CAVALCA (2015) [1]. To include wear in the geometry, it is necessary to make some adaptations to the stator radius. Considering that the fault starts at the angular position $\theta = \theta_{s}$ and ends at $\theta = \theta_{f}$, the stator description from the origin is defined as:

    $$R_o^* = R_o + d_{\theta}$$

    where
    $$d_{\theta} =\begin{cases}
        0 \text{,}
        &\text{if}
        \quad 0 \leq \theta \leq \theta_s\text{,} \quad
        \theta_f \leq \theta \leq 2\pi \\
        d_0 - F \left(1 + \cos{\left(\theta - \pi/2\right)} \right) \text{,}
        &\text{if}
        \quad \theta_s < \theta < \theta_f
    \end{cases}$$
    .

    In $\theta_{s}$ and $\theta_{f}$, the wear depth is zero, so the location of the edges can be defined as follows:

    $$\theta_s = \pi/2 + \cos^{-1}{\left(d_0/F -1\right)} + \gamma \nonumber\\
        \theta_f = \pi/2 - \cos^{-1}{\left(d_0/F -1\right)} + \gamma $$
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

    from ross.bearings.fluid_flow import fluid_flow_example4
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"

    my_fluid_flow_wear = fluid_flow_example4()

    fig8 = plot_pressure_theta(my_fluid_flow_wear, z=int(my_fluid_flow_wear.nz / 2))
    fig8.show()
    fig9 = plot_pressure_surface(my_fluid_flow_wear)
    fig9.show()

    radial_force, tangential_force, force_x, force_y = calculate_oil_film_force(
        my_fluid_flow_wear
    )
    print("N=", radial_force)
    print("T=", tangential_force)
    print("fx=", force_x)
    print("fy=", force_y)

    find_equilibrium_position(my_fluid_flow_wear)
    print("(xi,yi)=", "(", my_fluid_flow_wear.xi, ",", my_fluid_flow_wear.yi, ")")
    radial_force, tangential_force, force_x, force_y = calculate_oil_film_force(
        my_fluid_flow_wear
    )
    print("fx, fy=", force_x, ",", force_y)

    K, C = calculate_stiffness_and_damping_coefficients(my_fluid_flow_wear)
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
    #### Based on MOTA (2020), where is the complete theory used by *FluidFlow*:

    Mota, J. A.; **Estudo da teoria de lubrificação com parametrização diferenciada da geometria e aplicações em mancais hidrodinâmicos.** Dissertação de Mestrado - Programa de Pós-Graduação em Informática, Universidade Federal do Rio de Janeiro, Rio de Janeiro, 2020



    **REFERENCES CITED IN THE TEXT**

    [1] MACHADO, T. H.; CAVALCA, K. L. Modeling of hydrodynamic bearing wear in rotor-bearing systems. **Mechanics Research Communications** - Elsevier, [S.l.],v. 69, p. 15–23, 2015.
    """)
    return


if __name__ == "__main__":
    app.run()
