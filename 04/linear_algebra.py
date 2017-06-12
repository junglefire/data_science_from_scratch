#!/usr/bin/python
import math
from collections import defaultdict, Counter
from functools import partial, reduce
from pprint import pprint

##### 4.1 functions for working with vectors
# 两个向量相加
def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v,w)]

# 两个向量相减
def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v,w)]

# 多个向量求和
def vector_sum(vectors):
    return reduce(vector_add, vectors)

# 标量乘以向量
def scalar_multiply(c, v):
    return [c * v_i for v_i in v]

# 向量均值
def vector_mean(vectors):
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

# 点乘
def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

# 向量的平方
def sum_of_squares(v):
    return dot(v, v)

# 向量的长度
def magnitude(v):
    return math.sqrt(sum_of_squares(v))

def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))

# 两个向量的距离 
def distance(v, w):
   return math.sqrt(squared_distance(v, w))


##### 4.2 矩阵
# 矩阵的形状
def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols

# 获取行
def get_row(A, i):
    return A[i]

# 获取列
def get_column(A, j):
    return [A_i[j] for A_i in A]

# 生成矩阵
def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)-th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]

def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0

# 矩阵加法
def matrix_add(A, B):
    if shape(A) != shape(B):
        raise ArithmeticError("cannot add matrices with different shapes")

    num_rows, num_cols = shape(A)
    def entry_fn(i, j): return A[i][j] + B[i][j]

    return make_matrix(num_rows, num_cols, entry_fn)


##### 测试
if __name__ == "__main__":
    """
    v = [1, 2, 3, 4]
    w = [6, 7, 8, 9]
    u = [3, 4, 5, 6]
    print("v      =", v)
    print("w      =", w)
    print("u      =", u)
    print("v+w    =", vector_add(v, w))
    print("v-w    =", vector_subtract(v, w))
    print("sum()  =", vector_sum([v, w, u]))
    print("7*v    =", scalar_multiply(7, v))
    print("mean() =", vector_mean([v, w, u]))
    print("dot() =", dot(v, w))
    print("dist  =", distance(v, w))
    """
    m1 = [[1,2,3], [4,5,6]]
    m2 = [[3,4,5], [6,7,8]]
    print("m1       =", m1)
    print("m2       =", m2)
    print("m1 shape =", shape(m1))
    print("m1[1:]   =", get_row(m1, 1))
    print("m1[:1]   =", get_column(m1, 1))
    print("m1+m2    =", matrix_add(m1, m2))

    im = make_matrix(5, 5, is_diagonal)
    print("5x5 identity matrix=")
    pprint(im)






