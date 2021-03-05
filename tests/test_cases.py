import os
import sys
sys.path.insert(0, r"..//")

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hotstepper import Step
from hotstepper import Steps
import hotstepper.samples as samples


temperature_pacf50 = np.array(
        [ 1.00000000e+00,  7.74412727e-01,  7.67161046e-02,  1.90753456e-01,
        1.51168968e-01,  1.30488677e-01,  1.09688278e-01,  1.03180726e-01,
        7.40487586e-02,  7.23424727e-02,  3.66411396e-02,  4.90658557e-02,
        6.03244916e-02,  5.16685714e-02,  3.42923530e-02,  4.87442465e-02,
        3.31770194e-02,  4.15641134e-02,  4.59185605e-02,  1.54721873e-02,
        4.32596130e-02,  2.84461862e-02,  7.95454858e-03, -9.68858639e-03,
        1.54705234e-02,  3.16354586e-02,  2.65901003e-02,  1.30973715e-02,
        4.81855517e-03, -1.41044205e-03, -1.62216408e-04,  1.87945294e-02,
       -2.85904040e-02,  1.73824790e-02,  1.56443066e-02, -2.47659323e-02,
       -3.59706186e-02, -2.12042781e-02,  1.59517272e-02, -2.75139587e-02,
       -2.67181067e-02, -1.99418684e-02, -1.03915680e-02, -2.07944228e-02,
       -9.88643675e-03, -2.82140211e-02, -3.12074096e-02, -4.78243323e-03,
       -2.53289144e-02, -2.39959283e-02,  9.32891083e-04])

temperature_acf50 = np.array(
        [1.0, 0.77468148, 0.63069402, 0.58633114, 0.57870434,
       0.57837778, 0.57635252, 0.57556244, 0.5688385 , 0.56286569,
       0.54900693, 0.54069657, 0.54258273, 0.54472233, 0.53956592,
       0.53807885, 0.53461722, 0.53346538, 0.53607525, 0.52884604,
       0.52890239, 0.52907775, 0.52067092, 0.50444483, 0.4991351 ,
       0.50583768, 0.51125071, 0.50845783, 0.49968989, 0.48962764,
       0.48228194, 0.4838798 , 0.47075989, 0.46978602, 0.47469593,
       0.46340243, 0.44224109, 0.42893111, 0.43552291, 0.4297317 ,
       0.41705745, 0.4068356 , 0.40325828, 0.3972095 , 0.39169704,
       0.38045958, 0.36801452, 0.36649398, 0.35945832, 0.34877278,
       0.34646972])

temperature_hist10y = np.array(
        [0.014524527267744605,
        0.04960263085776934,
        0.15456289394354478,
        0.23622910386406953,
        0.22745957796656352,
        0.18361194847903345,
        0.09509454645108212,
        0.0276788161140038,
        0.008769525897506174,
        0.0021923814743765417,
        0.0002740476842970677])

temperature_hist10x = np.array(
        [-3.55271368e-15,  2.63000000e+00,  5.26000000e+00,  7.89000000e+00,
        1.05200000e+01,  1.31500000e+01,  1.57800000e+01,  1.84100000e+01,
        2.10400000e+01,  2.36700000e+01,  2.63000000e+01])


# def test_temperature_study():
# #     df_temps = pd.read_csv(r'..//data//daily-min-temperatures.csv',parse_dates=['Date'])
# #     temps_steps = Steps.read_dataframe(df_temps,start='Date',weight='Temp',convert_delta=True)

# temp_steps = samples.daily_temperature_sample()
#     gt20_df = df_temps[df_temps.Temp > 20]['Temp'].count()/df_temps['Temp'].count()

#     temps_step20 = temps_steps > 20

#     gt20 =(
#         temps_step20.clamp(lbound=temps_step20.first()-pd.Timedelta(days=1))
#         .normalise()
#         .integrate()/temps_steps.normalise().integrate()
#     )

#     np.testing.assert_almost_equal(gt20,gt20_df)

#     #pacf
#     x,y = temps_steps.pacf(50)
#     np.testing.assert_almost_equal(y,temperature_pacf50)
#     np.testing.assert_almost_equal(x,list(range(51)))

#     #acf
#     x,y = temps_steps.acf(50)
#     np.testing.assert_almost_equal(y,temperature_acf50)
#     np.testing.assert_almost_equal(x,list(range(51)))

#     #histogram, 10 bins
#     x,y = temps_steps.histogram(bins=10)
#     np.testing.assert_almost_equal(y,temperature_hist10y)
#     np.testing.assert_almost_equal(x,temperature_hist10x)


def test_vessel_queue_study():

    vessel_steps = samples.vessel_queue_sample()
    vclip = vessel_steps.clip(lbound=pd.Timestamp(2020,10,10),ubound=pd.Timestamp(2020,11,1))

    vclamp = vessel_steps.clamp(lbound=pd.Timestamp(2020,10,10),ubound=pd.Timestamp(2020,11,1))

    np.testing.assert_almost_equal(vclamp.integrate(),2567.9333333333334)
    np.testing.assert_almost_equal(vclip.integrate(),2554.0)

    assert (not vclamp.compare(vclip))
    assert vclamp.compare(vclip*Step(start=pd.Timestamp(2020,10,10),end=pd.Timestamp(2020,11,1)))

