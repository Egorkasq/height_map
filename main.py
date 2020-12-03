import numpy as np
import matplotlib.pyplot as plt
from plyfile import PlyData, PlyElement
from PIL import Image
import open3d as o3d
from scipy.interpolate import griddata
import cv2


# generate some data

plydata = PlyData.read('odm_mesh.ply')
# print(data)

X = plydata.elements[0].data['x']
Y = plydata.elements[0].data['y']
Z = plydata.elements[0].data['z']
print(X, Y, Z)

X = np.asarray(X)
Y = np.asarray(Y)

X = X.reshape(X.shape[0], 1)
Y = Y.reshape(Y.shape[0], 1)
print(X)

points = np.concatenate((X, Y), axis=1)
values = Z

x_range=((X.max()-X.min()))
y_range=((Y.max()-Y.min()))
grid_x, grid_y = np.mgrid[X.min():X.max():(x_range*1j), Y.min():Y.max():(y_range*1j)]
# points = df[['X','Y']].values
# values = df['new'].values
grid_z0 = griddata(points, values, (grid_x, grid_y), method='linear').astype(np.uint8)
cv2.imwrite('123.jpg', grid_z0)