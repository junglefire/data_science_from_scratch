#!/usr/bin/python
import math, random

##### 7.1 掷硬币
# 根据n(实验次数)和p(概率)计算正态分布的mu和sigma
def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma

# 正态分布的累积分布函数
def normal_cdf(x, mu=0,sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

# 正态cdf是一个变量在一个阈值以下的概率
normal_probability_below = normal_cdf

# 如果它不在阈值以下,就在阈值之上
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)

# 如果它小于hi但不比lo小,那么它在区间之内
def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

# 如果不在区间之内,那么就在区间之外
def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)

# 或者反过来,找出非尾区域,或者找出均值两边的(对称)区域,这个区域恰好对应
# 特定比例的可能性。比如,如果我们需要找出以均值为中心、覆盖 60% 可能性
# 的区间,那我们需要找到两个截点,使上尾和下尾各覆盖 20% 的可能性(给中间
# 留出60%)
# 对normal_cdf取逆, 从而可以求出特定的概率的相应值
def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    """find approximate inverse using binary search"""
    # if not standard, compute standard and rescale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0            # normal_cdf(-10) is (very close to) 0
    hi_z,  hi_p  =  10.0, 1            # normal_cdf(10)  is (very close to) 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2     # consider the midpoint
        mid_p = normal_cdf(mid_z)      # and the cdf's value there
        if mid_p < p:
            # midpoint is still too low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            # midpoint is still too high, search below it
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z

def normal_upper_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)

def normal_lower_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """returns the symmetric (about the mean) bounds
    that contain the specified probability"""
    tail_probability = (1 - probability) / 2
    # upper bound should have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    # lower bound should have tail_probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound

def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is above x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is below x
        return 2 * normal_probability_below(x, mu, sigma)
        


##### 测试
if __name__ == "__main__":
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    print("mu_0    :", mu_0)
    print("sigma_0 :", sigma_0)
    print("normal_two_sided_bounds(0.95, mu_0, sigma_0): ", normal_two_sided_bounds(0.95, mu_0, sigma_0))
    print()

    print("actual mu and sigma based on p = 0.55")
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
    print("mu_1    :", mu_1)
    print("sigma_1 :", sigma_1)
    print("normal_two_sided_bounds(0.95, mu_1, sigma_1): ", normal_two_sided_bounds(0.95, mu_1, sigma_1))
    print()

    # a type 2 error means we fail to reject the null hypothesis
    # which will happen when X is still in our original interval
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    print("lo :", lo)
    print("hi :", hi)

    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    power = 1 - type_2_probability # 0.887

    print("type 2 probability :", type_2_probability)
    print("power :", power)



