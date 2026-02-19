import marimo

__generated_with = "0.19.9"
app = marimo.App(auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Tutorial - Modeling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a basic tutorial on how to use ROSS (rotordynamics open-source software), a Python library for rotordynamic analysis. Most of this code follows object-oriented paradigm, which is represented in this
    [UML DIAGRAM](https://user-images.githubusercontent.com/32821252/50386686-131c5200-06d3-11e9-9806-f5746295be81.png).

    Also [**ROSS GPT**](https://bit.ly/rossgpt), is a virtual assistant trained specifically for the ROSS package.

    Before starting the tutorial, it is worth noting some of ROSS' design characteristics.

    First, we can divide the use of ROSS in two steps:
     - Building the model;
     - Calculating the results.

    We can build a model by instantiating elements such as beams (shaft), disks and bearings. These elements are all defined in classes with names such as `ShaftElement`, `BearingElement` and so on.

    After instantiating some elements, we can then use these to build a rotor.

    This tutorial is about building your **rotor model**. First, you will learn how to create and assign **materials**, how to instantiate the **elements** which compose the rotor and how to convert **units** in ROSS with [pint](https://pint.readthedocs.io/en/stable/) library. This means that every time we call a function, we can use pint.Quantity as an argument for values that have units. If we give a float to the function ROSS will consider SI units as default.

    In the following topics, we will discuss the most relevant classes for a quick start on how to use ROSS.
    """)
    return


@app.cell
def _():
    from pathlib import Path
    # import ross as rs
    import numpy as np

    # Make sure the default renderer is set to 'notebook' for inline plots in Jupyter
    import plotly.io as pio

    pio.renderers.default = "notebook"
    return Path, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 1: Material Class

    There is a class called Material to hold material's properties. Materials are applied to shaft and disk elements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.1 Creating a material

    To instantiate a Material class, you only need to give 2 out of
    the following parameters: `E` (Young's Modulus), `G_s` (Shear
    Modulus) ,`Poisson` (Poisson Coefficient), and the material
    density `rho`.
    """)
    return


@app.cell
def _(rs):
    # from E and G_s
    steel = rs.Material(name="Steel", rho=7810, E=211e9, G_s=81.2e9)
    # from E and Poisson
    steel2 = rs.Material(name="Steel", rho=7810, E=211e9, Poisson=0.3)
    # from G_s and Poisson
    steel3 = rs.Material(name="Steel", rho=7810, G_s=81.2e9, Poisson=0.3)

    print(steel)

    # returning attributes
    print("=" * 36)
    print(f"Young's Modulus: {steel.E}")
    print(f"Shear Modulus:    {steel.G_s}")
    return (steel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note**: Adding 3 arguments to the Material class raises an error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2 Saving materials

    To save an already instantiated Material object, you need to use the following method.
    """)
    return


@app.cell
def _(steel):
    steel.save_material()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.3 Available materials

    Saved Materials are stored in a **.toml file**, which can be read as .txt. The file is placed on ROSS root file with name `available_materials.toml`.

    It's possible to access the Material data from the file. With the file opened, you can:
     - modify the properties directly;
     - create new materials;

    It's important to **keep the file structure** to ensure the correct functioning of the class.

    ```
    [Materials.Steel]
    name = "Steel"
    rho = 7810
    E = 211000000000.0
    Poisson = 0.2992610837438423
    G_s = 81200000000.0
    color = "#525252"
    ```

    **Do not change the dictionary keys and the order they're built**.

    To check what materials are available, use the command:
    """)
    return


@app.cell
def _(rs):
    rs.Material.available_materials()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.4 Loading materials

    After checking the available materials, you should use the `Material.use_material('name')` method with the **name of the material** as a parameter.
    """)
    return


@app.cell
def _(rs):
    steel5 = rs.Material.load_material("Steel")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 2: ShaftElement Class

    `ShaftElement` allows you to create cylindrical and conical shaft elements. It means you can set differents outer and inner diameters for each element node.

    There are some ways in which you can choose the parameters to model this element:

    - Euler–Bernoulli beam Theory (`rotary_inertia=False, shear_effects=False`)
    - Timoshenko beam Theory (`rotary_inertia=True, shear_effects=True` - used as default)

    The matrices (mass, stiffness, damping and gyroscopic) will be defined considering the following local coordinate vector:

    $[x_0, y_0, \alpha_0, \beta_0, x_1, y_1, \alpha_1, \beta_1]^T$
    Where
    $\alpha_0$ and $\alpha_1$ are the bending on the yz plane
    $\beta_0$ and $\beta_1$ are the bending on the xz plane.


    This element represents the rotor's shaft, all the other elements are correlated with this one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1 Creating shaft elements

    The next examples present different ways of how to create a ShaftElement object, from a single element to a list of several shaft elements with different properties.

    When creating shaft elements, you don't necessarily need to input a specific node. If `n=None`, the `Rotor` class will assign a value to the element when building a rotor model (*see section 6*).

    You can also pass the same `n` value to several shaft elements in the same rotor model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.1 Cylindrical shaft element

    As it's been seen, a shaft element has 4 parameters for diameters. To simplify that, when creating a cylindrical element, you only need to give 2 of them: `idl` and `odl`. So the other 2 (`idr` and `odr`) get the same values.

    **Note**: you can give all the 4 parameters, as long they match each other.
    """)
    return


@app.cell
def _(rs, steel):
    # Cylindrical shaft element
    _L = 0.25
    _i_d = 0
    _o_d = 0.05
    cy_elem = rs.ShaftElement(L=_L, idl=_i_d, odl=_o_d, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True)
    print(cy_elem)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.2 Conical shaft element

    To create conical shaft elements, you must give all the 4 diameter parameters, and `idl != idr` and/or `odl != odr`.
    """)
    return


@app.cell
def _(rs, steel):
    # Conical shaft element
    _L = 0.25
    idl = 0
    idr = 0
    odl = 0.05
    odr = 0.07
    co_elem = rs.ShaftElement(L=_L, idl=idl, idr=idr, odl=odl, odr=odr, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True)
    print(co_elem)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Returning element matrices

    Use one of this methods to return the matrices:
    - `.M()`: returns the mass matrix
    - `.K(frequency)`: returns the stiffness matrix
    - `.C(frequency)`: returns the damping matrix
    - `.G()`: returns the gyroscopic matrix
    """)
    return


@app.cell
def _():
    # Mass matrix
    # cy_elem.M()

    # Stiffness matrix
    # frequency = 0
    # cy_elem.K(frequency)

    # Damping matrix
    # frequency = 0
    # cy_elem.C(frequency)

    # Gyroscopic matrix
    # cy_elem.G()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.3 List of elements - identical properties

    Now we learned how to create elements, let's automate the process of creating multiple elements with identical properties.

    In this example, we want 6 shaft elements with identical properties. This process can be done using a `for` loop or a list comprehension.
    """)
    return


@app.cell
def _(rs, steel):
    # Creating a list of shaft elements
    _L = 0.25
    _i_d = 0
    _o_d = 0.05
    _N = 6
    shaft_elements = [rs.ShaftElement(L=_L, idl=_i_d, odl=_o_d, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for _ in range(_N)]
    shaft_elements
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.1.4 List of elements - different properties

    Now we learned how to create elements, let's automate the process of creating multiple elements with different properties.

    In this example, we want 6 shaft elements which properties may not be the same. This process can be done using a `for` loop or a list comprehension, coupled with Python's `zip()` method.

    We create lists for each property, where each term refers to a single element:
    """)
    return


@app.cell
def _(rs, steel):
    _L = [0.2, 0.2, 0.1, 0.1, 0.2, 0.2]
    _i_d = [0.01, 0, 0, 0, 0, 0.01]
    _o_d = [0.05, 0.05, 0.06, 0.06, 0.05, 0.05]
    shaft_elements_1 = [rs.ShaftElement(L=l, idl=idl, odl=odl, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for (l, idl, odl) in zip(_L, _i_d, _o_d)]
    shaft_elements_1
    return


@app.cell
def _(rs, steel):
    _L = [0.2, 0.2, 0.1, 0.1, 0.2, 0.2]
    _i_d = [0.01, 0, 0, 0, 0, 0.01]
    _o_d = [0.05, 0.05, 0.06, 0.06, 0.05, 0.05]
    _N = len(_L)
    shaft_elements_2 = [rs.ShaftElement(L=_L[i], idl=_i_d[i], odl=_o_d[i], material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for i in range(_N)]
    shaft_elements_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Creating shaft elements via Excel

    There is an option for creating a list of shaft elements via an Excel file. The classmethod `.from_table()` reads an Excel file created and converts it to a list of shaft elements.

    A header with the names of the columns is required. These names should match the names expected by the routine (usually the names of the parameters, but also similar ones). The program will read every row bellow the header until they end or it reaches a NaN, which means if the code reaches to an empty line, it stops iterating.

    An example of Excel content can be found at ROSS GitHub repository at *ross/tests/data/shaft_si.xls*, spreadsheet "Model".

    You can load it using the following code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    shaft_file = Path("shaft_si.xls")
    shaft = rs.ShaftElement.from_table(
        file=shaft_file, sheet_type="Model", sheet_name="Model"
    )
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Creating coupling element (CouplingElement Class)

    Here, we introduce the `CouplingElement` class, a subclass of the `ShaftElement` class, designed to model the interaction between two rotor shafts. This element is implemented in a general form in ROSS. The coupling plays a crucial role in mechanical systems by transmitting forces, vibrations, and motion between rotating shafts. It is primarily characterized by adding stiffness, mass, and inertia to the system, which are essential for simulating the real-world behavior of coupled rotors.

    __Steps:__
    - Create two shafts: Start by defining two rotor shafts using the `ShaftElement` class. Each shaft can have its own properties like material, length, and diameter.
    - Join shafts with coupling: Use the `CouplingElement` class to connect the two shafts by inserting the elements in a list following a certain order.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.3.1 Define the shafts with their respective dimensions and properties
    """)
    return


@app.cell
def _(rs, steel):
    # Shaft 1 - Left
    L1 = [300, 92, 200, 200, 92, 300]  # Segment lengths (in mm)
    r1 = [61.5, 75, 75, 75, 75, 61.5]  # Segment radii (in mm)
    shaft1 = [
        rs.ShaftElement(
            L=L1[i] * 1e-3,  # Convert length to meters
            idl=0.0,  # Inner diameter in meters
            odl=r1[i] * 2e-3,  # Outer diameter in meters
            material=steel,  # Material used for the shaft
            shear_effects=True,
            rotary_inertia=True,
            gyroscopic=True,
        )
        for i in range(len(L1))
    ]
    return (shaft1,)


@app.cell
def _(rs, steel):
    # Shaft 2 - Right
    L2 = [80, 200, 200, 640]  # Segment lengths (in mm)
    r2 = [160.5, 160.5, 130.5, 130.5]  # Segment radii (in mm)
    shaft2 = [
        rs.ShaftElement(
            L=L2[i] * 1e-3,  # Convert length to meters
            idl=0.0,  # Inner diameter in meters
            odl=r2[i] * 2e-3,  # Outer diameter in meters
            material=steel,  # Material used for the shaft
            shear_effects=True,
            rotary_inertia=True,
            gyroscopic=True,
        )
        for i in range(len(L2))
    ]
    return (shaft2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.3.2 Define the coupling element that connects the two shafts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this example, only the torsional stiffness is adopted. However, you can pass any of the following arguments (if not provided, the default value is zero):
    - kt_x,
    - kt_y,
    - kt_z (axial stiffness),
    - kr_x,
    - kr_y,
    - kr_z (torsional stiffness),

    considering that the stiffness matrix $\mathbf{K}$ will be assembled like this:

    \begin{equation}
    \mathbf{K} =
    \begin{bmatrix}
    k_{t_x} & 0 & 0 & 0 & 0 & 0 & -k_{t_x} & 0 & 0 & 0 & 0 & 0 \\
    0 & k_{t_y} & 0 & 0 & 0 & 0 & 0 & -k_{t_y} & 0 & 0 & 0 & 0 \\
    0 & 0 & k_{t_z} & 0 & 0 & 0 & 0 & 0 & -k_{t_z} & 0 & 0 & 0 \\
    0 & 0 & 0 & k_{r_x} & 0 & 0 & 0 & 0 & 0 & -k_{r_x} & 0 & 0 \\
    0 & 0 & 0 & 0 & k_{r_y} & 0 & 0 & 0 & 0 & 0 & -k_{r_y} & 0 \\
    0 & 0 & 0 & 0 & 0 & k_{r_z} & 0 & 0 & 0 & 0 & 0 & -k_{r_z} \\
    -k_{t_x} & 0 & 0 & 0 & 0 & 0 & k_{t_x} & 0 & 0 & 0 & 0 & 0 \\
    0 & -k_{t_y} & 0 & 0 & 0 & 0 & 0 & k_{t_y} & 0 & 0 & 0 & 0 \\
    0 & 0 & -k_{t_z} & 0 & 0 & 0 & 0 & 0 & k_{t_z} & 0 & 0 & 0 \\
    0 & 0 & 0 & -k_{r_x} & 0 & 0 & 0 & 0 & 0 & k_{r_x} & 0 & 0 \\
    0 & 0 & 0 & 0 & -k_{r_y} & 0 & 0 & 0 & 0 & 0 & k_{r_y} & 0 \\
    0 & 0 & 0 & 0 & 0 & -k_{r_z} & 0 & 0 & 0 & 0 & 0 & k_{r_z}
    \end{bmatrix}
    \end{equation}

    __Note:__ Although not demonstrated here, the same logic used for stiffness coefficients can also be applied to damping coefficients (ct_x, ct_y, ct_z, cr_x, cr_y, cr_z).
    """)
    return


@app.cell
def _(rs):
    # Mass at each station (e.g., hub mass of the coupling)
    mass_left_station = 151 / 2
    mass_right_station = 151 / 2

    # Polar moment of inertia of the coupling
    Ip = 3.48

    # Torsional stiffness
    torsional_stiffness = 3.04e6

    # Create the coupling element
    coupling = rs.CouplingElement(
        m_l=mass_left_station,  # Mass on the left station (in kg)
        m_r=mass_right_station,  # Mass on the right station (in kg)
        Ip_l=Ip
        / 2,  # Polar moment of inertia on the left station (assuming equal distribution in kg·m²)
        Ip_r=Ip
        / 2,  # Polar moment of inertia on the right station (assuming equal distribution in kg·m²)
        kr_z=torsional_stiffness,  # Torsional stiffness (in N·m/rad)
    )
    coupling
    return (coupling,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 2.3.3 Coupling all elements

    Combine all elements into a single list for the rotor model.
    The elements must be in order.
    """)
    return


@app.cell
def _(coupling, shaft1, shaft2):
    shaft_elements_3 = [*shaft1, coupling, *shaft2]
    shaft_elements_3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 3: DiskElement Class

    The class `DiskElement` allows you to create disk elements, representing rotor equipments which can be considered only to add mass and inertia to the system, disregarding the stiffness.

    ROSS offers 3 (three) ways to create a disk element:
    1. Inputing mass and inertia data
    2. Inputing geometrical and material data
    3. From Excel table
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.1 Creating disk elements from inertia properties

    If you have access to the mass and inertia properties of a equipment, you can input the data directly to the element.

    Disk elements are useful to represent equipments which mass and inertia are significant, but the stiffness can be neglected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 3.1.1 Creating a single disk element

    This example below shows how to instantiate a disk element according to the mass and inertia properties:
    """)
    return


@app.cell
def _(rs):
    disk = rs.DiskElement(n=0, m=32.58, Ip=0.178, Id=0.329, tag="Disk")
    disk
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 3.1.2 Creating a list of disk element

    This example below shows how to create a list of disk element according to the mass and inertia properties. The logic is the same applied to shaft elements.
    """)
    return


@app.cell
def _(rs):
    # OPTION No.1:
    # Using zip() method
    _n_list = [2, 4]
    _m_list = [32.6, 35.8]
    _Id_list = [0.17808928, 0.17808928]
    _Ip_list = [0.32956362, 0.38372842]
    _disk_elements = [rs.DiskElement(n=_n, m=m, Id=Id, Ip=Ip) for (_n, m, Id, Ip) in zip(_n_list, _m_list, _Id_list, _Ip_list)]
    _disk_elements
    return


@app.cell
def _(rs):
    # OPTION No.2:
    # Using list index
    _n_list = [2, 4]
    _m_list = [32.6, 35.8]
    _Id_list = [0.17808928, 0.17808928]
    _Ip_list = [0.32956362, 0.38372842]
    _N = len(_n_list)
    _disk_elements = [rs.DiskElement(n=_n_list[i], m=_m_list[i], Id=_Id_list[i], Ip=_Ip_list[i]) for i in range(_N)]
    _disk_elements
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.2 Creating disk elements from geometrical properties

    Besides the instantiation previously explained, there is a way to instantiate a DiskElement with only geometrical parameters (an approximation for cylindrical disks) and the disk’s material, as we can see in the following code. In this case, there's a class method (`rs.DiskElement.from_geometry()`) which you can use.

    ROSS will take geometrical parameters (outer and inner diameters, and width) and convert them into mass and inertia data. Once again, considering the disk as a cylinder.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 3.2.1 Creating a single disk element

    This example below shows how to instantiate a disk element according to the geometrical and material properties:
    """)
    return


@app.cell
def _(rs, steel):
    _disk1 = rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.28)
    print(_disk1)
    print('=' * 76)
    print(f'Disk mass:              {_disk1.m}')
    print(f'Disk polar inertia:     {_disk1.Ip}')
    print(f'Disk diametral inertia: {_disk1.Id}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 3.2.2 Creating a list of disk element

    This example below shows how to create a list of disk element according to the geometrical and material properties. The logic is the same applied to shaft elements.
    """)
    return


@app.cell
def _(rs, steel):
    # OPTION No.1:
    # Using zip() method
    _n_list = [2, 4]
    _width_list = [0.7, 0.7]
    _i_d_list = [0.05, 0.05]
    _o_d_list = [0.15, 0.18]
    _disk_elements = [rs.DiskElement.from_geometry(n=_n, material=steel, width=width, i_d=_i_d, o_d=_o_d) for (_n, width, _i_d, _o_d) in zip(_n_list, _width_list, _i_d_list, _o_d_list)]
    _disk_elements
    return


@app.cell
def _(rs, steel):
    # OPTION No.2:
    # Using list index
    _n_list = [2, 4]
    _width_list = [0.7, 0.7]
    _i_d_list = [0.05, 0.05]
    _o_d_list = [0.15, 0.18]
    _N = len(_n_list)
    _disk_elements = [rs.DiskElement.from_geometry(n=_n_list[i], material=steel, width=_width_list[i], i_d=_i_d_list[i], o_d=_o_d_list[i]) for i in range(_N)]
    _disk_elements
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3.3 Creating disk elements via Excel

    The third option for creating disk elements is via an Excel file. The classmethod `.from_table()` reads an Excel file created and converts it to a list of disk elements. This method accepts **only mass and inertia** inputs.

    A header with the names of the columns is required. These names should match the names expected by the routine (usually the names of the parameters, but also similar ones). The program will read every row bellow the header until they end or it reaches a NaN, which means if the code reaches to an empty line, it stops iterating.

    You can take advantage of the excel file used to assemble shaft elements, to assemble disk elements, just add a new spreadsheet to your Excel file and specify the correct `sheet_name`.

    An example of Excel content can be found at diretory *ross/tests/data/shaft_si.xls*, spreadsheet "More".
    """)
    return


@app.cell
def _(Path, rs):
    _file_path = Path('shaft_si.xls')
    _list_of_disks = rs.DiskElement.from_table(file=_file_path, sheet_name='More')
    _list_of_disks
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 4: Bearing and Seal Classes

    ROSS has a series of classes to represent elements that add stiffness and / or damping to a rotor system.
    They're suitable to represent mainly bearings, supports and seals. Each one aims to represent some types of bearing and seal.

    All the classes will return four stiffness coefficients ($k_{xx}$, $k_{xy}$, $k_{yx}$, $k_{yy}$) and four damping coefficients ($c_{xx}$, $c_{xy}$, $c_{yx}$, $c_{yy}$), which will be used to assemble the stiffness and damping matrices.

    The main difference between these classes are the arguments the user must input to create the element.

    Available bearing classes and class methods:

    - 1. `BearingElement`: represents a general (journal) bearing element.
    - 2. `SealElement`: represents a general seal element.
    - 3. `BallBearingElement`: A bearing element for ball bearings
    - 4. `RollerBearingElement`: A bearing element for roller bearings.
    - 5. `MagneticBearingElement`: A bearing element for magnetic bearings.
        - 5.1. `param_to_coef`: A bearing element for magnetic bearings from electromagnetic parameters
    - 6. `PlainJournal`: A cylindrical bearing element based on the pressure and temperature field in oil film.

    The classes from item 2 to 6 inherit from `BearingElement` class. It means, you can use the same methods and commands, set up to `BearingElement`, in the other classes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1 BearingElement Class

    This class will create a bearing element. Bearings are elements that only add stiffness and damping properties to the rotor system. These parameters are defined by 8 dynamic coefficients (4 stiffness coefficients and 4 damping coefficients).

    Parameters can be a constant value or speed dependent. For speed dependent parameters, each argument should be passed as an array and the correspondent speed values should also be
    passed as an array. Values for each parameter will be interpolated for the speed.

    Bearing elements are single node elements and linked to "ground", but it's possible to create a new node with `n_link` argument to introduce a link with other elements. Useful to add bearings in series or co-axial rotors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 4.1.1 Bearing with constant coefficients

    Bearings can have a constant value for each coefficient. In this case, it's **not necessary** to give a value to `frequency` argument.

    The next example shows how to instantiate a **single bearing with constant coefficients**:
    """)
    return


@app.cell
def _(rs):
    _stfx = 1000000.0
    _stfy = 800000.0
    _bearing1 = rs.BearingElement(n=0, kxx=_stfx, kyy=_stfy, cxx=1000.0)
    print(_bearing1)
    print('=' * 55)
    print(f'Kxx coefficient: {_bearing1.kxx}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 4.1.2 Bearing with varying coefficients

    The coefficients could be an array with different values for different rotation speeds, in that case you only have to give a parameter 'frequency' which is a array with the same size as the coefficients array.

    The next example shows how to instantiate a **single bearing with speed dependent parameters**:
    """)
    return


@app.cell
def _(np, rs):
    bearing2 = rs.BearingElement(
        n=0,
        kxx=np.array([0.5e6, 1.0e6, 2.5e6]),
        kyy=np.array([1.5e6, 2.0e6, 3.5e6]),
        cxx=np.array([0.5e3, 1.0e3, 1.5e3]),
        frequency=np.array([0, 1000, 2000]),
    )

    print(bearing2)
    print("=" * 79)
    print(f"Kxx coefficient: {bearing2.kxx}")
    return (bearing2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the size of coefficient and frequency arrays do not match, an `ValueError` is raised

    The next example shows the instantiate of a **bearing with odd parameters**:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    bearing_odd = rs.BearingElement( # odd dimensions
        n=0,
        kxx=np.array([0.5e6, 1.0e6, 2.5e6]),
        kyy=np.array([1.5e6, 2.0e6, 3.5e6]),
        cxx=np.array([0.5e3, 1.0e3, 1.5e3]),
        frequency=np.array([0, 1000, 2000, 3000])
    )
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 4.1.3 Inserting bearing elements in series

    Bearing and seal elements are 1-node element, which means the element attaches to a given node from the rotor shaft and it's connect to the "ground". However, there's an option to couple multiple elements in series, using the `n_link` argument. This is very useful to simulate structures which support the machine, for example.

    `n_link` opens a new node to the rotor system, or it can be associated to another rotor node (useful in co-axial rotor models). Then, the new BearingElement node, is set equal to the `n_link` from the previous element.
    """)
    return


@app.cell
def _(rs):
    _stfx = 1000000.0
    _stfy = 800000.0
    bearing3 = rs.BearingElement(n=0, kxx=_stfx, kyy=_stfy, cxx=1000.0, n_link=1, tag='journal_bearing')
    bearing4 = rs.BearingElement(n=1, kxx=10000000.0, kyy=1000000000.0, cxx=10, tag='support')
    print(bearing3)
    print(bearing4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 4.1.4 Visualizing coefficients graphically

    If you want to visualize how the coefficients varies with speed, you can select a specific coefficient and use the `.plot()` method.

    Let's return to the example done in **4.1.2** and check how $k_{yy}$ and $c_{yy}$ varies. You can check for all the 8 dynamic coefficients as you like.
    """)
    return


@app.cell
def _(bearing2):
    bearing2.plot("kyy")
    return


@app.cell
def _(bearing2):
    bearing2.plot(["kxx", "kyy"])
    return


@app.cell
def _(bearing2):
    bearing2.plot("cyy")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.2 SealElement Class

    `SealElement` class method have the exactly same arguments than `BearingElement`. The differences are found in some considerations when assembbling a full rotor model. For example, a SealElement won't generate reaction forces in a static analysis. So, even they are very similar when built, they have different roles in the model.

    Let's see an example:
    """)
    return


@app.cell
def _(rs):
    _stfx = 1000000.0
    _stfy = 800000.0
    seal = rs.SealElement(n=0, kxx=_stfx, kyy=_stfy, cxx=1000.0, cyy=800.0)
    seal
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.3 BallBearingElement Class

    This class will create a bearing element based on some geometric and constructive parameters of ball bearings. The main difference is that cross-coupling stiffness and damping are not modeled in this case.

    Let's see an example:
    """)
    return


@app.cell
def _(np, rs):
    _n = 0
    n_balls = 8
    d_balls = 0.03
    _fs = 500.0
    _alpha = np.pi / 6
    _tag = 'ballbearing'
    ballbearing = rs.BallBearingElement(n=_n, n_balls=n_balls, d_balls=d_balls, fs=_fs, alpha=_alpha, tag=_tag)
    ballbearing
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.4 RollerBearingElement Class

    This class will create a bearing element based on some geometric and constructive parameters of roller bearings. The main difference is that cross-coupling stiffness and damping are not modeled in this case.

    Let's see an example:
    """)
    return


@app.cell
def _(np, rs):
    _n = 0
    n_rollers = 8
    l_rollers = 0.03
    _fs = 500.0
    _alpha = np.pi / 6
    _tag = 'rollerbearing'
    rollerbearing = rs.RollerBearingElement(n=_n, n_rollers=n_rollers, l_rollers=l_rollers, fs=_fs, alpha=_alpha, tag=_tag)
    rollerbearing
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.5 MagneticBearingElement Class

    This class creates a magnetic bearing element. You can input electromagnetic parameters and PID gains. ROSS converts them to stiffness and damping coefficients. To do it, use the class `MagneticBearingElement()`

    See the following reference for the electromagnetic parameters g0, i0, ag, nw, alpha:
    Book: Magnetic Bearings. Theory, Design, and Application to Rotating Machinery
    Authors: Gerhard Schweitzer and Eric H. Maslen
    Page: 84-95

    From: "Magnetic Bearings. Theory, Design, and Application to Rotating Machinery"
    Authors: Gerhard Schweitzer and Eric H. Maslen
    Page: 354

    Let's see an example:
    """)
    return


@app.cell
def _(rs):
    _n = 0
    g0 = 0.001
    i0 = 1.0
    ag = 0.0001
    nw = 200
    _alpha = 0.392
    kp_pid = 1.0
    kd_pid = 1.0
    k_amp = 1.0
    k_sense = 1.0
    _tag = 'magneticbearing'
    mbearing = rs.MagneticBearingElement(n=_n, g0=g0, i0=i0, ag=ag, nw=nw, alpha=_alpha, kp_pid=kp_pid, kd_pid=kd_pid, k_amp=k_amp, k_sense=k_sense, tag=_tag)
    mbearing
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.6 PlainJournal Class

    This class computes the pressure and temperature fields within the oil film of a cylindrical bearing while also determining the stiffness and damping coefficients. These calculations are based on a wide range of inputs, including bearing geometry, operating conditions, fluid properties, turbulence modeling, and mesh discretization.

    __Class arguments:__
    - Bearing geometry:
    Parameters like axial_length, journal_radius, radial_clearance, etc., define the physical characteristics.
    It supports multiple geometries (circular, lobe, or elliptical).

    - Operational conditions:
    The class accounts for the speed, load, and operating type (e.g., "flooded" or "starvation").

    - Fluid properties:
    Parameters for lubricant type, oil flow, injection pressure, etc., ensure accurate simulation of fluid dynamics under varying conditions.

    - Turbulence model:
    Incorporates turbulence effects using Reynolds numbers and a turbulence scaling factor (delta_turb), which enhances accuracy at higher speeds.

    - Mesh discretization:
    Allows detailed control over numerical simulations by adjusting the number of circumferential and axial elements.

    - Methodology:
    Offers two methods (lund, perturbation) for dynamic coefficient calculation.
    """)
    return


@app.cell
def _(rs):
    cybearing = rs.PlainJournal(
        axial_length=0.263144,
        journal_radius=0.2,
        radial_clearance=1.95e-4,
        elements_circumferential=11,
        elements_axial=3,
        n_pad=2,
        pad_arc_length=176,
        preload=0,
        geometry="circular",
        reference_temperature=50,
        frequency=rs.Q_([900], "RPM"),
        fxs_load=0,
        fys_load=-112814.91,
        groove_factor=[0.52, 0.48],
        lubricant="ISOVG32",
        n=3,
        sommerfeld_type=2,
        initial_guess=[0.1, -0.1],
        method="perturbation",
        operating_type="flooded",
        injection_pressure=0,
        oil_flow=37.86,
        show_coef=False,
        print_result=False,
        print_progress=False,
        print_time=False,
    )
    cybearing
    return (cybearing,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Plot pressure distribution

    You can choose the axial element on which you want to see the pressure distribution on the bearing.
    """)
    return


@app.cell
def _(cybearing):
    # Show pressure distribution on bearing for the first axial element
    cybearing.plot_pressure_distribution(axial_element_index=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.7 Creating bearing elements via Excel

    There's an option for creating bearing elements via an Excel file. The classmethod `.from_table()` reads an Excel file and converts it to a `BearingElement` instance. Differently from creating shaft or disk elements, this method creates only a single bearing element. To create a list of bearing elements, the user should open several spreadsheets in the Excel file and run a list comprehension loop appending each element to the list.

    A header with the names of the columns is required. These names should match the names expected by the routine (usually the names of the parameters, but also similar ones). The program will read every row below the header until they end or it reaches a NaN, which means if the code reaches an empty line, it stops iterating.

    ```text
    n : int
        The node in which the bearing will be located in the rotor.
    file: str
        Path to the file containing the bearing parameters.
    sheet_name: int or str, optional
        Position of the sheet in the file (starting from 0) or its name. If none is passed, it is
        assumed to be the first sheet in the file.
    ```

    An example of Excel content can be found at directory *ross/tests/data/bearing_seal_si.xls*, spreadsheet "XLUserKCM".
    """)
    return


@app.cell
def _(Path, rs):
    # single bearing element
    _file_path = Path('bearing_seal_si.xls')
    bearing = rs.BearingElement.from_table(n=0, file=_file_path)
    bearing
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As `.from_table()` creates only a single bearing, let's see an example how to create multiple elements without typing the same command line multiple times.

    - First, in the EXCEL file, create multiple spreadsheets. Each one must hold the bearing coefficients and frequency data.

    - Then, create a list holding the node numbers for each bearing (respecting the order of the spreadsheets from the EXCEL file).

    - Finally, create a loop which iterates over the the nodes list and the spreadsheet.
    """)
    return


@app.cell
def _():
    # list of bearing elements

    # nodes = list with the bearing elements nodes number
    # file_path = Path("bearing_seal_si.xls")
    # bearings = [rs.BearingElement.from_table(n, file_path, sheet_name=i) for i, n in enumerate(nodes)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 5: PointMass Class

    The `PointMass` class creates a point mass element. This element can be used to link other elements in the analysis. The mass provided can be different on the x and y direction (e.g. different support inertia for x and y directions).

    `PointMass` also keeps the mass, stiffness, damping and gyroscopic matrices sizes consistence. When adding 2 bearing elements in series, it opens a new node with new degrees of freedom (DoF) (*see section 4.1.3*) and expands the stiffness and damping matrices. For this reason, it's necessary to add mass values to those DoF to match the matrices sizes.

    If you input the argument `m`, the code automatically replicate the mass value for both directions "x" and "y".

    Let's see an example of creating point masses:
    """)
    return


@app.cell
def _(rs):
    # inputting m
    p0 = rs.PointMass(n=0, m=2)
    p0.M()  # returns de mass matrices for the element
    return


@app.cell
def _(rs):
    # inputting mx and my
    p1 = rs.PointMass(n=0, mx=2, my=3)
    p1.M()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 6: Rotor Class

    `Rotor` is the main class from ROSS. It takes as argument lists with all elements and assembles the mass, gyroscopic, damping and stiffness global matrices for the system. The object created has several methods that can be used to evaluate the dynamics of the model (they all start with the prefix `.run_`).

    To use this class, you must input all the already instantiated elements in a list format.

    If the shaft elements are not numbered, the class set a number for each one, according to the element's position in the list supplied to the rotor constructor.

    To assemble the matrices, the `Rotor` class takes the local DoF's index from each element (element method `.dof_mapping()`) and calculate the global index
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.1 Creating a rotor model
    Let's create a simple rotor model with $1.5 m$ length with 6 identical shaft elements, 2 disks, 2 bearings in the shaft ends and a support linked to the first bearing. First, we create the elements, then we input them to the `Rotor` class.
    """)
    return


@app.cell
def _(np, rs, steel):
    _n = 6
    shaft_elem = [rs.ShaftElement(L=0.25, idl=0.0, odl=0.05, material=steel, shear_effects=True, rotary_inertia=True, gyroscopic=True) for _ in range(_n)]
    _disk0 = rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28)
    _disk1 = rs.DiskElement.from_geometry(n=4, material=steel, width=0.07, i_d=0.05, o_d=0.28)
    _disks = [_disk0, _disk1]
    _stfx = 1000000.0
    _stfy = 800000.0
    _bearing0 = rs.BearingElement(0, kxx=_stfx, kyy=_stfy, cxx=0, n_link=7)
    _bearing1 = rs.BearingElement(6, kxx=_stfx, kyy=_stfy, cxx=0)
    bearing2_1 = rs.BearingElement(7, kxx=_stfx, kyy=_stfy, cxx=0)
    _bearings = [_bearing0, _bearing1, bearing2_1]
    pm0 = rs.PointMass(n=7, m=30)
    pointmass = [pm0]
    rotor1 = rs.Rotor(shaft_elem, _disks, _bearings, pointmass)
    print('Rotor total mass = ', np.round(rotor1.m, 2))
    print('Rotor center of gravity =', np.round(rotor1.CG, 2))
    rotor1.plot_rotor()
    return (rotor1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.2 Adding new nodes

    You can add new nodes to the model based on a list of their positions by using the method `.add_nodes()`:
    """)
    return


@app.cell
def _(rotor1):
    node_position = [0.42, 1.1]
    rotor1_new = rotor1.add_nodes(node_position)
    rotor1_new.plot_rotor()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.3 Creating a rotor from sections

    An alternative to build rotor models is dividing the rotor in sections. Each section gets the same number of shaft elements.

    There's an important difference in this class method when placing disks and bearings. The argument `n` will refer, not to the element node, but to the section node. So if your model has 3 sections with 4 elements each, there're 4 section nodes and 13 element nodes.

    Let's repeat the rotor model from the last example, but using `.from_section()` class method, without the support.
    """)
    return


@app.cell
def _(np, rs, steel):
    _i_d = 0
    _o_d = 0.05
    i_ds_data = [0, 0, 0]
    # inner diameter of each section
    o_ds_data = [0.05, 0.05, 0.05]
    # outer diameter of each section
    leng_data = [0.5, 0.5, 0.5]
    # length of each section
    material_data = [steel, steel, steel]
    _stfx = 1000000.0
    _stfy = 800000.0
    # material_data = steel
    _bearing0 = rs.BearingElement(n=0, kxx=_stfx, kyy=_stfy, cxx=1000.0)
    _bearing1 = rs.BearingElement(n=3, kxx=_stfx, kyy=_stfy, cxx=1000.0)
    _bearings = [_bearing0, _bearing1]
    # n = 0 refers to the section 0, first node
    _disk0 = rs.DiskElement.from_geometry(n=1, material=steel, width=0.07, i_d=0.05, o_d=0.28)
    _disk1 = rs.DiskElement.from_geometry(n=2, material=steel, width=0.07, i_d=0.05, o_d=0.28)
    # n = 3 refers to the section 2, last node
    _disks = [_disk0, _disk1]
    rotor2 = rs.Rotor.from_section(brg_seal_data=_bearings, disk_data=_disks, idl_data=i_ds_data, leng_data=leng_data, odl_data=o_ds_data, nel_r=4, material_data=steel)
    print('Rotor total mass = ', np.round(rotor2.m, 2))
    # n = 1 refers to the section 1, first node
    print('Rotor center of gravity =', np.round(rotor2.CG, 2))
    # n = 2 refers to the section 2, first node
    rotor2.plot_rotor()
    return (rotor2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.4 Visualizing the rotor model

    It is interesting to plot the rotor to check if the geometry checks with what you wanted to the model. Use the `.plot_rotor()` method to create a plot.

    `nodes` argument is useful when your model has lots of nodes and the visualization of nodes label may be confusing. Set an increment to the plot nodes label

    ROSS uses **PLOTLY** as main plotting library:

    With the Plotly, you can hover the mouse icon over the shaft, disk and point mass elements to check some of their parameters.
    """)
    return


@app.cell
def _(rotor1):
    rotor1.plot_rotor()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's visualize another rotor example with **overlapping shaft elements**:
    """)
    return


@app.cell
def _(Path, rs):
    shaft_file = Path('shaft_si.xls')
    shaft = rs.ShaftElement.from_table(file=shaft_file, sheet_type='Model', sheet_name='Model')
    _file_path = Path('shaft_si.xls')
    _list_of_disks = rs.DiskElement.from_table(file=_file_path, sheet_name='More')
    _bearing1 = rs.BearingElement.from_table(n=7, file='bearing_seal_si.xls')
    bearing2_2 = rs.BearingElement.from_table(n=48, file='bearing_seal_si.xls')
    _bearings = [_bearing1, bearing2_2]
    rotor3 = rs.Rotor(shaft, _list_of_disks, _bearings)
    return (rotor3,)


@app.cell
def _(rotor3):
    node_increment = 5
    rotor3.plot_rotor(nodes=node_increment)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.5 Saving a rotor model

    You can save a rotor model using the method `.save()`. This method saves the each element type and the rotor object in different *.toml* files.

    You just need to input a name and the diretory, where it will be saved. If you don't input a file_path, the rotor model is saved inside the "ross" folder.

    To save the `rotor2` we can use:
    """)
    return


@app.cell
def _(rotor2):
    rotor2.save("rotor2.toml")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.6 Loading a rotor model

    You can load a rotor model using the method `.load()`. This method loads a previously saved rotor model.

    You just need to input the file path to the method.

    Now, let's load the `rotor2` we saved before:
    """)
    return


@app.cell
def _(rotor2, rs):
    rotor2_1 = rs.Rotor.load("rotor2.toml")
    rotor2_1 == rotor2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6.7 Using CouplingElement as lumped-element

    Shafts can be connected using the `CouplingElement` class, which can also function as a lumped-element model.
    For instance, a motor can be represented using a `CouplingElement` by specifying its stiffness, mass, and polar moment of inertia.

    Here's an example:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 6.7.1 Creating coupling element
    """)
    return


@app.cell
def _(rs):
    ktc = 3042560.0  # Torsional stiffness
    Ipc = 3.47888
    mc = 151.55
    coupling_1 = rs.CouplingElement(m_l=mc / 2, m_r=mc / 2, Ip_l=Ipc / 2, Ip_r=Ipc / 2, kr_z=ktc, L=0.46, o_d=0.1755, tag='Coupling')  # This parameter is used for visualization purposes
    return Ipc, coupling_1, mc


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 6.7.2 Creating motor as lumped-element
    """)
    return


@app.cell
def _(Ipc, mc, rs):
    ktm = 9.13e6
    Ipm = 156
    mm = mc * Ipm / Ipc

    motor = rs.CouplingElement(
        m_l=mm / 2,
        m_r=mm / 2,
        Ip_l=Ipm / 2,
        Ip_r=Ipm / 2,
        kr_z=ktm,
        L=1,  # This parameter is used for visualization purposes
        tag="Motor",
    )
    return (motor,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 6.7.3 Connecting coupling and motor to the end

    Since `CouplingElement` is a type of `ShaftElement`, it must be inserted into the appropriate position within the `shaft_elements` array.
    """)
    return


@app.cell
def _(coupling_1, motor, rs, steel):
    length = [200.0, 200.0, 200.0, 100.0, 1190.0, 160.0, 160.0, 1190.0, 100.0, 200.0, 200.0, 240.0, 210.0]
    out_diam_left = [160.0, 160.0, 200.0, 200.0, 298.0, 430.0, 430.0, 298.0, 298.0, 200.0, 160.0, 160.0, 140.0]
    out_diam_right = [160.0, 160.0, 200.0, 298.0, 298.0, 430.0, 430.0, 298.0, 200.0, 200.0, 160.0, 160.0, 140.0]
    shaft_elements_4 = [rs.ShaftElement(material=steel, L=_L * 0.001, odl=out_diam_left[_n] * 0.001, odr=out_diam_right[_n] * 0.001, idl=0.0, idr=0.0, alpha=10, beta=0.0001) for (_n, _L) in enumerate(length)]
    shaft_elements_4.append(coupling_1)
    shaft_elements_4.append(motor)
    return (shaft_elements_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 6.7.6 Creating coupled rotor
    """)
    return


@app.cell
def _(rs, shaft_elements_4):
    _disk_elements = [rs.DiskElement(n=6, m=2833.0, Ip=2797.0, Id=1551.0)]
    support_1 = rs.BearingElement(n=1, kxx=271600000.0, kxy=-134900000.0, kyx=-862800000.0, kyy=1811000000.0, cxx=1399000.0, cxy=-2895000.0, cyx=-2887000.0, cyy=15720000.0)
    support_2 = rs.BearingElement(n=11, kxx=294400000.0, kxy=-156200000.0, kyx=-954900000.0, kyy=2066000000.0, cxx=1475000.0, cxy=-3147000.0, cyx=-3137000.0, cyy=17380000.0)
    bearing_elements = [support_1, support_2]
    crotor = rs.Rotor(shaft_elements_4, _disk_elements, bearing_elements)
    crotor.plot_rotor().show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 7: ROSS Units System

    ROSS uses an units system package called [Pint](https://pint.readthedocs.io/en/stable/).

    `Pint` defines, operates and manipulates **physical quantities**: the product of a numerical value and a unit of measurement. It allows arithmetic operations between them and conversions from and to different units.

    With `Pint`, it's possible to define units to every element type available in ROSS and manipulate the units when plotting graphs. ROSS takes the user-defined units and internally converts them to the International System (SI).

    **Important**: It's not possible to manipulate units for attributes from any class. Attributes' values are always returned converted to SI. **Only plot methods** are able to manipulate the output unit.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.1 Inserting units

    Working with `Pint` requires a specific syntax to assign an unit to an argument.

    First of all, it's necessary to import a function called `Q_` from `ross.units`. This function must be assigned to every variable that are desired to have units, followed by a *tuple* containing the magnitude and the unit (in string format).

    The example below shows how to create a material using `Pint`, and how it is returned to the user.
    """)
    return


@app.cell
def _(rs):
    from ross.units import Q_

    rho = Q_(487.56237, "lb/foot**3")  # Imperial System
    E = Q_(211.0e9, "N/m**2")  # International System
    G_s = Q_(81.2e9, "N/m**2")  # International System

    steel4 = rs.Material(name="steel", rho=rho, E=E, G_s=G_s)
    return Q_, steel4


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note**: Taking a closer look to the output values, the material density is converted to the SI and it's returned this way to the user.
    """)
    return


@app.cell
def _(steel4):
    print(steel4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The same syntax applies to elements instantiation, if units are desired. Besides, notice the output is displayed in SI units.

    #### Shaft Element using Pint
    """)
    return


@app.cell
def _(Q_, rs, steel):
    _L = Q_(10, 'in')
    _i_d = Q_(0.0, 'meter')
    _o_d = Q_(0.05, 'meter')
    elem_pint = rs.ShaftElement(L=_L, idl=_i_d, odl=_o_d, material=steel)
    print(elem_pint)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Bearing Element using Pint
    """)
    return


@app.cell
def _(Q_, rs):
    kxx = Q_(2.54e4, "N/in")
    cxx = Q_(1e2, "N*s/m")

    brg_pint = rs.BearingElement(n=0, kxx=kxx, cxx=cxx)
    print(brg_pint)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7.2 Manipulating units for plotting

    The plot methods presents arguments to change the units for each axis. This kind of manipulation does not affect the resulting data stored. It only converts the data on the graphs.

    The arguments names follow a simple logic. It is the "axis name" underscore "units" (axisname_units). It should help the user to identify which axis to modify. For example:

    - frequency_units:
        - "rad/s", "RPM", "Hz"...
    - amplitude_units:
        - "m", "mm", "in", "foot"...
    - displacement_units:
        - "m", "mm", "in", "foot"...
    - rotor_length_units:
        - "m", "mm", "in", "foot"...
    - moment_units:
        - "N/m", "lbf/foot"...

    It's not necessary to add units previously to each element or material to use `Pint` with plots. But keep in mind ROSS will considers results values in the SI units.

    **Note**: If you input data using the Imperial System, for example, without using Pint, ROSS will consider it's in SI if you try to manipulate the units when plotting.

    Let's run a simple example of manipulating units for plotting.
    """)
    return


@app.cell
def _(np, rotor3):
    samples = 31
    speed_range = np.linspace(315, 1150, samples)

    campbell = rotor3.run_campbell(speed_range)
    return (campbell,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plotting with default options will bring graphs with SI units. X and Y axes representing the frequencies are set to `rad/s`
    """)
    return


@app.cell
def _(campbell):
    campbell.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's change the units to `RPM`.

    Just by adding `frequency_units="rpm"` to plot method, you'll change the plot units.
    """)
    return


@app.cell
def _(campbell):
    campbell.plot(frequency_units="RPM")
    return


if __name__ == "__main__":
    app.run()
