import numpy as np

B = np.loadtxt("data/icbm_thick_mat.txt")
G = nx.from_numpy_matrix(B)