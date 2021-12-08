from __future__ import division

import numpy as np

import matplotlib.pyplot as plt

from PIL import Image
from numpy.linalg import norm
from random import normalvariate
from math import sqrt

img_file = "spideymeme.jpeg"
image = np.array(Image.open(img_file))
image = image / 255
row, col, _ = image.shape
print("pixels: " + str(row) + "*" + str(col))
pixels: 720*1280
fig = plt.figure(figsize=(9,6))
#a = fig.add_subplot(1,1,1)
imgplot = plt.imshow(image)
#a.set_title("Castle Hill, Budapest")
plt.show()

img_r = image[:,:,0]
img_g = image[:,:,1]
img_b = image[:,:,2]
row, col = img_r.shape
print("size: " + str(row) + "*" + str(col))
og_size = image.nbytes
print("Original size of image (bytes): " + str(og_size))

def class_svd(A, epsilon=1e-10):
    m, n = A.shape
    flag = False
    A_square = np.dot(A, A.T)
    #print(A_square)
    e_vals, e_vecs = np.linalg.eig(A_square)
    #print(e_vals)
    #print(e_vecs)
    U = []
    singulars = []
    V = []
    # find singulars
    for i in range(len(e_vals)):
        if e_vals[i] > 0:
            singulars.append(sqrt(e_vals[i]))
        else:
            singulars.append(0)
    # find V
    #if flag:
    #    A_square_V = np.dot(A.T, A)
    #else:
    #    A_square_V = np.dot(A.T, A)
    A_square_V = np.dot(A.T, A)
    e_vals_v, e_vecs_v = np.linalg.eig(A_square_V)
    e_vecs_v = e_vecs_v.T
    for i in range(len(e_vals_v)):
        if e_vals_v[i] < epsilon:
            e_vals_v[i] = 0
    #print(e_vecs_v)
    for i in range(len(e_vals_v)):
        for j in range(len(e_vecs_v[i])):
            if abs(e_vecs_v[i][j]) < epsilon:
                e_vecs_v[i][j] = 0
        V.append(e_vecs_v[i].T)
    #    V.append(e_vecs_v[:,i] / norm(e_vecs_v[:,i]))
    V = np.array(V)
    # find U
    for i in range(len(singulars)):
        U.append(np.dot(A, np.array(e_vecs_v[i]).T) / singulars[i])
    U = np.array(U)
    U = U.T
    sigma = np.zeros(shape= A.shape)
    for i in range(len(singulars)):
        sigma[i][i] = singulars[i]
    return U, sigma, V

def trim(U, sigma, V, k):
    return U[:][:k], sigma[:k][:k], V[:k][:]

k = 50
U_r, d_r, V_r = class_svd(img_r) #np.linalg.svd(img_r, full_matrices=True)
U_g, d_g, V_g = class_svd(img_g) #np.linalg.svd(img_g, full_matrices=True)
U_b, d_b, V_b = class_svd(img_b) #np.linalg.svd(img_b, full_matrices=True)
print(d_r)
U_r_k = U_r[:, 0:k]
V_r_k = V_r[0:k, :]
U_g_k = U_g[:, 0:k]
V_g_k = V_g[0:k, :]
U_b_k = U_b[:, 0:k]
V_b_k = V_b[0:k, :]

d_r_k = d_r[:k]
d_g_k = d_g[:k]
d_b_k = d_b[:k]
d_r_k = d_r_k[:,:k]
d_g_k = d_g_k[:,:k]
d_b_k = d_b_k[:,:k]

row1, col1 = U_r.shape
row2 = d_r.shape
row3, col3 = V_r.shape
print("size: {}, {}, {}, {}, {}".format(row1, col1, row2, row3, col3))
matrix_storage = sum([matrix.nbytes for matrix in [U_r, d_r, V_r, U_g, d_g, V_g, U_b, d_b, V_g]])
print("Size of matrices to store (bytes): " + str(matrix_storage))

img_r_approx = np.dot( 
    np.dot( U_r_k, d_r_k),V_r_k)
img_g_approx = np.dot( np.dot(U_g_k, d_g_k), V_g_k)
img_b_approx = np.dot(np.dot(U_b_k, d_b_k), V_b_k)
reconstructed_img = np.zeros((row,col,3))
reconstructed_img[:,:,0] = img_r_approx
reconstructed_img[:,:,1] = img_g_approx
reconstructed_img[:,:,2] = img_b_approx
reconstructed_img[reconstructed_img < 0] = 0
reconstructed_img[reconstructed_img > 1] = 1
fig = plt.figure(figsize=(9,6))
imgplot = plt.imshow(reconstructed_img)
out = Image.fromarray((reconstructed_img * 255).astype(np.uint8))
out.save( "output.png")
plt.show()
