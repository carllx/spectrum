"""
in data s
in scale s
out rows s
out cols s
out flatten_data s
"""

#### This expects an input mesh that represents an edgenet without junctions and unlooped.
import numpy as np 

rows =len(data)
cols =len(data[0])
data = np.array(data)
data = np.multiply(data, scale)
flatten_data = data.flatten().tolist()

rows = [[rows]]
cols = [[cols]]
flatten_data = [flatten_data]