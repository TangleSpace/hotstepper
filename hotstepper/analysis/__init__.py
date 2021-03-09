import hotstepper.analysis.statistics as s
import hotstepper.analysis.Sequency as Sequency

to_add = [
    s.pacf,
    s.acf,
    s.ecdf,
    s.histogram,
    s.span_and_weights,
    s.mean_integrate,
    s.mean,
    s.var,
    s.std,
    s.integrate,
    s.percentile,
    s.min,
    s.max,
    s.mode,
    s.median,
    s.covariance,
    s.correlation,
    s.describe,
    s.rolling_function_step
]

def apply_mixins(cls):
    for a in to_add:
        setattr(cls,a.__name__,a)

