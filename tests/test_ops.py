import os
import sys
sys.path.insert(0, r"..//")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

from hotstepper import Step
from hotstepper import Steps
import hotstepper.samples as samples

import warnings
warnings.filterwarnings("ignore")

def test_pow():
    s1 = Step(start=10,end=15,weight=-2)
    s2 = Step(start=12,weight=-1)
    s3 = Step(end=13,weight=2.5)
    s3n = Step(end=13,weight=-2.5)
    s4 = Step(start=14,end=16.5)
    s5 = Step(start=15,weight=2)
    s6 = Step(start=16,weight=2)
    s6n = Step(start=16,weight=-2)
    s7 = Step(start=13.5,end=14.5,weight=2)

    sd1 = Step(start=datetime.datetime(2020,1,14,10,15),end=datetime.datetime(2020,1,16,12,1),weight=-2,use_datetime=True)
    sd2 = Step(start=datetime.datetime(2020,1,10),weight=-1,use_datetime=True)
    sd3 = Step(end=datetime.datetime(2020,1,10),weight=2.5,use_datetime=True)
    sd3n = Step(end=datetime.datetime(2020,1,10),weight=-2.5,use_datetime=True)
    sd4 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),use_datetime=True)
    sd5 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6n = Step(start=datetime.datetime(2020,1,10),weight=-2,use_datetime=True)
    sd7 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),weight=2,use_datetime=True)

    #compare direct and shortcut methods
    assert (s1**2).compare(s1*s1)
    assert (s3**2).compare(s3*s3)
    assert (s3n**2).compare(s3n*s3n)
    assert (s5**2).compare(s5*s5)
    assert (s7**2).compare(s7*s7)
    assert (s6**2).compare(s6*s6)
    assert (s6n**2).compare(s6n*s6n)

    assert (s1**3).compare(s1*s1*s1)
    assert (s3n**3).compare(s3n*s3n*s3n)
    assert (s3**3).compare(s3*s3*s3)
    assert (s5**3).compare(s5*s5*s5)
    assert (s7**3).compare(s7*s7*s7)
    assert (s6**3).compare(s6*s6*s6)
    assert (s6n**3).compare(s6n*s6n*s6n)

    #date version of tests
    assert (sd1**2).compare(sd1*sd1)
    assert (sd3**2).compare(sd3*sd3)
    assert (sd3n**2).compare(sd3n*sd3n)
    assert (sd5**2).compare(sd5*sd5)
    assert (sd7**2).compare(sd7*sd7)
    assert (sd6**2).compare(sd6*sd6)
    assert (sd6n**2).compare(sd6n*sd6n)

    assert (sd1**3).compare(sd1*sd1*sd1)
    assert (sd3n**3).compare(sd3n*sd3n*sd3n)
    assert (sd3**3).compare(sd3*sd3*sd3)
    assert (sd5**3).compare(sd5*sd5*sd5)
    assert (sd7**3).compare(sd7*sd7*sd7)
    assert (sd6**3).compare(sd6*sd6*sd6)
    assert (sd6n**3).compare(sd6n*sd6n*sd6n)


def test_reflect():
    s1 = Step(start=10,end=15,weight=-2)
    s2 = Step(start=12,weight=-1)
    s3 = Step(end=13,weight=2.5)
    s3n = Step(end=13,weight=-2.5)
    s4 = Step(start=14,end=16.5)
    s5 = Step(start=15,weight=2)
    s6 = Step(start=16,weight=2)
    s6n = Step(start=16,weight=-2)
    s7 = Step(start=13.5,end=14.5,weight=2)

    sd1 = Step(start=datetime.datetime(2020,1,14,10,15),end=datetime.datetime(2020,1,16,12,1),weight=-2,use_datetime=True)
    sd2 = Step(start=datetime.datetime(2020,1,10),weight=-1,use_datetime=True)
    sd3 = Step(end=datetime.datetime(2020,1,10),weight=2.5,use_datetime=True)
    sd3n = Step(end=datetime.datetime(2020,1,10),weight=-2.5,use_datetime=True)
    sd4 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),use_datetime=True)
    sd5 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6n = Step(start=datetime.datetime(2020,1,10),weight=-2,use_datetime=True)
    sd7 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),weight=2,use_datetime=True)

    #compare direct and shortcut methods
    assert s1.reflect().compare(s1*-1)
    assert s3n.reflect().compare(s3n*-1)
    assert s3.reflect().compare(s3*-1)
    assert s5.reflect().compare(s5*-1)
    assert s7.reflect().compare(s7*-1)
    assert s6.reflect().compare(s6*-1)
    assert s6n.reflect().compare(s6n*-1)

    #date version of tests
    assert sd1.reflect().compare(sd1*-1)
    assert sd3n.reflect().compare(sd3n*-1)
    assert sd3.reflect().compare(sd3*-1)
    assert sd5.reflect().compare(sd5*-1)
    assert sd7.reflect().compare(sd7*-1)
    assert sd6.reflect().compare(sd6*-1)
    assert sd6n.reflect().compare(sd6n*-1)


    def test_vessel():
        vessel_steps = samples.vessel_queue_sample()

        assert vessel_steps.reflect().compare(vessel_steps*-1)
        assert (vessel_steps**2).compare(vessel_steps*vessel_steps)
        assert (vessel_steps**3).compare(vessel_steps*vessel_steps*vessel_steps)
        assert (vessel_steps**-1).compare(1/vessel_steps)


def test_add():
    s1 = Step(start=10,end=15,weight=-2)
    s2 = Step(start=12,weight=-1)
    s3 = Step(end=13,weight=2.5)
    s3n = Step(end=13,weight=-2.5)
    s4 = Step(start=14,end=16.5)
    s5 = Step(start=15,weight=2)
    s6 = Step(start=16,weight=2)
    s6n = Step(start=16,weight=-2)
    s7 = Step(start=13.5,end=14.5,weight=2)

    sd1 = Step(start=datetime.datetime(2020,1,14,10,15),end=datetime.datetime(2020,1,16,12,1),weight=-2,use_datetime=True)
    sd2 = Step(start=datetime.datetime(2020,1,10),weight=-1,use_datetime=True)
    sd3 = Step(end=datetime.datetime(2020,1,10),weight=2.5,use_datetime=True)
    sd3n = Step(end=datetime.datetime(2020,1,10),weight=-2.5,use_datetime=True)
    sd4 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),use_datetime=True)
    sd5 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6n = Step(start=datetime.datetime(2020,1,10),weight=-2,use_datetime=True)
    sd7 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),weight=2,use_datetime=True)

    #compare direct and shortcut methods
    assert (s1+s1).compare(2*s1)
    assert (s3+s3).compare(2*s3)
    assert (s3n+s3n).compare(2*s3n)
    assert (s5+s5).compare(2*s5)
    assert (s7+s7).compare(2*s7)
    assert (s6+s6).compare(2*s6)
    assert (s6n+s6n).compare(2*s6n)

    assert (s1+s1+s1).compare(3*s1)
    assert (s3+s3+s3).compare(3*s3)
    assert (s3n+s3n+s3n).compare(3*s3n)
    assert (s5+s5+s5).compare(3*s5)
    assert (s7+s7+s7).compare(3*s7)
    assert (s6+s6+s6).compare(3*s6)
    assert (s6n+s6n+s6n).compare(3*s6n)

    #date version of tests
    assert (sd1+sd1).compare(2*sd1)
    assert (sd3+sd3).compare(2*sd3)
    assert (sd3n+sd3n).compare(2*sd3n)
    assert (sd5+sd5).compare(2*sd5)
    assert (sd7+sd7).compare(2*sd7)
    assert (sd6+sd6).compare(2*sd6)
    assert (sd6n+sd6n).compare(2*sd6n)

    assert (sd1+sd1+sd1).compare(3*sd1)
    assert (sd3+sd3+sd3).compare(3*sd3)
    assert (sd3n+sd3n+sd3n).compare(3*sd3n)
    assert (sd5+sd5+sd5).compare(3*sd5)
    assert (sd7+sd7+sd7).compare(3*sd7)
    assert (sd6+sd6+sd6).compare(3*sd6)
    assert (sd6n+sd6n+sd6n).compare(3*sd6n)



def test_sub():
    s1 = Step(start=10,end=15,weight=-2)
    s2 = Step(start=12,weight=-1)
    s3 = Step(end=13,weight=2.5)
    s3n = Step(end=13,weight=-2.5)
    s4 = Step(start=14,end=16.5)
    s5 = Step(start=15,weight=2)
    s6 = Step(start=16,weight=2)
    s6n = Step(start=16,weight=-2)
    s7 = Step(start=13.5,end=14.5,weight=2)

    sd1 = Step(start=datetime.datetime(2020,1,14,10,15),end=datetime.datetime(2020,1,16,12,1),weight=-2,use_datetime=True)
    sd2 = Step(start=datetime.datetime(2020,1,10),weight=-1,use_datetime=True)
    sd3 = Step(end=datetime.datetime(2020,1,10),weight=2.5,use_datetime=True)
    sd3n = Step(end=datetime.datetime(2020,1,10),weight=-2.5,use_datetime=True)
    sd4 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),use_datetime=True)
    sd5 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6 = Step(start=datetime.datetime(2020,1,10),weight=2,use_datetime=True)
    sd6n = Step(start=datetime.datetime(2020,1,10),weight=-2,use_datetime=True)
    sd7 = Step(start=datetime.datetime(2020,1,14),end=datetime.datetime(2020,1,16,12,1),weight=2,use_datetime=True)

    #compare direct and shortcut methods
    assert (s1+s1-s1).compare(s1)
    assert (s3+s3-s3).compare(s3)
    assert (s3n+s3n-s3n).compare(s3n)
    assert (s5+s5-s5).compare(s5)
    assert (s7+s7-s7).compare(s7)
    assert (s6+s6-s6).compare(s6)
    assert (s6n+s6n-s6n).compare(s6n)

    #date version of tests
    assert (sd1+sd1-sd1).compare(sd1)
    assert (sd3+sd3-sd3).compare(sd3)
    assert (sd3n+sd3n-sd3n).compare(sd3n)
    assert (sd5+sd5-sd5).compare(sd5)
    assert (sd7+sd7-sd7).compare(sd7)
    assert (sd6+sd6-sd6).compare(sd6)
    assert (sd6n+sd6n-sd6n).compare(sd6n)