import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(170, 10, 250)

# plt.hist(x)

plt.hist([1, 2, 1], bins=[0, 1, 2, 3])
plt.show()