import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./streamed.csv')
df['time'] = pd.to_datetime(df['time'])

plt.plot(df['time'], df['factor'])
plt.show()

plt.plot(df['time'], df['pi'])
plt.show()