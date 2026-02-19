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
    # Fluid-flow: Short Bearing
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the literature on bearings, several studies use the Reynolds equation,

    $$ \dfrac{\partial}{\partial{x}}\left(h^3\dfrac{\partial{p}}{\partial{x}}\right)+\dfrac{\partial}{\partial{z}}\left(h^3\dfrac{\partial{p}}{\partial{z}}\right) = 6 \mu \left\{ \left(U_o + U_1\right) \dfrac{\partial{h}}{\partial{x}} + 2 V \right\}$$

    after a series of simplifications, to find the pressure behavior in bearings. However, as it is an equation that has no analytical solution, they use the artifice of approximating the equation for cases of short bearings $\left(L/D \rightarrow 0 \right)$ and infinitely long $\left(L/D \rightarrow \infty \right)$ (L length, D diameter). Thus, one of the parts of the equation is neglected, and it is possible to find reduced models that can be solved analytically.

    Most modern bearings in high performance turbomachinery applications have a small $L/D$ ratio, rarely exceeding the unit. The author indicates that the short model provides accurate results for cylindrical bearings with the ratio $L/D \leq 0.5$, being widely used for quick estimates of the performance characteristics of the static and dynamic forces of the bearing.

    In this context, the bearing length is considered to be very small and, according to {cite}`ishida2013linear`, the pressure variation in the $z$ direction can be considered much greater than in the $ x $ direction, that is, $\partial p/\partial x \ll \partial p/\partial z$. Thus, the first term of the Reynolds equation is neglected. Making the appropriate adjustments to the coordinate system adopted in this work, a formula is then obtained that describes the pressure behavior in the short bearing:

    $$
    p_{curto} = \dfrac{-3\mu \epsilon \omega \sin{\theta}}{\left(R_\theta - R_i\right)^2\left(1 + \epsilon \cos{\theta}\right)^3}\left[\left(z-\dfrac{L}{2}\right)^2 - \dfrac{L^2}{4}\right]
    $$

    where $\epsilon = \dfrac{e}{R_{o} - R_{i}}$ is the reason for eccentricity.

    The numerical solution presented is verified with this approximation, which is used by the Fluid-Flow code if the bearing is classified as short ($L/D \leq 1/4$)
    """)
    return


@app.cell
def _():
    import ross
    from ross.bearings.fluid_flow_graphics import (
        plot_pressure_theta_cylindrical,
        plot_pressure_z,
        plot_pressure_theta,
        plot_pressure_surface,
    )
    from ross.bearings.fluid_flow import fluid_flow_example
    import plotly.graph_objects as go

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"

    my_fluid_flow_short = fluid_flow_example()
    my_fluid_flow_short.calculate_pressure_matrix_analytical()

    fig1 = plot_pressure_z(my_fluid_flow_short, theta=int(my_fluid_flow_short.ntheta / 2))
    fig1.show()
    fig2 = plot_pressure_theta(my_fluid_flow_short, z=int(my_fluid_flow_short.nz / 2))
    fig2.show()
    fig3 = plot_pressure_theta_cylindrical(
        my_fluid_flow_short, z=int(my_fluid_flow_short.nz / 2)
    )
    fig3.show()
    return (my_fluid_flow_short,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **FORCES**

    For the approach of a short bearing, it is possible to perform the integrals analytically to obtain the forces of the oil film. These are given by {cite}`ishida2013linear` in the stationary context as:

    $$N = \dfrac{1}{2}\mu\left(\dfrac{R_i}{R_o - R_i}\right)^2 \dfrac{L^3}{r}\left[\dfrac{2\epsilon^2\omega}{\left(1-\epsilon^2\right)^2} \right]$$
    $$T = \dfrac{1}{2}\mu\left(\dfrac{R_i}{R_o - R_i}\right)^2 \dfrac{L^3}{r}\left[\dfrac{\pi\epsilon\omega}{2\left(1-\epsilon^2\right)^{3/2}} \right]$$
    """)
    return


@app.cell
def _(my_fluid_flow_short):
    from ross.bearings.fluid_flow_coefficients import calculate_oil_film_force

    radial_force, tangential_force, force_x, force_y = calculate_oil_film_force(
        my_fluid_flow_short, force_type="short"
    )
    print("N=", radial_force)
    print("T=", tangential_force)
    print("fx=", force_x)
    print("fy=", force_y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **EQUILIBRIUM POSITION**

    It is known that, in the equilibrium position, the vertical force $f_y$ tends to balance with the applied external load $W$. Thus, knowing $W$ and an equation of the force $f_y$ to approach the short bearing, it is possible to obtain the eccentricity of the rotor. According to {cite}`friswell2010dynamics`, this information is obtained by solving the quadratic polynomial in $\epsilon^2$

    $$\epsilon^8 - 4\epsilon^6 + \left(6 - S_s^2\left(16 -\pi^2\right)\right)\epsilon^4 - \left(4 + \pi^2 S_s^2\right)\epsilon^2 +1=0$$

    where $S_s=\dfrac{2R_o \omega \mu L^3}{8WF^2}$ is called the modified Sommerfeld number.

    Still according to {cite}`friswell2010dynamics`, the direction of the force given by:

    $$\tan{\beta}=\dfrac{\pi\sqrt{1 - \epsilon^2}}{4\epsilon}$$
    """)
    return


@app.cell
def _(my_fluid_flow_short):
    from ross.bearings.fluid_flow_geometry import (
        modified_sommerfeld_number,
        calculate_eccentricity_ratio,
        calculate_attitude_angle,
    )

    modified_s = modified_sommerfeld_number(
        my_fluid_flow_short.radius_stator,
        my_fluid_flow_short.omega,
        my_fluid_flow_short.viscosity,
        my_fluid_flow_short.length,
        my_fluid_flow_short.load,
        my_fluid_flow_short.radial_clearance,
    )
    eccentricity_ratio = calculate_eccentricity_ratio(modified_s)
    beta = calculate_attitude_angle(eccentricity_ratio)
    print("Eccentricity ratio=", eccentricity_ratio)
    print("Attitude angle=", beta)
    print("(xi,yi)=", "(", my_fluid_flow_short.xi, ",", my_fluid_flow_short.yi, ")")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **DYNAMIC COEFFICIENTS**

    Once equations have been obtained that describe the forces $ f_x $ and $ f_y $ on the short bearing, it is possible to perform analytically the derivatives that define the stiffness and damping coefficients. {cite}`friswell2010dynamics` presents the stiffness and damping matrices as:

    $$K = \dfrac{W}{F}\begin{bmatrix}
    k_{xx} & k_{xy}\\
    k_{yx} & k_{yy}
    \end{bmatrix}\text{,}\quad
    C = \dfrac{W}{F\omega}\begin{bmatrix}
    c_{xx} & c_{xy}\\
    c_{yx} & c_{yy}
    \end{bmatrix}$$

    where

    $k_{xx} = 4 h_0 \left(\pi^2 \left(2 - \epsilon^2\right)+16\epsilon^2\right)\text{,}$

    $k_{xy} = h_0 \dfrac{\pi \left(\pi^2 \left(1 - \epsilon^2\right)^2 - 16\epsilon^4\right)}{\epsilon\sqrt{1-\epsilon^2}}\text{,}$

    $k_{yx} = - h_0 \dfrac{
    			\pi \left(
    				\pi^2
    				\left(1-\epsilon^2\right)
    				\left(1+2\epsilon^2\right)
    				+32\epsilon^2
    				\left(1+\epsilon^2\right)
    \right) }
    {\epsilon\sqrt{1-\epsilon^2}}\text{,}$

    $k_{yy} = 4 h_0 \left(\pi^2 \left(1 + 2\epsilon^2\right) + \dfrac{32\epsilon^2\left(1+\epsilon^2 \right)}
    {1-\epsilon^2} \right)\text{,}$

    $c_{xx} = h_0 \dfrac{2 \pi \sqrt{1 - \epsilon^2}
    			\left(\pi^2 \left(1 + 2\epsilon^2\right)
    			-16\epsilon^2
    \right)}
    {\epsilon}\text{,}$

    $c_{xy} = c_{yx} = - 8 h_0 \left(\pi^2 \left(1 + 2\epsilon^2\right) -16 \epsilon^2 \right)\text{,}$

    $c_{yy} = h_0 \dfrac{2\pi\left(\pi^2\left(1 - \epsilon^2\right)^2 +48 \epsilon^2\right)}{\epsilon\sqrt{1 - \epsilon^2}}\text{,}$

    and

    $h_0 = \dfrac{1}{\left(\pi^2\left(1 - \epsilon^2\right)+16\epsilon^2\right)^{3/2}}\text{.}$
    """)
    return


@app.cell
def _(my_fluid_flow_short):
    from ross.bearings.fluid_flow_coefficients import (
        calculate_short_stiffness_matrix,
        calculate_short_damping_matrix,
    )

    [kxx, kxy, kyx, kyy] = calculate_short_stiffness_matrix(my_fluid_flow_short)
    [cxx, cxy, cyx, cyy] = calculate_short_damping_matrix(my_fluid_flow_short)

    print("Stiffness coefficients:")
    print("kxx, kxy, kyx, kyy = ", kxx, kxy, kyx, kyy)
    print("Damping coefficients:")
    print("cxx, cxy, cyx, cyy", cxx, cxy, cyx, cyy)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Most modern bearings in high-performance turbomachinery applications have a small $L/D$ ratio, rarely exceeding the unit. The author indicates that the short model provides accurate results for cylindrical bearings with the ratio $L/D \leq 0.5$, being widely used for quick estimates of the performance characteristics of the static and dynamic forces of the bearing.

    The results obtained by the Fluid Flow numerical solutions are compatible with these approaches for bearings with the ratio $L/D \leq 0.25$. However, it is worth mentioning that the features of Fluid Flow are not restricted to the context of short bearings, making it possible to explore other sizes and geometries.
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
