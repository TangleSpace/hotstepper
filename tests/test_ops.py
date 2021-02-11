import sys
sys.path.insert(0, r".\\")

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

#from hotstepper.Basis import Basis
from hotstepper.Step import Step
from hotstepper.Steps import Steps
#from hotstepper.analysis.stats import *


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
    assert (s1**2) == (s1*s1)
    assert (s3**2) == (s3*s3)
    assert (s3n**2) == (s3n*s3n)
    assert (s5**2) == (s5*s5)
    assert (s7**2) == (s7*s7)
    assert (s6**2) == (s6*s6)
    assert (s6n**2) == (s6n*s6n)

    assert (s1**3) == (s1*s1*s1)
    assert (s3n**3) == (s3n*s3n*s3n)
    assert (s3**3) == (s3*s3*s3)
    assert (s5**3) == (s5*s5*s5)
    assert (s7**3) == (s7*s7*s7)
    assert (s6**3) == (s6*s6*s6)
    assert (s6n**3) == (s6n*s6n*s6n)

    #date version of tests
    assert (sd1**2) == (sd1*sd1)
    assert (sd3**2) == (sd3*sd3)
    assert (sd3n**2) == (sd3n*sd3n)
    assert (sd5**2) == (sd5*sd5)
    assert (sd7**2) == (sd7*sd7)
    assert (sd6**2) == (sd6*sd6)
    assert (sd6n**2) == (sd6n*sd6n)

    assert (sd1**3) == (sd1*sd1*sd1)
    assert (sd3n**3) == (sd3n*sd3n*sd3n)
    assert (sd3**3) == (sd3*sd3*sd3)
    assert (sd5**3) == (sd5*sd5*sd5)
    assert (sd7**3) == (sd7*sd7*sd7)
    assert (sd6**3) == (sd6*sd6*sd6)
    assert (sd6n**3) == (sd6n*sd6n*sd6n)


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
    assert s1.reflect() == s1*-1
    assert s3n.reflect() == s3n*-1
    assert s3.reflect() == s3*-1
    assert s5.reflect() == s5*-1
    assert s7.reflect() == s7*-1
    assert s6.reflect() == s6*-1
    assert s6n.reflect() == s6n*-1

    #date version of tests
    assert sd1.reflect() == sd1*-1
    assert sd3n.reflect() == sd3n*-1
    assert sd3.reflect() == sd3*-1
    assert sd5.reflect() == sd5*-1
    assert sd7.reflect() == sd7*-1
    assert sd6.reflect() == sd6*-1
    assert sd6n.reflect() == sd6n*-1
