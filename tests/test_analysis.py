import os
import sys
sys.path.insert(0, r"..//")

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

from hotstepper.Step import Step
from hotstepper.Steps import Steps
import hotstepper.samples as samples


vessel_stats = {
    'integrate': 67562.4666666666,
    'nintegrate': 3165.1666666666665,
    'mean': 7.7218513022624045,
    'var': 23.431962388696526,
    'mode': 6.0,
    'median': 7.0,
    'min': 0.0,
    'max': 23.0, 
    'percentile50': 7.0,
    'percentile37': 6.0
}

def test_statistic_values():

    vessel_steps = samples.vessel_queue_sample()

    np.testing.assert_almost_equal(vessel_steps.integrate(), vessel_stats['integrate'])
    np.testing.assert_almost_equal(vessel_steps.normalise().integrate(), vessel_stats['nintegrate'])
    np.testing.assert_almost_equal(vessel_steps.mean(), vessel_stats['mean'])
    np.testing.assert_almost_equal(vessel_steps.var(), vessel_stats['var'])
    np.testing.assert_almost_equal(vessel_steps.mode(), vessel_stats['mode'])
    np.testing.assert_almost_equal(vessel_steps.median(), vessel_stats['median'])
    np.testing.assert_almost_equal(vessel_steps.min(), vessel_stats['min'])
    np.testing.assert_almost_equal(vessel_steps.max(), vessel_stats['max'])
    np.testing.assert_almost_equal(vessel_steps.percentile(50), vessel_stats['percentile50'])
    np.testing.assert_almost_equal(vessel_steps.percentile(37), vessel_stats['percentile37'])
