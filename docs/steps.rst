.. _api.Steps:

==============
Steps methods
==============
.. currentmodule:: hotstepper.Steps

Constructor & basic methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/
.. :show-inheritance:

   Steps
   Steps.copy
   Steps.plot
   Steps.step_keys
   Steps.ste_values
   Steps.steps

.. _api.step_functions:
 
Step Functions
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.step
   Steps.smooth_step
   Steps.fast_step


.. _api.arithmetic_operators:
 
Arithmetic operators
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.negate
   Steps.add
   Steps.subtract
   Steps.multiply
   Steps.divide

.. _api.relational_operators:
   
Relational operators
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.compare
   
.. _api.logical_operators:

Logical operators
~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.normalise
   Steps.invert

.. _api.statistical_operators:

Statistical operators
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.cov
   Steps.corr

.. _api.summary_statistics:

Summary statistics
~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.integrate
   Steps.describe
   Steps.min
   Steps.max
   Steps.var
   Steps.std
   Steps.mean
   Steps.median
   Steps.percentile
   Steps.ecdf
   Steps.histogram
   
   
Miscellaneous functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.clip
   Steps.clamp
   Steps.rshift
   Steps.lshift