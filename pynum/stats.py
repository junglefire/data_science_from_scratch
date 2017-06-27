#!/usr/bin/python
from __future__ import division
from collections import Counter
import math
import linear_algebra as la

### 均值(mean 或average), 即用数据和除以数据个数
### this isn't right if you don't from __future__ import division
def mean(x):
    return sum(x) / len(x)

### 中位数(median), 它是指数据中间点的值
def median(v):
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if n % 2 == 1:
        return sorted_v[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2

### 中位数的一个泛化概念是分位数(quantile), 它表示少于数据中特定百分比的一个值
def quantile(x, p):
    p_index = int(p * len(x))
    return sorted(x)[p_index]

### 众数(mode),它是指出现次数最多的一个或多个数
def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items()
            if count == max_count]





### 离散度是数据的离散程度的一种度量。通常, 如果它所统计的值接近零, 则表示数据聚集
### 在一起, 离散程度很小; 如果值很大(无论那意味着什么), 则表示数据的离散度很大

### 极差(range),指最大元素与最小元素的差
### "range" already means something in Python, so we'll use a different name
def data_range(x):
    return max(x) - min(x)

### 去均值
def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

### 方差是在概率论和统计方差衡量随机变量或一组数据时离散程度的度量
### 概率论中方差用来度量随机变量和其数学期望（即均值）之间的偏离程度
### 统计中的方差是每个样本值与全体样本值的平均数之差的平方值的平均数
def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return la.sum_of_squares(deviations) / (n - 1)

### 标准差, 又常称均方差, 即方差的平方根
### 标准差的单位和测量值的单位是一样的，这点在实际物理等应用中很重要, 而方差的单位是其平方
def standard_deviation(x):
    return math.sqrt(variance(x))

### 分位数之差
### 极差和标准差也都有我们之前提到的均值计算常遇到的异常值问题
### 一种更加稳健的方案是计算 75% 的分位数和 25% 的分位数之差
def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

### 协方差(covariance),这个概念是方差的一个对应词
### 方差衡量了单个变量对均值的偏离程度, 协方差衡量了两个变量对均值的串联偏离程度
### 尝试理解：
###     点乘(dot)意味着对应的元素对相乘后再求和
###     如果向量x、y的对应元素同时大于它们自身序列的均值, 或者同时小于均值, 那将为求和贡献一个正值
###     如果其中一个元素大于自身的均值, 而另一个小于均值, 将为求和贡献一个负值
###     因此，
###     协方差是一个大的正数意味着如果y很大, 那么x也很大, 或者y很小, x 也很小
###     如果协方差为负而且绝对值很大, 就意味着x和y一个很大,而另一个很小
###     接近零的协方差意味着以上关系都不存在
def covariance(x, y):
    n = len(x)
    return la.dot(de_mean(x), de_mean(y)) / (n - 1)

### 相关是更常受到重视的概念(why?), 它是由协方差除以两个变量的标准差
### 相关的取值在-1(完全反相关) 和 1(完全相关)之间
def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0 # if no variation, correlation is zero



