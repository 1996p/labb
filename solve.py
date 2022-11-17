import math
import matplotlib.pyplot as plt
import numpy as np
from time import time
from consts import EPS

def refraction_reflection_graph(obj, left_border, right_border, eps):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.11, 3.31), dpi=100)

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.grid()

    function_values = []
    function_args = []
    for i in np.linspace(left_border, right_border, 20):
        function_values.append(f(i))
        function_args.append(i)

    ax.plot(function_args, function_values)
    plt.xlim(left_border, right_border)
    plt.ylim(-5, 5)
    root, spent_time, iters_count = get_root(left_border, right_border, eps)
    obj.ui.result.setText(str(root))
    obj.ui.feed.append(f"При точности {eps} -- {spent_time} s. -- {iters_count} итераций")
    return fig


def get_root(left_root_border: float, right_root_border: float, eps: float):
    if not has_root(left_root_border, right_root_border, eps):
        raise ValueError("Корней в промежутке нет")

    if convergence(left_root_border, right_root_border, eps):

        counter = 0
        start_time = time()
        last_approximate_root = (right_root_border - left_root_border) / 2
        # approximate_root = fi(last_approximate_root)
        #
        # while abs(approximate_root - last_approximate_root) >= eps:
        #     counter += 1
        #     last_approximate_root = approximate_root
        #     approximate_root = fi(approximate_root)

        while counter < 1000000:
            approximate_root = fi(last_approximate_root)
            if abs(approximate_root - last_approximate_root) < EPS:
                break
            counter += 1
            last_approximate_root = approximate_root

        return approximate_root, time() - start_time, counter
    else:
        max = abs(fd(left_root_border))
        i = left_root_border
        while i < right_root_border:
            cur = abs(fd(i))
            if cur > max:
                max = cur
            i += eps


        last_approximate_root = (right_root_border - left_root_border) / 2
        counter = 0
        while counter < 100000000:
            approximate_root = last_approximate_root - f(last_approximate_root) / max
            if abs(approximate_root - last_approximate_root) < EPS:
                break
            counter += 1
            last_approximate_root = approximate_root

        return approximate_root, 3, counter


def has_root(left_border: float, right_border: float, eps: float) -> bool:
    if f(left_border) * f(right_border) > 0:
        if abs(right_border - left_border) < eps:
            return False
        else:
            return has_root(left_border, (left_border + right_border) / 2, eps) or has_root((left_border + right_border) / 2, right_border, eps)
    else:
        return True


def convergence(left_border: float, right_border: float, eps: float) -> bool:
    while left_border < right_border:
        left_border += eps
        a = abs(fd(left_border))
        if abs(fd(left_border)) >= 1:
            return False
    return True


def f(x: float) -> float:
    return math.e ** x - 5 * x
    # return x * (2**x) - 1


def fi(x: float) -> float:
    # return 1 / (2**x)
    return (math.e ** x) / 5


def fd(x: float) -> float:
    h = 0.000000000001
    return (fi(x + h) - fi(x - h)) / (2 * h)




