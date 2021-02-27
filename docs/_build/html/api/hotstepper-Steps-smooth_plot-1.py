st = Step(5,10,3) + Step(6,weight=2)
ax = st.smooth_plot(smooth_factor=2,ts_grain=0.01)
st.plot(ax=ax,color='g')
ax.set_title('Smooth Steps Plot')