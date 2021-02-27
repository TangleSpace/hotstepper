s1 = Step(5,10,3)
s2 = Step(6,weight=2)
st = s1 + s2
ax = s1.plot(color='r')
s2.plot(ax=ax,color='g',method='function')
st.plot(ax=ax)

ax.set_title('Steps Plot')