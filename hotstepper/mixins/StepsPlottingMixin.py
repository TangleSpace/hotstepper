from abc import ABC
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import seaborn as sns

from hotstepper.utilities.helpers import (
    get_epoch_start, steps_plot,
    get_default_plot_color,
    get_default_plot_size,
    prepare_datetime,
    get_plot_range,
    get_epoch_start
)

from hotstepper.analysis.statistics import (
    histogram,
    ecdf,
    pacf,
    acf
)

colors = ["#9c00ff","#2931b3","#800080","#531cb3", "#5465ff","#835af1"]

# Set your custom color palette
sns.set_palette(sns.color_palette(colors))

class StepsPlottingMixin(ABC):
    """
    A plotting mixin class to generate plots for any object implementing the AbstractSteps interface.

    """

    def smooth_plot(self,smooth_factor = None,smooth_basis=None, interval = 0.01,ax=None,where='post',**kargs):
        """
        Plot a smoothed steps function using different parameters and methods.

        Parameters
        ===========
        smooth_factor : int, float, Optional
            If using the method='smooth' option, set the strength of the smoothing to apply.

        smooth_basis : Basis, Optional
            The `:class: Basis` to use when calculating the smooth steps function.

        interval : int, float, Pandas.Timedetla, Optional
            If using method = 'function' or 'smooth', specify the increment size between step key locations used to calculate the steps function.

        ax : Matplotlib.Axes, Optional
            The axes to plot this chart onto is already defined.

        where : {'pre', 'post', Optional}
            How to draw the step plot, this parameter is the same as the Matplotlib *where* parameter used in the Axes.step plotting function.

        **kargs :
            Matplotlib key-value arguments
            

        Returns
        =========
        Matplotlib.Axes
            A reference to the plot axes object to allow further plotting on the same axes.

        Examples
        ==========

        .. plot::
            :context: close-figs

            st = Step(5,10,3) + Step(6,weight=2)
            ax = st.smooth_plot(smooth_factor=2)
            st.plot(ax=ax,color='g')
            ax.set_title('Smooth Steps Plot')

        """

        return self.plot(method='smooth',smooth_factor = smooth_factor,smooth_basis=smooth_basis,interval = interval,ax=ax,where=where,**kargs)


    def plot(self,method=None,smooth_factor=None,smooth_basis=None,interval = 0.01,ax=None,where='post',**kargs):
        """
        Plot the steps function using different parameters and methods.

        Parameters
        ===========
        method : {'function','smooth','pretty','smooth_function', Optional}
            Specify how the steps should be calculated to generate the plot and the type of plot style.

        smooth_factor : int, float, Optional
            If using the method='smooth' option, set the strength of the smoothing to apply.

        smooth_basis : Basis, Optional
            The `:class: Basis` to use when calculating the smooth steps function.

        interval : int, float, Pandas.Timedetla, Optional
            If using method = 'function' or 'smooth', specify the increment size between step key locations used to calculate the steps function.

        ax : Matplotlib.Axes, Optional
            The axes to plot this chart onto is already defined.

        where : {'pre', 'post', Optional}
            How to draw the step plot, this parameter is the same as the Matplotlib *where* parameter used in the Axes.step plotting function.

        **kargs :
            Matplotlib key-value arguments


        Returns
        =========
        Matplotlib.Axes
            A reference to the plot axes object to allow further plotting on the same axes.

        Examples
        ==========

        .. plot::
            :context: close-figs

            s1 = Step(5,10,3)
            s2 = Step(6,weight=2)
            st = s1 + s2
            ax = s1.plot(color='r',figsize=(8,4))
            s2.plot(ax=ax,method='function')
            s2.plot(ax=ax,method='smooth')
            st.plot(ax=ax)
            st.smooth_plot(ax=ax)

            ax.set_title('Steps Plot')
            
        """

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()
                
            _, ax = plt.subplots(figsize=plot_size)


        np_keys = self.step_keys()
        np_values = self.step_values()

        reverse_step = False

        if len(np_keys) < 3 :
            if len(np_keys) == 0:
                ax.axhline(self(get_epoch_start(self.using_datetime()))[0], **kargs)
                return ax
            else:
                reverse_step = np_keys[0]==get_epoch_start(False)
                np_keys = get_plot_range(self.first(),self.last(),interval,use_datetime=self.using_datetime())
                np_values = self.step(np_keys)

        if method == 'pretty':
            end_index = len(np_keys)
            start_index = 1

            if self.using_datetime():
                offset = pd.Timedelta(minutes=1)
                offset = prepare_datetime(np_keys)
            else:
                offset = 0.0000000001

            if np_keys[0] == get_epoch_start(self.using_datetime()):
                np_keys[0] = np_keys[1] - offset

                np_keys = np.insert(np_keys,0,np_keys[0] - offset)
                np_values = np.insert(np_values,0,0)
                np_keys[0] = np_keys[0] - offset

            step0_k = np_keys[0]
            step0_v = np_values[0]

            for i in range(len(np_keys)):

                k = np_keys[i]
                v = np_values[i]

                ax.hlines(y = step0_v, xmin = step0_k, xmax = k,**kargs)
                ax.vlines(x = k, ymin = step0_v, ymax = v,linestyles=':',**kargs)

                if i > start_index - 1 and i < end_index:
                    if i == start_index:
                        ax.plot(k,v,marker='o',fillstyle='full',**kargs)
                    else:
                        ax.plot(k,step0_v,marker='o',fillstyle='none',**kargs)
                        ax.plot(k,v,marker='o',fillstyle='full',**kargs)
                elif i == end_index:
                    ax.plot(k,step0_v,marker='o',fillstyle='none',**kargs)

                step0_k = k
                step0_v = v

        elif method == 'function':
                tsx = get_plot_range(self.first(),self.last(),interval,use_datetime=self.using_datetime())
                ax.step(tsx,self.step(tsx), where=where, **kargs)
        elif method == 'smooth_function':
                tsx = get_plot_range(self.first(),self.last(),interval,use_datetime=self.using_datetime())
                ax.plot(tsx,self.smooth_step(tsx,smooth_factor = smooth_factor, smooth_basis=smooth_basis), **kargs)
        elif method == 'smooth':
            if np_keys.shape[0] < 20:
                tsx = get_plot_range(self.first(),self.last(),interval,use_datetime=self.using_datetime())
                ax.plot(tsx,self.smooth_step(tsx,smooth_factor = smooth_factor, smooth_basis=smooth_basis), **kargs)
            else:
                # small offset to ensure we plot the initial step transition
                if self.using_datetime():
                    offset = pd.Timedelta(minutes=1)
                    np_keys = prepare_datetime(np_keys)
                else:
                    offset = 0.000000000001
                    
                if np_keys[0] == get_epoch_start(self.using_datetime()):
                    np_keys[0] = np_keys[1] - offset
                elif not reverse_step:
                    np_keys = np.insert(np_keys,0,np_keys[0] - offset)
                    np_values = np.insert(np_values,0,0)
                    np_keys[0] = np_keys[0] - offset

                ax.plot(np_keys,self.smooth_step(np_keys,smooth_factor = smooth_factor, smooth_basis=smooth_basis), **kargs)
        else:
            # small offset to ensure we plot the initial step transition
            if self.using_datetime():
                offset = pd.Timedelta(minutes=1)
                np_keys = prepare_datetime(np_keys)
            else:
                offset = 0.0000000001
            
            if np_keys[0] == get_epoch_start(self.using_datetime()):
                np_keys[0] = np_keys[1] - offset
            elif not reverse_step:
                np_keys = np.insert(np_keys,0,np_keys[0] - offset)
                np_values = np.insert(np_values,0,0)
                np_keys[0] = np_keys[0] - offset


            ax.step(np_keys,np_values, where=where, **kargs)

        return ax


    def plot_rolling_step(self,rolling_function=None, window=5, pre_mid_post='mid',ax=None,**kargs):
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

        **kargs : 
            Matplotlib key-value paramters to pass to the plot.

        Returns
        ========
        Matplotlib.Axes

        See Also
        ==============
        ecdf_plot
        pacf_plot
        histogram_plot
        summary
        
        """

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()
                
            _, ax = plt.subplots(figsize=plot_size)

        #if kargs.get('color') is None:
        #    kargs['color']=get_default_plot_color()

        np_keys = self.step_keys()
        
        # small offset to ensure we plot the initial step transition
        if self.using_datetime():
            offset = pd.Timedelta(minutes=1)
            np_keys = prepare_datetime(np_keys)
        else:
            offset = 0.0000001

        if np_keys[0] == get_epoch_start(self.using_datetime()):
            np_keys[0] = np_keys[1] - offset
        else:
            np_keys[0] = np_keys[0] - offset

        x,y = self.rolling_function_step(np_keys,rolling_function=rolling_function,window=window,pre_mid_post=pre_mid_post)
        ax.plot(x,y,**kargs)

        return ax


    def acf_plot(self,lags=10, minlags=0,ax=None,**kargs):
        """
        Plot an auto-correlation function of the cummulative step values.

        Parameters
        ==============
        lags : int, Optional
            The number of previous steps to perform ACF analysis.

        minlags : int, Optional
            The minimum lag to include.

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
        .. https://en.wikipedia.org/wiki/autocorrelation_function

        """

        x,y = acf(self,lags)

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()

            _, ax = plt.subplots(figsize=plot_size)

        if kargs.get('kind') is None:
            kargs['kind']='bar'

        if kargs.get('xlabel') is None:
            kargs['xlabel']='Lag'

        if kargs.get('title') is None:
            kargs['title']='Steps Autocorrelation for Lags = {}'.format(lags)

        #if kargs.get('color',None) is None:
        #    kargs['color']= get_default_plot_color()

        ecdf_series = pd.Series(
            data=y[minlags:],
            index=pd.Index(x[minlags:])
        )

        ecdf_series.plot(ax=ax, **kargs)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
        return ax


    def pacf_plot(self,lags=10, minlags=0,ax=None,**kargs):
        """
        Plot an partial auto-correlation function of the cummulative step values.

        Parameters
        ==============
        lags : int, Optional
            The number of previous steps to perform PACF analysis.

        minlags : int, Optional
            The minimum lag to include.

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
        .. https://en.wikipedia.org/wiki/Partial_autocorrelation_function

        """

        x,y = pacf(self,lags)

        if ax is None:
            plot_size = kargs.pop('figsize',None)
            if plot_size is None:
                plot_size = get_default_plot_size()

            _, ax = plt.subplots(figsize=plot_size)

        if kargs.get('kind') is None:
            kargs['kind']='bar'

        if kargs.get('xlabel') is None:
            kargs['xlabel']='Lag'

        if kargs.get('title') is None:
            kargs['title']='Steps Partial Autocorrelation for Lags = {}'.format(lags)

        #if kargs.get('color',None) is None:
        #    kargs['color']= get_default_plot_color()

        ecdf_series = pd.Series(
            data=y[minlags:],
            index=pd.Index(x[minlags:])
        )

        ecdf_series.plot(ax=ax, **kargs)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
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
        .. https://en.wikipedia.org/wiki/Empirical_distribution_function

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

        #if kargs.get('color',None) is None:
        #    kargs['color']= get_default_plot_color()

        ecdf_series = pd.Series(
            data=y,
            index=pd.Index(x)
        )

        ecdf_series.plot(ax=ax, **kargs)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
        return ax


    def histogram_plot(self, bins=20,axis=0,precision=2,offset = None,ax=None,label_style='bins',**kargs):
        """
        Plot a histogram of the cummulative step values.

        Parameters
        ==============
        bins : int, array of ints, Optional
            How many bins to partition the data into or an array of the specific bin values to partition the data into.

        axis : int, Optional
            The data axis to partition into the bins.
            axis = 0 will parition the y values
            axis = 1 will partition the x values

        precision : int, Optional
            The number of digits the bins labels will display.

        ax : Matplotlib.Axes
            The plot axis to create the plot on if being created externally.

        offset : Timedelta, Optional
            The delta time precision to use when binning the data if using axis = 1 and the data type is datetime like.

        label_style : str, Optional
            The x-axis label style to use on the plot, the available styles are;
            'bins'  -> [8.3, 9.4), number of digits is set by setting the precision paramter.
            'value' -> 8.8, the lower inclusion value of the bin range will be used as the label.

        **kargs : 
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

        x,y = histogram(self, bins=bins,axis=axis)

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

        #if kargs.get('color',None) is None:
        #    kargs['color']= get_default_plot_color()

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
        ==============
        plot_params : dictionary_like, Optional
            A dictionary to control the look of the plots.
            {
            'steps_plot': {parameter_name:value, } -> the same as kargs,
            'smooth_steps_plot': {parameter_name:value, } -> the same as kargs,
            'ecdf_plot': {parameter_name:value, } -> the same as kargs,
            'histogram_plot': {parameter_name:value, } -> the same as kargs
            }

            example, plot_params =
            {
            'steps_plot': {'color': 'green',},
            'smooth_steps_plot': {'linewidth': 5, },
            'ecdf_plot': {'linestyle': ':', },
            'histogram_plot': {'width': 4}
            }

        Returns
        ==============
        array
            [steps_plot_ax,ecdf_plot_ax, statistics_table_ax, histogram_plot_ax,statistics_table]

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

        smooth_step_params = {'ax':axr1,'linewidth':3}
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
