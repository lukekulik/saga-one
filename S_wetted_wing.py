import math
import numpy as np


def S_wet_w(filename, taper, S, b, c_r, sections, d_fus, y_fus, twin):
    f = open(filename, 'r')
    flines = f.readlines()
    for i in range(len(flines)):
        flines[i] = flines[i][:-1]
        flines[i] = flines[i].split()
        flines[i][0] = float(flines[i][0])
        flines[i][1] = float(flines[i][1])

    b_step = b / (2. * sections)
    theta = math.atan(2. * (1 - taper) / b * c_r)
    b_i = 0.
    A_wet = 0.
    if twin == "ON":
        y_fus_in = y_fus - d_fus / 2
        y_fus_out = y_fus + d_fus / 2
    else:
        y_fus_in = 0.
        y_fus_out = d_fus / 2
    for i in range(sections):
        c_i_prev = c_r - b_i * math.tan(theta)
        b_i += b_step
        if y_fus_in <= b_i < y_fus_out:
            A_j = 0.
        else:
            c_i = c_r - b_i * math.tan(theta)
            dist_i = 0.
            dist_i_prev = 0.
            A_j = 0.
            for j in range(len(flines)):
                x_j_i = c_i * flines[j][0]  # Current section, current point
                x_j_prev_i = c_i * flines[j - 1][0]  # Current section, previous point
                x_j_i_prev = c_i_prev * flines[j][0]  # Previous section, current point
                x_j_prev_i_prev = c_i_prev * flines[j - 1][0]  # Previous section, previous point
                y_j_i = c_i * flines[j][1]
                y_j_prev_i = c_i * flines[j - 1][1]
                y_j_i_prev = c_i_prev * flines[j][1]
                y_j_prev_i_prev = c_i_prev * flines[j - 1][1]
                dist_j_i = math.sqrt((x_j_i - x_j_prev_i) ** 2 + (y_j_i - y_j_prev_i) ** 2)
                dist_j_i_prev = math.sqrt((x_j_i_prev - x_j_prev_i_prev) ** 2 + (y_j_i_prev - y_j_prev_i_prev) ** 2)
                A_j += b_step * (dist_j_i + dist_j_i_prev) / 2
        A_wet += A_j
    S_wet = 2 * A_wet
    return S_wet


def S_wet_fus(d_fus, l_nose, l_tail, l_fus):
    # S_wet_fus = math.pi*d_fus*(l_fus-1.3*d_fus)
    h_gf = 2 * 1  # m - factor of 2 because there are two bays
    w_gf = 1.5  # m
    d_gf = np.sqrt(h_gf * w_gf)
    l1 = 0.5 * d_gf + 0.05
    l2 = l1
    l_gf = (1.8 - l2) + l1 + l2  # m
    k1_gf = l1 / l_gf
    k2_gf = l2 / l_gf
    eta1_gf = np.sqrt(1 - ((d_gf / l_gf) / (2 * k1_gf)) ** 2)
    eta2_gf = np.sqrt(1 - ((d_gf / l_gf) / (2 * k2_gf)) ** 2)
    fe1_gf = np.arcsin(eta1_gf) / eta1_gf
    fe2_gf = np.arcsin(eta2_gf) / eta2_gf
    Sw_gf = (0.5 * np.pi * d_gf ** 2) * (
        1 + (l_gf / d_gf) * (k1_gf * (fe1_gf - 2) + k2_gf * (fe2_gf - 2) + 2)) * np.sqrt(
        h_gf / w_gf + w_gf / h_gf) / np.sqrt(2)

    k1 = l_nose / l_fus
    k2 = l_tail / l_fus
    eta1 = np.sqrt(1 - ((d_fus / l_fus) / (2 * k1)) ** 2)
    eta2 = np.sqrt(1 - ((d_fus / l_fus) / (2 * k2)) ** 2)
    fe1 = np.arcsin(eta1) / eta1
    fe2 = np.arcsin(eta2) / eta2

    S_wet_fus = (0.5 * np.pi * d_fus ** 2) * (
        1 + (l_fus / d_fus) * (k1 * (fe1 - 2) + k2 * (fe2 - 2) + 2)) + Sw_gf  # m^2
    return S_wet_fus
