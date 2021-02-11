<p align="left"><img src="https://github.com/TangleSpace/HotStepper/blob/main/docs/images/HotstepperLogo.png?raw=true" title="Hot Stepper" alt="Hot Stepper"></p>

The Hot Stepper library is for exploring datasets via step function expansions.

What the f*&^ is a step function you may ask?, Have you ever seen some stairs?, this is an equal oppotunity package, so you may be in a wheel chair and unable to use stairs in the typical way, so just having seen some stairs will suffix.

Instead of providing a strict mathematical definition that we can all wank off about, how bout just some simple comparisons to warm us up? If you still need to have a wank, feel free to step out (pun intended) anytime.

What is a function? ok, how about just some data we could plot? let's go home school, say we have a vector...oh f&^%, what is that? ok ok, how about just a list of numbers, say y = (1, 1, 2, 3, 5, 8, 13, 21), to keep the wanking impulse alive, we could say that this is a discrete function where we can index the values from left to right with an integer, for example <img src=
"https://render.githubusercontent.com/render/math?math=%5Ctextstyle+y%28x%29+%3D+%281%2C1%2C2%2C3%2C5%2C8%2C13%2C21%29%2C+%7Bx%3A+x%5Cin+%5Cmathbb%7BN%7D%7D%0A" alt="y(x) = (1,1,2,3,5,8,13,21), {x: x\in \mathbb{N}}">, so that we could do something fancy like y(5) = 8, since we are starting at n = 0.

Alright, if we just plot y(n) with straight lines connecting the points, we'd get something like,

```python
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
<p align="left"><img src="https://github.com/TangleSpace/HotStepper/blob/main/docs/images/fibo_line.png?raw=true" title="Fibonacci Plot" alt="Fibonacci Plot"></p>

Or we could get fancy and use step functions to construct the same plot from the fibonacci sequence.

```python
    fibo_deltas = np.diff(list(fibo_sequence(sequence_length)),prepend=0)

    st = Steps().add([Step(i,None,fn) for i, fn in enumerate(fibo_deltas)])
    ax = st.plot()
```
<p align="left"><img src="https://github.com/TangleSpace/HotStepper/blob/main/docs/images/fibo_steps.png?raw=true" title="Fibonacci Step Plot" alt="Fibonacci Step Plot"></p>

Now what if we only start with the rules of the fibonacci sequence, we can generate a step sequence directly.

```python
    def fibo_step_sequence(n):
        f0 = 0
        fn = 1

        for i in range(n):
            yield Step(i,None,fn - f0)
            f0, fn = fn, f0 + fn

    sequence_length = 8
    st = Steps().add(list(fibo_step_sequence(sequence_length)))
    ax = st.plot()

    #Our steps object contains individual step functions, we can iterate over these directly, nice!
    for s in st:
        s.plot(ax=ax,linestyle='-.')
```

<p align="left"><img src="https://github.com/TangleSpace/HotStepper/blob/main/docs/images/fibo_steps_sequence.png?raw=true" title="Fibonacci Step Plot" alt="Fibonacci Step Plot"></p>
