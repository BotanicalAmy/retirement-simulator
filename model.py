import numpy as np


def IQR(dist):
    return np.percentile(dist, 75) - np.percentile(dist, 25)

def Q1(dist):
    return np.percentile(dist, 25)

def Q3(dist):
    return np.percentile(dist, 75)

def confidence_interval(dist):
    dist_avg = np.mean(dist)
    dist_std = np.std(dist)
    conf_top = ((dist_avg + (2 * dist_std))*100)
    conf_bottom = ((dist_avg - (2 * dist_std))*100)
    return round(conf_bottom,2), round(conf_top,2)
