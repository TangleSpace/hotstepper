import os
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

from matplotlib.testing.compare import compare_images
from hotstepper import Step
from hotstepper import Steps
import hotstepper.samples as samples


def perform_plot_comparison(test_name, fig):

    actual_image, test_image = get_test_images(test_name, fig)
    results = compare_images(actual_image,test_image,tol=0.0001,in_decorator=True)


    if results is not None:
        os.remove(results['diff'])
        print(results['diff'])
        raise AssertionError('{} test failed'.format(test_name))
    else:
        #if the test failed, save the plot for review
        os.remove(test_image)


def get_test_images(test_name, test_fig):
    testplot_file = './basecharts/{}_test.png'.format(test_name)
    test_fig.set_dpi(200.0)
    test_fig.savefig(testplot_file)

    return './basecharts/{}_baseline.png'.format(test_name), testplot_file


def test_multiplots():

    hotel_stays = samples.hotel_stays_sample()

    fig, ax = plt.subplots(nrows=4,figsize=(36,8))

    hcl = hotel_stays.clip(lbound=pd.Timestamp(2016,8,1))
    hcu = hotel_stays.clip(ubound=pd.Timestamp(2016,5,1))

    hcl.plot(ax=ax[0],color='g')
    hcu.plot(ax=ax[0],color='r')

    hcl.smooth_plot(ax=ax[0],color='black',smooth_factor=10**5)
    hcu.smooth_plot(ax=ax[0],color='black',smooth_factor=10**5)

    hotel_stays.plot(ax=ax[1],color='r')
    hotel_stays.smooth_plot(ax=ax[1],color='g',linewidth=5,smooth_factor=10**5)

    step_clip_start = Steps(start=pd.Timestamp(2016,6,1))
    step_clip_end = Steps(end=pd.Timestamp(2016,6,1))

    (hotel_stays*step_clip_start).plot(ax=ax[2])
    (hotel_stays*step_clip_end).plot(ax=ax[3])

    perform_plot_comparison('hotel_multiplots', fig)


def test_filter_plots():

    hotel_stays = samples.hotel_stays_sample()

    ax = hotel_stays.plot(color='g',figsize=(36,6))
    hotel125 = (hotel_stays<50)
    hotel125.plot(ax=ax,color='r')
    ((25+hotel125-25)).plot(ax=ax,color='black')

    fig = ax.get_figure()
    perform_plot_comparison('hotel_filter50', fig)


def test_vessel_multiplots():
    fig,ax = plt.subplots(nrows=5,figsize=(20,12))
    vsteps = samples.vessel_queue_sample()

    v_ul_clip = vsteps.clip(lbound=pd.Timestamp(2020,2,1),ubound=pd.Timestamp(2020,2,10))
    v_ul_clip.plot(ax=ax[1])
    (v_ul_clip>=8).plot(ax=ax[1],color='blue')
    ((v_ul_clip>=8)/v_ul_clip).plot(ax=ax[1],color='red')
    (v_ul_clip>=8).normalise().plot(ax=ax[1],color='black')
    vsteps.clip(lbound=pd.Timestamp(2020,2,1),ubound=pd.Timestamp(2020,5,1)).plot(ax=ax[0],color='r')
    clip_step_end = Steps(end=pd.Timestamp(2020,1,10))
    steps_end = Steps(True).add_direct([None],[pd.Timestamp(2020,1,10)])
    (vsteps*clip_step_end).plot(ax=ax[2],color='black')
    (vsteps*steps_end).plot(ax=ax[2],color='r')
    vsteps.clip(ubound=pd.Timestamp(2020,1,10)).plot(ax=ax[2],color='g')
    vsteps.plot(ax=ax[4])
    vsteps.smooth_plot(ax=ax[4],color='g',linewidth=3)
    vc = vsteps.clip(ubound=pd.Timestamp(2020,1,10))
    vc.plot(ax=ax[3])
    vc7 = vc>9
    vc7.plot(ax=ax[3],color='g')
    vc7.invert(3).plot(ax=ax[3],color='black')

    perform_plot_comparison('vessel_multiplots', fig)


def test_summary_plots():
    vsteps = samples.vessel_queue_sample()
    ax = vsteps.summary()
    fig = ax[0].get_figure()

    perform_plot_comparison('vessel_summary', fig)

    psteps = samples.page_view_sample()
    ax = psteps.summary()
    fig = ax[0].get_figure()

    perform_plot_comparison('pages_summary', fig)

    hsteps = samples.hotel_stays_sample()
    ax = hsteps.summary()
    fig = ax[0].get_figure()

    perform_plot_comparison('hotel_summary', fig)



