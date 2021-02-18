import hotstepper.mixins.operations as o
import hotstepper.mixins.read_write as rw

to_add = [o.filter_values]
cl_to_add = [rw.read_array,rw.read_dataframe,rw.read_dict]
st_to_add = [o.apply_reduction_function,o.apply_math_function]


def apply_mixins(cls):
    for a in to_add:
        setattr(cls,a.__name__,a)

def apply_classmethods(cls):
    for a in cl_to_add:
        setattr(cls,a.__name__,classmethod(a))

def apply_staticmethods(cls):
    for a in st_to_add:
        setattr(cls,a.__name__,staticmethod(a))
