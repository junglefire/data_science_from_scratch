from collections import Counter
import math, random

#
# data splitting
#
def split_data(data, prob):
    """split data into fractions [prob, 1 - prob]"""
    results = [], []
    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results

def train_test_split(x, y, test_pct):
    data = list(zip(x, y))                        # pair corresponding values
    print("data=", data)
    train, test = split_data(data, 1 - test_pct)  # split the dataset of pairs
    print("train=", train)
    x_train, y_train = list(zip(*train))          # magical un-zip trick
    x_test, y_test = list(zip(*test))
    return x_train, x_test, y_train, y_test

#
# correctness
#
def accuracy(tp, fp, fn, tn):
    correct = tp + tn
    total = tp + fp + fn + tn
    return correct / total

def precision(tp, fp, fn, tn):
    return tp / (tp + fp)

def recall(tp, fp, fn, tn):
    return tp / (tp + fn)

def f1_score(tp, fp, fn, tn):
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)
    return 2 * p * r / (p + r)



##### 测试
if __name__ == "__main__":
    """
    X = [0,1,2,3,4,5,6,7,8,9]
    Y = [10,11,12,13,14,15,16,17,18,19]

    x1, x2 = split_data(X, 0.3)
    print("train =", x1)
    print("test  =", x2)

    x1, x2, y1, y2 = train_test_split(X, Y, 0.3)
    print("x-train =", x1)
    print("x-test  =", x2)
    print("y-train =", y1)
    print("y-test  =", y2)
    """

    print("accuracy(70, 4930, 13930, 981070)", accuracy(70, 4930, 13930, 981070))
    print("precision(70, 4930, 13930, 981070)", precision(70, 4930, 13930, 981070))
    print("recall(70, 4930, 13930, 981070)", recall(70, 4930, 13930, 981070))
    print("f1_score(70, 4930, 13930, 981070)", f1_score(70, 4930, 13930, 981070))

