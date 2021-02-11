import abc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from hotstepper.utilities.helpers import (
    get_epoch_start, steps_plot,
    get_default_plot_color,
    get_default_plot_size,
    prepare_datetime,
    get_epoch_start
)

from hotstepper.analysis.statistics import (
    histogram,
    ecdf
)


class StepsPlottingMixin(metaclass=abc.ABCMeta):
    """
<<<<<<< HEAD
    A plotting mixin class to generate step, smooth, histogram, ecdf and summary plots from any object implementing the AbstractSteps interface.

=======
    A plotting methods mixin class. A number of general and specialised plotting functions to be attached to an onject implementing the AbstractStep interface.
    
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
    """

    def smooth_plot(self,smooth_factor = None,smooth_basis=None, ts_grain = None,ax=None,where='post',**kargs):
        return steps_plot(self,method='smooth',smooth_factor = smooth_factor,smooth_basis=smooth_basis,ts_grain = ts_grain,ax=ax,where=where,**kargs)


    def plot(self,method=None,smooth_factor = None,ts_grain = None,ax=None,where='post',**kargs):
        return steps_plot(self,method=method,smooth_factor = smooth_factor,ts_grain = ts_grain,ax=ax,where=where,**kargs)


    def plot_rolling_step(self,rolling_function=None, window=5, pre_mid_post='mid',ts_grain=None,ax=None,**kargs):
        """
        Plot the result of applying a reduction function to a rolling window across the step values.

        Parameters
        ==============
        rolling_function : Numpy.ufunc, Optional
            A numpy reduction function to apply to the rolling window across the steps data, for example np.mean, np.max.

        widnow : int, Optional
            The size of the rolling window to apply across the steps data.

        pre_mid_post : {'pre','mid','post'}, Optional
            Where to centre the reduction location within the rolling window. Using centre will associate the reduced value with the centre key of the window.

        ax : Matplotlib.Axes
            The plot axis to create the plot on if being created externally.

        ts_grain : Timedelta, Optional
            The delta time precision to use when binning the data if using axis = 1 and the data type is datetime like.

        **kargs : 
            Matplotlib key-value paramters to pass to the plot.

        Returns
        ========
        Matplotlib.Axes

        See Also
        ==============
        ecdf_plot
        histogram_plot
        summary
        
        """

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()
                
            _, ax = plt.subplots(figsize=plot_size)

        if kargs.get('color') is None:
            kargs['color']=get_default_plot_color()

        np_keys = self.step_keys()
        
        # small offset to ensure we plot the initial step transition
        if self.using_datetime():
            ts_grain = pd.Timedelta(minutes=1)
            np_keys = prepare_datetime(np_keys)
        else:
            ts_grain = 0.0000001

        if np_keys[0] == get_epoch_start(self.using_datetime()):
            np_keys[0] = np_keys[1] - ts_grain
        else:
            np_keys[0] = np_keys[0] - ts_grain

        x,y = self.rolling_function_step(np_keys,rolling_function=rolling_function,window=window,pre_mid_post=pre_mid_post)
        ax.plot(x,y,**kargs)

        return ax


    def ecdf_plot(self,ax=None,**kargs):
        """
        Plot an empirical cummulative distribution function of the cummulative step values.

        Parameters
        ==============
        ax : Matplotlib.Axes
            The plot axis to create the plot on if being created externally.

        **kargs : 
            Matplotlib key-value paramters to pass to the plot.

        Returns
        ========
        Matplotlib.Axes    

        See Also
        ==============
        histogram_plot
        summary    
        plot_rolling_step

        References
        ==========
        .. [1] https://en.wikipedia.org/wiki/Empirical_distribution_function

        """

        x,y = ecdf(self)

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()

            _, ax = plt.subplots(figsize=plot_size)

        if kargs.get('drawstyle') is None:
            kargs['drawstyle']='steps'

        if kargs.get('xlabel') is None:
            kargs['xlabel']='Steps Range'

        if kargs.get('title') is None:
            kargs['title']='Step Values Empirical Distribution'

        if kargs.get('color',None) is None:
            kargs['color']= get_default_plot_color()

        ecdf_series = pd.Series(
            data=y,
            index=pd.Index(x)
        )

        ecdf_series.plot(ax=ax, **kargs)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
        return ax


    def histogram_plot(self, bins=20,axis=0,precision=2,ts_grain = None,ax=None,label_style='bins',**kargs):
        """
        Plot a histogram of the cummulative step values.

        Parameters
<<<<<<< HEAD
        ==============
        bins : int, array of ints, Optional
=======
        ------------
        bins : int,array of ints, Optional
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
            How many bins to partition the data into or an array of the specific bin values to partition the data into.

        axis : int, Optional
            The data axis to partition into the bins.
            axis = 0 will parition the y values
            axis = 1 will partition the x values

        precision : int, Optional
            The number of digits the bins labels will display.

        ax : Matplotlib.Axes
            The plot axis to create the plot on if being created externally.

        ts_grain : Timedelta, Optional
            The delta time precision to use when binning the data if using axis = 1 and the data type is datetime like.

        label_style : str, Optional
            The x-axis label style to use on the plot, the available styles are;
            'bins'  -> [8.3, 9.4), number of digits is set by setting the precision paramter.
            'value' -> 8.8, the lower inclusion value of the bin range will be used as the label.

<<<<<<< HEAD
        **kargs : 
=======
        kargs
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
            Matplotlib key-value paramters to pass to the plot.

        Returns
        ========
        Matplotlib.Axes

        See Also
        ==============
        ecdf_plot
        summary
        plot_rolling_step
        
        """

        x,y = histogram(self, bins=bins,axis=axis,ts_grain = ts_grain)

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()

            _, ax = plt.subplots(figsize=plot_size)

        if kargs.get('kind') is None:
            kargs['kind'] = 'bar'

        if kargs.get('xlabel') is None:
            kargs['xlabel']='Steps Range'

        if kargs.get('title') is None:
            kargs['title']='Step Values Histogram'

        if kargs.get('color',None) is None:
            kargs['color']= get_default_plot_color()

        histo_series = pd.Series(
                data=y[1:],
                index=pd.IntervalIndex.from_tuples(
                    [(round(c1,precision), round(c2,precision)) for c1, c2 in zip(x[:-1], x[1:])], closed='left'
                )
            )

        if label_style != 'bins':
            histo_series.index = histo_series.index.left

        histo_series.plot(ax=ax, **kargs)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))

        return ax


    def summary(self, plot_params = {}):
        """
        Plot and display summary details and statistics for the Steps object.

        Plots
        - Steps
        - Smooth steps
        - ECDF
        - Histogram

        Statistics
        Same as Steps.describe()

        Parameters
<<<<<<< HEAD
        ==============
        plot_params : dictionary_like, Optional
            A dictionary to control the look of the plots.
=======
        -------------------------
        plot_params : dictionary_like, Optional
            A dictionary to control the look of the plots. The expected format is:
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
            {'steps_plot': {parameter_name:value, } -> the same as **kargs,
             'smooth_steps_plot': {parameter_name:value, } -> the same as **kargs,
             'ecdf_plot': {parameter_name:value, } -> the same as **kargs,
             'histogram_plot': {parameter_name:value, } -> the same as **kargs}

<<<<<<< HEAD
            example, plot_params = {'steps_plot': {'color': 'green',},
=======
        for example
        -------------------------
            plot_params = {'steps_plot': {'color': 'green',},
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
                            'smooth_steps_plot': {'linewidth': 5, },
                            'ecdf_plot': {'linestyle': ':', },
                            'histogram_plot': {'width': 4}}

        Returns
<<<<<<< HEAD
        ==============
=======
        -------------------------
>>>>>>> f3e81cf1a36eafdefa0d0fed9259d5a332d9794e
            Array of Matplotilib Axes objects 
                [steps_plot_ax,
                ecdf_plot_ax, 
                statistics_table_ax, 
                histogram_plot_ax,
                statistics_table]

        See Also
        ==============
        ecdf_plot
        histogram_plot
        plot_rolling_step

        """
        
        fig = plt.figure(figsize =([22, 12])) 
        gs = gridspec.GridSpec(2, 4)

        axr1 = plt.subplot(gs[0,:3])
        axr21 = plt.subplot(gs[1,0:1])
        axr22 = plt.subplot(gs[1,1:2])
        axr23 = plt.subplot(gs[1,2:3])

        step_params = {'ax':axr1}
        if plot_params.get('steps_plot', None) is not None:
            step_params.update(plot_params.get('steps_plot', None))
        self.plot(**step_params)

        smooth_step_params = {'ax':axr1, 'color':'g','linewidth':3}
        if plot_params.get('smooth_steps_plot', None) is not None:
            smooth_step_params.update(plot_params.get('smooth_steps_plot', None))
        self.smooth_plot(**smooth_step_params)

        histogram_params = {'ax':axr23}
        if plot_params.get('histogram_plot', None) is not None:
            histogram_params.update(plot_params.get('histogram_plot', None))
        self.histogram_plot(**histogram_params)

        ecdf_params = {'ax': axr21}
        if plot_params.get('ecdf_plot', None) is not None:
            ecdf_params.update(plot_params.get('ecdf_plot', None))
        self.ecdf_plot(**ecdf_params)

        axr21.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
        axr23.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))

        axr22.set_axis_off()
        df = self.describe()
    
        table_params = {'loc':'center','cellLoc':'center'}
        add_table_params = plot_params.get('table_plot', None)

        if add_table_params is not None:
            colors = add_table_params.pop('color', None)
            if colors is None:
                colors= get_default_plot_color()
                table_params['colColours'] = [colors] * len(df.columns)
            else:
                table_params['colColours'] = [colors] * len(df.columns)
        else:
            colors= get_default_plot_color()
            table_params['colColours'] = [colors] * len(df.columns)

        if add_table_params is not None:
            table_params.update(add_table_params)
        
        tab = axr22.table(cellText=df.values, colLabels=df.columns, **table_params)
        tab.auto_set_column_width(list(range(len(df.columns))))

        fig.tight_layout()

        return [axr1, axr21,axr22,axr23,tab]
