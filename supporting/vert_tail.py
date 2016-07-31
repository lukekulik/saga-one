import numpy as np


def vert_tail(Sv, Bver, c_ver, taper_v, tc_vt, Av, sweep_vt, lh, MTOW):
    Svt = Sv / 0.3048 ** 2
    Hhor = 0.  # Change if tail is above fuselage!
    Nz = 2.5 * 1.5
    c_ver_tip = c_ver * taper_v
    Lt = lh / 0.3048
    Kz = Lt
    Hv = Bver / 0.3048
    Ht = Hhor / 0.3048
    W_vtail = 0.83 * 0.0026 * (
                                  1 + Ht / Hv) ** 0.225 * MTOW ** 0.556 * Nz ** 0.536 * Lt ** -0.5 * Svt ** 0.5 * Kz ** 0.875 * np.cos(
        sweep_vt) ** -1 * Av ** 0.35 * tc_vt ** -0.5 * 0.45359237  # kg assuing composite
    # cg_vtail = l_center - l_forwof_LE + l_tail - 0.58*(0.62*(c_ver-c_ver_tip)+c_ver_tip)
    return W_vtail
