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
    Tutorial - Stochastic ROSS
    ======================
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a basic tutorial on how to use STOCHASTIC ROSS - a ROSS' module for stochastic rotordynamics analysis. Before starting this tutorial, be sure you're already familiar with ROSS library.

    If you've already used ROSS, you've noticed the graphs present deterministic results, considering a set of parameters. In other words, the model always produce the same output from a given starting condition or initial state. In STOCHASTIC ROSS, the concept is different, and we'll work it stochastic processes.

    A stochastic process is defined as a indexed collection of random variables defined on a common probability space ($\Omega$, $\mathcal{F}$, $P$} where $\Omega$ is a sample space, $\mathcal{F}$ is a $\sigma$-algebra, and $P$ is a probability measure. The index is often assumed to be time.

    This new module allows you to work with random variables applied to the ROSS' functions. Basically, any element or material can be receive a parameter considered random. Moreover, some methods are also able to receive a random variable (random force, random unbalance...). It means that a parameter, once assumed deterministic (int or float in python language), now follows a distribution (list or array), like uniform distribution, normal distribution, etc.

    As consequence, plots do not display deterministic results anymore. Instead, plots shows the expectation $E(X_t(t))$ (or mean) for a stochastic process and intervals of confidence (user choice).

    Where:
    - $X_t$ is the stochastic process;
    - $t$ is the index time
    """)
    return


@app.cell
def _():
    import ross as rs
    import ross.stochastic as srs
    from ross.probe import Probe
    import numpy as np

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio
    import plotly.graph_objects as go

    pio.renderers.default = "notebook"
    return Probe, np, rs, srs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Random Sampling

    Arrays of random numbers can be creating using [`numpy.random`](https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html) package.

    `numpy.random` has a large set of distributions that cover most of our needs to run STOCHASTIC ROSS.
    In this [LINK](https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html) you can find a list of numpy random numbers generators.

    When using STOCHASTIC ROSS, **all the randam variables must have the same size**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Classes Name

    It's important to highlight that in STOCHASTIC ROSS, the classes name are the same than ROSS, but with a "**ST_**" prefix to differ.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ST_Material

    There is a class called ST_Material to hold material's properties, where:

    `ST_Material` allows you to create a material with random properties. It creates an object containing a generator with random instances of [`rs.Material`](https://ross-rotordynamics.github.io/ross-website/generated/material/ross.Material.html#ross.Material).

    The instantiation is the same than `rs.Material` class. It has the same parameters and assumptions. The only difference is that you are able to select some parameters to consider as random and instantiate it as a list.

    The parameters which can be passed as random are:
    - `rho` - Density
    - `E` - Young's modulus
    - `G_s` - Shear modulus
    - `Poisson` - Poisson ratio
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    name : str
        Material name.
    rho : float, list, pint.Quantity
        Density (kg/m**3).
        Input a list to make it random.
    E : float, list, pint.Quantity
        Young's modulus (N/m**2).
        Input a list to make it random.
    G_s : float, list
        Shear modulus (N/m**2).
        Input a list to make it random.
    Poisson : float, list
        Poisson ratio (dimensionless).
        Input a list to make it random.
    color : str
        Can be used on plots.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that, to instantiate a ST_Material class, you only need to give 2 out of the following parameters: `E`, `G_s` ,`Poisson`.

    Let's consider that the Young's Modulus is a random variable the follows a uniform distribution from $208e9$ to $211e9$ $N/m^2$.
    """)
    return


@app.cell
def _(np, srs):
    var_size = 5
    _E = np.random.uniform(208000000000.0, 211000000000.0, var_size)
    rand_mat = srs.ST_Material(name='Steel', rho=7810, E=_E, G_s=81200000000.0)
    # Random values for Young's Modulus
    print(rand_mat['E'])
    return (rand_mat,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can return the random Materials created using the following command:
    `iter()`
    It returns a generator with the random objects. It consumes less computational memory and runs loops faster.
    """)
    return


@app.cell
def _(rand_mat):
    list(iter(rand_mat))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can pass one or all parameters as random (but remember the rule of given only 2 out of `E`, `G_s` ,`Poisson`).

    Let's see another example considering all parameters as random.
    """)
    return


@app.cell
def _(np, srs):
    var_size_1 = 5
    _E = np.random.uniform(208000000000.0, 211000000000.0, var_size_1)
    rho = np.random.uniform(7780, 7850, var_size_1)
    G_s = np.random.uniform(79800000000.0, 81500000000.0, var_size_1)
    rand_mat_1 = srs.ST_Material(name='Steel', rho=rho, E=_E, G_s=G_s)
    list(iter(rand_mat_1))
    return (rand_mat_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ST_ShaftElement

    `ST_ShaftElement` allows you to create random shaft element. It creates an object containing a generator with random instances of `ShaftElement`.

    The instantiation is the same than [`rs.ShaftElement`](https://ross-rotordynamics.github.io/ross-website/generated/elements/ross.ShaftElement.html#ross.ShaftElement) class. It has the same parameters and the same beam model and assumptions. The only difference is that you are able to select some parameters to consider as random and instantiate it as a list.

    The parameters which can be passed as random are:
    - `L` - Length
    - `idl` - Inner diameter of the element at the left position
    - `odl` - Outer diameter of the element at the left position
    - `idr` - Inner diameter of the element at the right position
    - `odr` - Outer diameter of the element at the right position.
    - `material` - Shaft material

    The selected parameters must be appended to `is_random` list as string.

    You can return the random shaft element created using the following command:
    `iter()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    L : float, pint.Quantity, list
        Element length.
        Input a list to make it random.
    idl : float, pint.Quantity, list
        Inner diameter of the element at the left position.
        Input a list to make it random.
    odl : float, pint.Quantity, list
        Outer diameter of the element at the left position.
        Input a list to make it random.
    idr : float, pint.Quantity, list, optional
        Inner diameter of the element at the right position
        Default is equal to idl value (cylindrical element)
        Input a list to make it random.
    odr : float, pint.Quantity, list, optional
        Outer diameter of the element at the right position.
        Default is equal to odl value (cylindrical element)
        Input a list to make it random.
    material : ross.material, list of ross.material
        Shaft material.
        Input a list to make it random.
    n : int, optional
        Element number (coincident with it's first node).
        If not given, it will be set when the rotor is assembled
        according to the element's position in the list supplied to
    shear_effects : bool, optional
        Determine if shear effects are taken into account.
        Default is True.
    rotary_inertia : bool, optional
        Determine if rotary_inertia effects are taken into account.
        Default is True.
    gyroscopic : bool, optional
        Determine if gyroscopic effects are taken into account.
        Default is True.
    shear_method_calc : str, optional
        Determines which shear calculation method the user will adopt.
        Default is 'cowper'
    is_random : list
        List of the object attributes to become random.
        Possibilities:
            ["L", "idl", "odl", "idr", "odr", "material"]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cylindrical shaft element with random outer diameter
    If you want to create a cylindrical element with random outer diameter, making sure both `odl` and `odr` are the same, input only `odl` parameter.

    The same logic is applied to inner diameter.
    """)
    return


@app.cell
def _(np, rand_mat_1, srs):
    var_size_2 = 5
    _L = 0.25
    _i_d = 0.0
    _o_d = np.random.uniform(0.04, 0.06, var_size_2)
    _is_random = ['odl', 'material']
    r_s0 = srs.ST_ShaftElement(L=_L, idl=_i_d, odl=_o_d, material=rand_mat_1, shear_effects=True, rotary_inertia=True, gyroscopic=True, is_random=_is_random)
    list(iter(r_s0))
    return (r_s0,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Conical shaft element with random outer diameter
    If you want to create a conical element with random outer diameter, input lists for `odl` ans `odr` parameters.
    """)
    return


@app.cell
def _(np, rand_mat_1, srs):
    var_size_3 = 5
    _L = 0.25
    idl = 0.0
    idr = 0.0
    odl = np.random.uniform(0.04, 0.06, var_size_3)
    odr = np.random.uniform(0.06, 0.07, var_size_3)
    _is_random = ['odl', 'odr', 'material']
    r_s1 = srs.ST_ShaftElement(L=_L, idl=idl, odl=odl, idr=idr, odr=odr, material=rand_mat_1, shear_effects=True, rotary_inertia=True, gyroscopic=True, is_random=_is_random)
    list(iter(r_s1))
    return (var_size_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating a list of shaft elements

    Let's see 2 examples of building rotor shafts:
    - a shaft with 5 shaft elements considered random
    ```
    shaft_elements = [
        ST_ShaftElement,
        ST_ShaftElement,
        ST_ShaftElement,
        ST_ShaftElement,
        ST_ShaftElement,
    ]
    ```
    - a shaft with 5 elements, being only the 3rd element considered as random. So we want;
    ```
    shaft_elements = [
        ShaftElement,
        ShaftElement,
        ST_ShaftElement,
        ShaftElement,
        ShaftElement,
    ]
    ```

    First we create the deterministic shaft elements.
    """)
    return


@app.cell
def _(np, srs, var_size_3):
    from ross.materials import steel
    _L = 0.25
    _N = 5
    _l_list = [_L for _ in range(_N)]
    shaft_elements = [srs.ST_ShaftElement(L=l, idl=0.0, odl=np.random.uniform(0.04, 0.06, var_size_3), material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True, is_random=['odl']) for l in _l_list]
    for i in range(_N):
        print('Element', i)
        print(list(iter(shaft_elements[i])))
    return (steel,)


@app.cell
def _(r_s0, rs, steel):
    _L = 0.25
    _i_d = 0.0
    _o_d = 0.05
    _N = 4
    _l_list = [_L for _ in range(_N)]
    shaft_elements_1 = [rs.ShaftElement(L=l, idl=_i_d, odl=_o_d, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for l in _l_list]
    list(iter(shaft_elements_1))
    shaft_elements_1.insert(2, r_s0)
    list(iter(shaft_elements_1))
    return (shaft_elements_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ST_DiskElement

    This class represents a random Disk element.

    `ST_DiskElement` allows you to create random disk element. It creates an object containing a generator with random instances of [`rs.DiskElement`](https://ross-rotordynamics.github.io/ross-website/generated/elements/ross.DiskElement.html#ross.DiskElement).

    The instantiation is the same than `DiskElement` class. It has the same parameters and assumptions. The only difference is that you are able to select some parameters to consider as random and instantiate it as a list.

    The parameters which can be passed as random are:
    - `m` - mass
    - `Id` - Diametral moment of inertia.
    - `Ip` - Polar moment of inertia

    The selected parameters must be appended to `is_random` list as string.

    You can return the random disk element created using the following command:
    `iter()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    n: int
        Node in which the disk will be inserted.
    m : float, list
        Mass of the disk element.
        Input a list to make it random.
    Id : float, list
        Diametral moment of inertia.
        Input a list to make it random.
    Ip : float, list
        Polar moment of inertia
        Input a list to make it random.
    tag : str, optional
        A tag to name the element
        Default is None
    color : str, optional
        A color to be used when the element is represented.
        Default is '#b2182b' (Cardinal).
    is_random : list
        List of the object attributes to become random.
        Possibilities:
            ["m", "Id", "Ip"]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All the values are following the S.I. convention for the units.
    """)
    return


@app.cell
def _(np, srs, var_size_3):
    _m = np.random.uniform(32.0, 33.0, var_size_3)
    Id = np.random.uniform(0.17, 0.18, var_size_3)
    Ip = np.random.uniform(0.32, 0.33, var_size_3)
    _is_random = ['m', 'Id', 'Ip']
    disk0 = srs.ST_DiskElement(n=2, m=_m, Id=Id, Ip=Ip, is_random=_is_random)
    list(iter(disk0))
    return (disk0,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### From geometry DiskElement instantiation

    Besides the instantiation previously explained, there is a way to instantiate a ST_DiskElement with only geometrical parameters (for cylindrical disks) and the disk’s material, as we can see in the following code.

    Use the classmethod `ST_DiskElement.from_geometry`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    n: int
        Node in which the disk will be inserted.
    material: ross.Material, list of ross.Material
        Disk material.
        Input a list to make it random.
    width: float, list
        The disk width.
        Input a list to make it random.
    i_d: float, list
        Inner diameter.
        Input a list to make it random.
    o_d: float, list
        Outer diameter.
        Input a list to make it random.
    tag : str, optional
        A tag to name the element
        Default is None
    is_random : list
        List of the object attributes to become random.
        Possibilities:
            ["material", "width", "i_d", "o_d"]
    ```
    """)
    return


@app.cell
def _(np, srs, steel, var_size_3):
    _i_d = np.random.uniform(0.05, 0.06, var_size_3)
    _o_d = np.random.uniform(0.35, 0.39, var_size_3)
    disk1 = srs.ST_DiskElement.from_geometry(n=3, material=steel, width=0.07, i_d=_i_d, o_d=_o_d, is_random=['i_d', 'o_d'])
    list(iter(disk1))
    return (disk1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ST_BearingElement

    This class represents a random bearing element.

    `ST_BearingElement` allows you to create random disk element. It creates an object containing a generator with random instances of [`rs.BearingElement`](https://ross-rotordynamics.github.io/ross-website/generated/elements/ross.BearingElement.html#ross.BearingElement).

    The instantiation is the same than `BearingElement` class. It has the same parameters and assumptions. The only difference is that you are able to select some parameters to consider as random and instantiate it as a list.

    If you're considering constant coefficients, use an 1-D array to make it random.
    If you're considering varying coefficients to the frequency, use a 2-D array to make it random

    The parameters which can be passed as random are:
    - `kxx` - Direct stiffness in the x direction.
    - `cxx` - Direct damping in the x direction.
    - `kyy` - Direct stiffness in the y direction.
    - `cyy` - Direct damping in the y direction.
    - `kxy` - Cross coupled stiffness in the x direction.
    - `cxy` - Cross coupled damping in the x direction.
    - `kyx` - Cross coupled stiffness in the y direction.
    - `cyx` - Cross coupled damping in the y direction.

    The selected parameters must be appended to `is_random` list as string.

    You can return the random disk element created using the following command:
    `iter()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
    n: int
        Node which the bearing will be located in
    kxx: float, 1-D array, 2-D array
        Direct stiffness in the x direction.
    cxx: float, 1-D array, 2-D array
        Direct damping in the x direction.
    kyy: float, 1-D array, 2-D array, optional
        Direct stiffness in the y direction.
        (defaults to kxx)
    kxy: float, 1-D array, 2-D array, optional
        Cross coupled stiffness in the x direction.
        (defaults to 0)
    kyx: float, 1-D array, 2-D array, optional
        Cross coupled stiffness in the y direction.
        (defaults to 0)
    cyy: float, 1-D array, 2-D array, optional
        Direct damping in the y direction.
        (defaults to cxx)
    cxy: float, 1-D array, 2-D array, optional
        Cross coupled damping in the x direction.
        (defaults to 0)
    cyx: float, 1-D array, 2-D array, optional
        Cross coupled damping in the y direction.
        (defaults to 0)
    frequency: array, optional
        Array with the frequencies (rad/s).
    tag: str, optional
        A tag to name the element
        Default is None.
    n_link: int, optional
        Node to which the bearing will connect. If None the bearing is
        connected to ground.
        Default is None.
    scale_factor: float, optional
        The scale factor is used to scale the bearing drawing.
        Default is 1.
    is_random : list
        List of the object attributes to become stochastic.
        Possibilities:
            ["kxx", "kxy", "kyx", "kyy", "cxx", "cxy", "cyx", "cyy"]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Bearing with random constant values for each coefficient:
    """)
    return


@app.cell
def _(np, srs):
    var_size_4 = 5
    _kxx = np.random.uniform(1000000.0, 2000000.0, var_size_4)
    _cxx = np.random.uniform(1000.0, 2000.0, var_size_4)
    brg0 = srs.ST_BearingElement(n=0, kxx=_kxx, cxx=_cxx, is_random=['kxx', 'cxx'])
    brg1 = srs.ST_BearingElement(n=5, kxx=_kxx, cxx=_cxx, is_random=['kxx', 'cxx'])
    list(iter(brg0))
    return brg0, brg1, var_size_4


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The coefficients could be an array with different values for different rotation speeds, in that case you only have to give a parameter 'frequency' which is a array with the same size as the coefficients array.

    To make it random, check the example below:
    """)
    return


@app.cell
def _(np, srs, var_size_4):
    _kxx = [np.random.uniform(1000000.0, 2000000.0, var_size_4), np.random.uniform(2300000.0, 3300000.0, var_size_4)]
    _cxx = [np.random.uniform(1000.0, 2000.0, var_size_4), np.random.uniform(2100.0, 3100.0, var_size_4)]
    frequency = np.linspace(500, 800, len(_kxx))
    brg2 = srs.ST_BearingElement(n=1, kxx=_kxx, cxx=_cxx, frequency=frequency, is_random=['kxx', 'cxx'])
    list(iter(brg2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ST_Rotor

    This class will create several instances of [`rs.Rotor`](https://ross-rotordynamics.github.io/ross-website/generated/results/ross.Rotor.html#ross.Rotor) class. The number of rotors to be created depends on the amount of random elements instantiated and theirs respective sizes.

    To use this class, you only have to give all the already instantiated elements in a list format, as it follows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```text
        shaft_elements : list
            List with the shaft elements
        disk_elements : list
            List with the disk elements
        bearing_seal_elements : list
            List with the bearing elements
        point_mass_elements: list
            List with the point mass elements
        tag : str
            A tag for the rotor
    ```
    """)
    return


@app.cell
def _(brg0, brg1, disk0, disk1, shaft_elements_1, srs):
    rotor1 = srs.ST_Rotor(shaft_elements_1, [disk0, disk1], [brg0, brg1])
    return (rotor1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Running the simulation

    After you verify that everything is fine with the rotor, you should
    run the simulation and obtain results.
    To do that you only need to use the one of the `.run_()` methods available.

    For now, STOCHASTIC ROSS has only a few stochastic analysis as shown below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Obtaining results

    These are the following stochastic analysis you can do with the program:

    - `.run_campbell()` - Campbell Diagram
    - `.run_freq_response()` - Frequency response
    - `.run_unbalance_response()` - Unbalance response
    - `.run_time_response()` - Time response

    ## Plotting results

    As it has been spoken before, STOCHASTIC ROSS presents results, not deterministic as ROSS does, but in the form of expectation (mean values) and percentiles (or confidence intervals). When plotting these analysis, it will always display the expectation and you are able to choose which percentile to plot.

    To return a plot, you need to enter the command `.plot()` rigth before the command the run an analysis:
    `.run_something().plot()`

    `.plot()` methods have two main arguments:
    ```text
    percentile : list, optional
        Sequence of percentiles to compute, which must be between
        0 and 100 inclusive.
    conf_interval : list, optional
        Sequence of confidence intervals to compute, which must be between
        0 and 100 inclusive.
    ```

    ### Plot interaction

    You can click on the legend label to ommit an object from the graph.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Campbell Diagram

    This function will calculate the damped natural frequencies for a speed range.

    ```text
    speed_range : array
        Array with the desired range of frequencies.
    frequencies : int, optional
        Number of frequencies that will be calculated.
        Default is 6.
    frequency_type : str, optional
        Choose between displaying results related to the undamped natural
        frequencies ("wn") or damped natural frequencies ("wd").
        The default is "wd".
    ```

    To run the Campbell Diagram, use the command `.run_campbell()`

    To plot the figure, use `.run_campbell().plot()`

    Notice that there're two plots. You can plot both or one of them:
    - damped natural frequency vs frequency;
        - use `.run_campbell().plot_nat_freq()`
    - log dec vs frequency
        - use `.run_campbell().plot_log_dec()`
    """)
    return


@app.cell
def _(np, rotor1):
    samples = 31
    _speed_range = np.linspace(0, 500, samples)
    camp = rotor1.run_campbell(_speed_range, frequencies=7)
    return (camp,)


@app.cell
def _(camp):
    fig1 = camp.plot_nat_freq(conf_interval=[90])
    fig1.show(renderer="notebook")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Frenquency Response

    ```text
    speed_range : array
        Array with the desired range of frequencies.
    inp : int
        Degree of freedom to be excited.
    out : int
        Degree of freedom to be observed.
    modes : list, optional
        Modes that will be used to calculate the frequency response
        (all modes will be used if a list is not given).
    ```

    We can put the frequency response of selecting the input and output degree of freedom.
    - Input is the degree of freedom to be excited;
    - Output is the degree of freedom to be observed.

    Each shaft node has 6 local degrees of freedom (dof) $[x, y, z, \alpha, \beta, \theta]$, and each degree of freedom has it own index:
    - $x$ &rarr; index 0
    - $y$ &rarr; index 1
    - $z$ &rarr; index 2
    - $\alpha$ &rarr; index 3
    - $\beta$ &rarr; index 4
    - $\theta$ &rarr; index 5

    Taking the rotor built as example, let's excite the node 3 (in the $y$ direction) and observe the response on the node 2 (also in $y$ direction):

    $global\_dof = node\_number * dof\_per\_node + dof\_index$

    node 2, local dof $y$:

    $out = 2 * 6 + 1 = 13$

    node 3, local dof $y$:

    $inp = 3 * 6 + 1 = 19$

    To run the Frequency Response, use the command `.run_freq_response()`

    To plot the figure, use the command `run_freq_response().plot()`
    """)
    return


@app.cell
def _(np, rotor1):
    _speed_range = np.linspace(0, 500, 301)
    inp = 3 * rotor1.number_dof + 1
    out = 2 * rotor1.number_dof + 1
    freqresp = rotor1.run_freq_response(inp, out, _speed_range)
    return (freqresp,)


@app.cell
def _(freqresp):
    fig2 = freqresp.plot(conf_interval=[90], mag_kwargs=dict(yaxis=dict(type="log")))
    fig2.show(renderer="notebook")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Unbalance Response

    This method returns the unbalanced response for a mdof system given magnitide and phase of the unbalance, the node where it's applied and a frequency range.

    ```text
    node : list, int
        Node where the unbalance is applied.
    magnitude : list, float
        Unbalance magnitude.
        If node is int, input a list to make make it random.
        If node is list, input a list of lists to make it random.
    phase : list, float
        Unbalance phase.
        If node is int, input a list to make make it random.
        If node is list, input a list of lists to make it random.
    frequency_range : list, float
        Array with the desired range of frequencies.
    ```

    In this analysis, you can enter **magnitude** and **phase** as random variables.

    To run the Unbalance Response, use the command `.run_unbalance_response()`

    To plot the figure, use the command `.run_unbalance_response().plot(probe)`

    Where `probe` is a list of tuples that allows you to choose not only the node where to observe the response, but also the orientation.

    Probe orientation equals 0º refers to `+X` direction (DoFX), and probe orientation equals 90º (or $\frac{\pi}{2} rad$) refers to `+Y` direction (DoFY).

    In this following example, we can obtain the response for a random unbalance(kg.m) with a uniform distribution and its respective phase in a selected node. Notice that it's possible to add multiple unbalances instantiating node, magnitude and phase as lists.

    ```text
    Unbalance: node = 3
               magnitude = np.random.uniform(0.001, 0.002, 10)
               phase = 0
    ```
    """)
    return


@app.cell
def _(np, rotor1):
    freq_range = np.linspace(0, 500, 201)
    n = 3
    _m = np.random.uniform(0.001, 0.002, 10)
    p = 0.0
    results = rotor1.run_unbalance_response(n, _m, p, freq_range)
    return (results,)


@app.cell
def _(Probe, np, results):
    fig3 = results.plot(
        probe=[Probe(3, np.pi / 2)],
        conf_interval=[90],
        mag_kwargs=dict(yaxis=dict(type="log")),
    )
    fig3.show(renderer="notebook")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Time Response

    This function will take a rotor object and plot its time response given a force and a time.
    The **force** and **ic** parameters can be passed as random.

    This function takes the following parameters:
    ```text
    speed: float
        Rotor speed
    force : 2-dimensional array, 3-dimensional array
        Force array (needs to have the same number of rows as time array).
        Each column corresponds to a dof and each row to a time step.
        Inputing a 3-dimensional array, the method considers the force as
        a random variable. The 3rd dimension must have the same size than
        ST_Rotor.rotor_list
    time_range : 1-dimensional array
        Time array.
    ic : 1-dimensional array, 2-dimensional array, optional
        The initial conditions on the state vector (zero by default).
        Inputing a 2-dimensional array, the method considers the
        initial condition as a random variable.
    ```

    To run the Time Response, use the command `.run_time_response()`

    To plot the figure, use the command `.run_time_response().plot()`

    In the following example, let's apply harmonic forces to the node 3 in both directions $x$ and $y$. Also lets analyze the first 10 seconds from the response for a speed of 100.0 rad/s (~955.0 RPM).
    """)
    return


@app.cell
def _(np, rotor1):
    size = 1000
    ndof = rotor1.ndof
    node = 3  # node where the force is applied
    speed = 100.0
    t = np.linspace(0, 10, size)
    F = np.zeros((size, ndof))
    F[:, node * rotor1.number_dof + 0] = 10 * np.cos(2 * t)
    F[:, node * rotor1.number_dof + 1] = 10 * np.sin(2 * t)
    results_1 = rotor1.run_time_response(speed, F, t)
    return node, results_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plotting Time Response 1D, 2D and 3D
    """)
    return


@app.cell
def _(Probe, np, results_1):
    fig4 = results_1.plot_1d(probe=[Probe(3, np.pi / 2)], conf_interval=[90])
    fig4.show(renderer='notebook')
    return


@app.cell
def _(node, results_1):
    fig5 = results_1.plot_2d(node=node, conf_interval=[90])
    fig5.show(renderer='notebook')
    return


@app.cell
def _(results_1):
    fig6 = results_1.plot_3d(conf_interval=[90])
    fig6.show(renderer='notebook')
    return


if __name__ == "__main__":
    app.run()
