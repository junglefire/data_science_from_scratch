#!/usr/bin/python
import sys
sys.path.append('../pynum')

import matplotlib.pyplot as plt
import math, random
import linear_algebra as la

##### 8.1 梯度下降的思想
# 向量的平方和
def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)

# 如果 f 是单变量函数,那么它在 x 点的导数衡量了当 x 发生变化时,f(x) 变化了多少
# 导数通过差商的极限来定义
def difference_quotient(f, x, h):
    return (f(x + h) - f(x)) / h

# 梯度估算 
def plot_estimated_derivative():
    # 平方函数
    def square(x):
        return x * x
    # 平方函数的导函数
    def derivative(x):
        return 2 * x 

    # 导数变化 
    derivative_estimate = lambda x: difference_quotient(square, x, h=0.000001)

    x = range(-10,10)
    plt.plot(x, list(map(derivative, x)), 'rx', label='Actual')
    plt.plot(x, list(map(derivative_estimate, x)), 'b+', label='Estimate') 
    plt.show() # purple *, hopefully

# 差商法计算偏导数
def partial_difference_quotient(f, v, i, h):
    # add h to just the i-th element of v
    w = [v_j + (h if j == i else 0)
         for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h

def estimate_gradient(f, v, h=0.00001):
    return [partial_difference_quotient(f, v, i, h) for i, _ in enumerate(v)]



##### 8.3 使用梯度
# 当输入v是零向量时, 函数sum_of_squares取值最小
# 但如果不知道输入是什么, 可以用梯度方法从所有的三维向量中找到最小值
# 我们先找出随机初始点, 并在梯度的反方向以小步逐步前进, 直到梯度变得非常小

def step(v, direction, step_size):
    """move step_size in the direction from v"""
    # print("v :", v)
    # print("d :", direction)
    # print("z :", list(zip(v, direction)))
    return [v_i + step_size * direction_i for v_i, direction_i in zip(v, direction)]

def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]



##### 8.4 选择正确的步长
def safe(f):
    """define a new function that wraps f and return it"""
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return float('inf') # this means "infinity" in Python
    return safe_f



##### 8.5 综合
# 我们称它为 minimize_batch,因为在每一步梯度计算中,它都会搜索整个数据集
# (因为target_fn 代表整个数据集的残差)
def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]

    theta = theta_0                           # set theta to initial value
    target_fn = safe(target_fn)               # safe version of target_fn
    value = target_fn(theta)                  # value we're minimizing

    while True:
        gradient = gradient_fn(theta)
        # print("gradient=", gradient)
        next_thetas = [step(theta, gradient, -step_size) for step_size in step_sizes]
        # choose the one that minimizes the error function
        next_theta = min(next_thetas, key=target_fn)
        # print("next theta=", next_theta)
        next_value = target_fn(next_theta)
        # print("next value=", next_value)
        # stop if we're "converging"
        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value

# 有时候,我们需要最大化某个函数,这只需要最小化这个函数的负值(相应的梯度函数也 需取负)
def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)

def negate_all(f):
    """the same when f returns a list of numbers"""
    return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]

def maximize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    return minimize_batch(negate(target_fn),
                          negate_all(gradient_fn),
                          theta_0,
                          tolerance)


##### 8.6 随机梯度下降
def in_random_order(data):
    """generator that returns the elements of data in random order"""
    indexes = [i for i, _ in enumerate(data)]  # create a list of indexes
    random.shuffle(indexes)                    # shuffle them
    for i in indexes:                          # return the data in that order
        yield data[i]

def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    data = list(zip(x, y))
    theta = theta_0                             # initial guess
    alpha = alpha_0                             # initial step size
    min_theta, min_value = None, float("inf")   # the minimum so far
    iterations_with_no_improvement = 0

    # if we ever go 100 iterations with no improvement, stop
    while iterations_with_no_improvement < 100:
        value = sum(target_fn(x_i, y_i, theta) for x_i, y_i in data )

        if value < min_value:
            # if we've found a new minimum, remember it
            # and go back to the original step size
            min_theta, min_value = theta, value
            iterations_with_no_improvement = 0
            alpha = alpha_0
        else:
            # otherwise we're not improving, so try shrinking the step size
            iterations_with_no_improvement += 1
            alpha *= 0.9

        # and take a gradient step for each of the data points
        for x_i, y_i in in_random_order(data):
            gradient_i = gradient_fn(x_i, y_i, theta)
            theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))

    return min_theta

def maximize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    return minimize_stochastic(negate(target_fn),
                               negate_all(gradient_fn),
                               x, y, theta_0, alpha_0)


##### 测试
if __name__ == "__main__":
    # test 1
    # plot_estimated_derivative()

    # test 2
    """
    print("using the gradient")
    v = [random.randint(-10,10) for i in range(3)]
    tolerance = 0.0000001

    while True:
        gradient = sum_of_squares_gradient(v)   # compute the gradient at v
        next_v = step(v, gradient, -0.01)       # take a negative gradient step
        if la.distance(next_v, v) < tolerance:     # stop if we're converging
            break
        v = next_v                              # continue if we're not

    print("minimum v", v)
    print("minimum value", sum_of_squares(v))
    print()
    """

    # test 3
    print("using minimize_batch")
    # v = [random.randint(-10,10) for i in range(3)]
    v = [2, 4, 6]
    v = minimize_batch(sum_of_squares, sum_of_squares_gradient, v)
    print("minimum v", v)
    print("minimum value", sum_of_squares(v))



