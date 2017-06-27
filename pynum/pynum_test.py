#!/usr/bin/python
from pprint import pprint
import linear_algebra as la
import stats as st

A = [1, 3, 5, 7, 9]
B = [6, 4, 8, 2, 10]

print("*** Test Module <linear_algebra> ***")
print("*** vector ......")

print("vector A = ", A)
print("vector B = ", B)

C = la.vector_add(A, B)
print("A + B = ", C)

C = la.vector_subtract(A, B)
print("A - B = ", C)

C = la.vector_sum([A, B])
print("A and B summary = ", C)

C = la.scalar_multiply(10, A)
print("10 * A = ", C)

C = la.vector_mean([A, B])
print("A and B mean = ", C)

C = la.dot(A, B)
print("A dot B = ", C)

C = la.sum_of_squares(A)
print("A^2's summary = ", C)

C = la.magnitude(A)
print("A's magnitude = ", C)

C = la.distance(A, B)
print("A's distance = ", C)

print()
print("*** matrix ......")
M = [[1,2,3], [5,6,7], [3,6,9]]
print("M = ", M)

shape = la.shape(M)
print("M's shape = ", shape)

row_1 = la.get_row(M, 1)
print("M[1,:] = ", row_1)

col_1 = la.get_column(M, 1)
print("M[:1] = ", col_1)

I = la.make_matrix(5, 5, la.is_diagonal)
print("identity matrix = ", I)

print("\n\n")
print("*** Test Module <stats> ***")

A = [1, 3, 5, 7, 9, 2, 3, 4, 4, 4, 6, 8, 10, 13, 15, 17]

print("vector A = ", A)
print("sorted A = ", sorted(A))

mean = st.mean(A)
print("A's mean = ", mean)

median = st.median(A)
print("A's median = ", median)

quantile = st.quantile(A, 0.2)
print("A's 20% quantile = ", quantile)

quantile = st.quantile(A, 0.9)
print("A's 90% quantile = ", quantile)

mode = st.mode(A)
print("A's mode = ", mode)

data_range = st.data_range(A)
print("A's range = ", data_range)

variance = st.variance(A)
print("A's variance = ", variance)

standard_deviation = st.standard_deviation(A)
print("A's standard deviation = ", standard_deviation)

interquartile_range = st.interquartile_range(A)
print("A's interquartile range of 25% ~ 75% = ", interquartile_range)

x = [-2, -1, 0, 1, 2]
y = [ 2,  1, 0, 1, 2]

correlation = st.correlation(x, y)
print("correlation = ", correlation)
