<p align="left"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/HotstepperLogo.png" title="Hot Stepper" alt="Hot Stepper"></p>

The Hot Stepper library is for exploring datasets via step function expansions.

It's all about tools that just work and no need for extensive knowledge of Pandas or Numpy or whatever, just HotStepper!. Albeit, knowledge of Pandas and Numpy is useful.


<p align="center">
	<a href="https://pepy.tech/project/hotstepper/" alt="PyPI downloads">
        <img src="https://static.pepy.tech/personalized-badge/hotstepper?period=month&units=international_system&left_color=black&right_color=brightgreen&left_text=Downloads" /></a>
    <a href="https://www.python.org/" alt="Python version">
        <img src="https://img.shields.io/pypi/pyversions/hotstepper" /></a>
    <a href="https://pypi.org/project/hotstepper/" alt="PyPI version">
        <img src="https://img.shields.io/pypi/v/hotstepper" /></a>
    <a href="https://hotstepper.mit-license.org/" alt="License">
        <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square"></a>
    <a href='https://hotstepper.readthedocs.io/?badge=latest'>
        <img src='https://readthedocs.org/projects/hotstepper/badge/?version=latest' alt='Documentation Status' />
    </a>
</p>

## Installation

HotStepper can be installed from PyPI:

```bash
pip install hotstepper
```

Conda install coming soon!


## Documentation
Everything (mostly) you want to know about HotStepper and making use in your workflow is here [Read the Docs](https://hotstepper.readthedocs.io/)

## Sample Data Repository
Sample data is located here: <a href="https://github.com/TangleSpace/hotstepper-data">hotstepper-data</a>.
I'd like to thank the Staircase package owner for currating some of these datasets, thanks Riley!

## Step Functions, ah?
<p align="center"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/temperature.gif" title="Daily Temperature" alt="Daily Temperature", width="50%" height="50%"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/store.gif" title="Store" alt="Store", width="50%" height="50%"></p>

What the f*&^ is a step function you may ask?, Have you ever seen some stairs?, this is an equal oppotunity package, so you may be in a wheel chair and unable to use stairs in the typical way, so just having seen some stairs will suffix.

Instead of providing a strict mathematical definition that we can all wank off about, how bout just some simple comparisons to warm us up? If you still need to have a wank, feel free to step out (pun intended) anytime.

What is a function? ok, how about just some data we could plot? let's go home school, say we have a vector...oh f&^%, what is that? ok ok, how about just a list of numbers, say y = (1, 1, 2, 3, 5, 8, 13, 21), to keep the wanking impulse alive, we could say that this is a discrete function where we can index the values from left to right with an integer, for example <img src=
"https://render.githubusercontent.com/render/math?math=%5Ctextstyle+y%28x%29+%3D+%281%2C1%2C2%2C3%2C5%2C8%2C13%2C21%29%2C+%7Bx%3A+x%5Cin+%5Cmathbb%7BN%7D%7D%0A" alt="y(x) = (1,1,2,3,5,8,13,21), {x: x\in \mathbb{N}}">, so that we could do something fancy like y(6) = 8.

Alright, if we just plot y(n) with straight lines connecting the points, we'd get something like,

```python
    import matplotlib.pyplot as plt
    
    def fibo_sequence(n):
        f0 = 0
        fn = 1

        for _ in range(n):
            yield fn
            f0, fn = fn, f0 + fn

    sequence_length = 8
    x = np.arange(0,8,1,dtype=int)
    y = np.array(list(fibo_sequence(sequence_length)),dtype=int)

    fig,ax = plt.subplots()
    ax.plot(x,y)
```
<p align="center"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/fibo_steps.png" title="Fibonacci Step Plot" alt="Fibonacci Step Plot"></p>

Now what if we only start with the rules of the fibonacci sequence, we can generate a step sequence directly.

```python
    import matplotlib.pyplot as plt
    from hotstepper import Step, Steps

    def fibo_step_sequence(n):
        f0 = 0
        fn = 1

        for i in range(n):
            yield Step(start=i+1,weight=(fn - f0))
            f0, fn = fn, f0 + fn

    sequence_length = 8
    st = Steps().add([f for f in fibo_step_sequence(sequence_length)])

    ax = st.plot(method='pretty')
    st.smooth_plot(color='g',ax=ax,smooth_factor=0.3)
    plt.setp(ax, title='Fibo Steps and Components',xlabel='Index', ylabel='Steps Value')

    #Our steps object contains individual step functions, we can iterate over these directly, nice!
    for s in st:
        s.plot(ax=ax)
        s.smooth_plot(ax=ax,linestyle='-.',color='g')
```

<p align="center"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/fibo_steps_sequence.png" title="Fibonacci Step Plot" alt="Fibonacci Step Plot"></p>

A very quick taste of the power that can be tapped with HotStepper. Let's say you have a data set as check-in and check-out times for a hotel. If we need to understand how many people are present in the hotel at any point in time and, as a sample of how HotStepper can help speed your analysis, we can get a quick summary of the dataset with a single line of code.

```python
    import hotstepper.samples as samples

    #Typical work flow, get the data
    hotel_stays = samples.hotel_stays_sample()

    #Explore the data
    hotel_stays.summary()

```

<p align="center"><img src="https://raw.githubusercontent.com/tanglespace/hotstepper/master/docs/images/hotel_summary.png" title="Fibonacci Step Plot" alt="Fibonacci Step Plot"></p>


## Acknowledgments
This project is was inspired by the [Staircase Package](https://github.com/venaturum/staircase), whilst the use cases are similar, HotStepper and Staircase represent different appraoches and each provides pros and cons over the other.
