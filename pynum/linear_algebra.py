#!/usr/bin/python
from functools import partial, reduce
import math

################################################################
#####                   向量操作                            #####
################################################################

### 向量加法
def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v,w)]

### 向量减法
def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v,w)]

### 多个向量加法，即生成一个新向量,其第一个元素是这一系列向量第一个元素的和,
### 第二个元素是这一系列向量第二个元素的和,以此类推
def vector_sum(vectors):
    return reduce(vector_add, vectors)

### 标量乘以向量
def scalar_multiply(c, v):
    return [c * v_i for v_i in v]

### 计算一系列向量(长度相同)的均值
def vector_mean(vectors):
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

### 点乘(dot product)
### 两个向量的点乘表示对应元素的分量乘积之和
### 另外，点乘衡量了向量 v 在向量 w 方向延伸的程度
def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

### 计算一个向量的平方和
def sum_of_squares(v):
    return dot(v, v)

### 计算向量的大小(或长度)
def magnitude(v):
    return math.sqrt(sum_of_squares(v))

### 计算向量的欧式距离
def distance(v, w):
    return magnitude(vector_subtract(v, w))



################################################################
#####                   矩阵操作                            #####
################################################################

### 获取矩阵的形状
def shape(M):
    num_rows = len(M)
    num_cols = len(M[0]) if M else 0
    return num_rows, num_cols

### 获取矩阵M的第i行
def get_row(M, i):
    return M[i]

### 获取矩阵M的第j列
def get_column(M, j):
    return [M_i[j] for M_i in M]

### 生成矩阵
def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)-th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]

def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0








