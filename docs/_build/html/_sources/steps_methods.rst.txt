.. _api.Steps:

==============
Steps methods
==============
.. currentmodule:: hotstepper

Basic methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   Steps.copy
   Steps.clear
   Steps.first
   Steps.last
   Steps.series
   Steps.using_datetime
   Steps.step_keys
   Steps.step_values
   Steps.steps


.. _api.plot_functions:

Plotting functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   Steps.plot
   Steps.smooth_plot
   Steps.plot_rolling_step
   Steps.histogram_plot
   Steps.ecdf_plot
   Steps.pacf_plot
   Steps.acf_plot
   Steps.summary


.. _api.class_loader_functions:

Class Loader functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.read_dataframe
   Steps.read_array
   Steps.read_dict

.. _api.instant_loader_functions:

Instance Loader functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.add
   Steps.add_steps
   Steps.add_direct

.. _api.step_functions:
 
Step Functions
~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.step
   Steps.smooth_step
   Steps.fast_step
   Steps.rebase
   Steps.basis

.. _api.arithmetic_operators:
 
Arithmetic operators
~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   Steps.__neg__
   Steps.__add__
   Steps.__sub__
   Steps.__mul__
   Steps.__truediv__
   
.. _api.logical_operators:

Logical operators
~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.normalise
   Steps.invert
   Steps.reflect
   Steps.__eq__
   Steps.__ne__
   Steps.__gt__
   Steps.__lt__
   Steps.__ge__
   Steps.__le__

.. _api.statistical_operators:

Statistical operators
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.covariance
   Steps.correlation
   Steps.span_and_weights

.. _api.summary_statistics:

.. currentmodule:: hotstepper

Summary statistics
~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/
   
   Steps.clip
   Steps.clamp
   Steps.rshift
   Steps.lshift
   Steps.compare