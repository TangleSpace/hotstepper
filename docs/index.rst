.. image:: images/HotstepperLogo.png
   :width: 80%
   :alt: hotstepper logo
   :align: center

.. rst-class:: center

Behold! the power of the `Heaviside step function <https://en.wikipedia.org/wiki/Heaviside_step_function>`__ 

.. math::
   :nowrap:
   
    \begin{equation*}
    \theta(t) = \left\{
            \begin{array}{ll}
                0 & \quad t < 0 \\
                1 & \quad t \geq 0
            \end{array}
    \right\}
    \;\;\;\;\; where \;t \in \mathbb{R}
    \end{equation*}


**Date**: |today| **Version**: |release|

.. rst-class:: center

**Repo & Issues**:
`Repository <https://github.com/TangleSpace/hotstepper>`__ |
`Issues & Ideas <https://github.com/TangleSpace/hotstepper/issues>`__ 

.. rst-class:: center

HotStepper is a Numpy based step function analysis and exploration library that trys (not always) to follow general patterns established by Numpy in order to implement step and smoothing functions by way of a linear algebra approach.
Some use cases for the HotStepper package are the analysis of count and discontinuous data (queues, forex, trips etc.). It's all about tools that just work and no need for extensive knowledge of Pandas or Numpy or whatever, just HotStepper. Analysis and exploration should take less code!

**Step Functions**
======================================
.. toctree::
   :maxdepth: 1

   step_functions.rst

**Sequency Analysis**
======================================
.. toctree::
   :maxdepth: 1

   sequency_methods.rst
   sequency.rst

**What do you want to know?**
======================================
.. toctree::
   :maxdepth: 1

   howto recipes.rst
   steps_class.rst
   steps_methods.rst
   basis.rst
   examples.rst

