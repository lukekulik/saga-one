# tube.py
#
# Created:  Jan 2014, A. Wendorff
# Modified: Feb 2014, A. Wendorff
#           Feb 2016, E. Botero  

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Units
import numpy as np


# ----------------------------------------------------------------------
#   Tube
# ----------------------------------------------------------------------

def tube(S_fus, diff_p_fus, w_fus, h_fus, l_nose, l_center, l_tail, l_fus, Nlim, wt_zf, wt_wing, wt_propulsion,
         wing_c_r, MTOW, h_gear):
    """ weight = SUAVE.Methods.Weights.Correlations.Tube_Wing.tube(S_fus, diff_p_fus, w_fus, h_fus, l_fus, Nlim, wt_zf, wt_wing, wt_propulsion, wing_c_r)
        Calculate the weight of a fuselage in the state tube and wing configuration
        
        Inputs:
            S_fus - fuselage wetted area [meters**2]
            diff_p_fus - Maximum fuselage pressure differential [Pascal]
            w_fus - width of the fuselage [meters]
            h_fus - height of the fuselage [meters]
            l_fus - length of the fuselage [meters]
            Nlim - limit load factor at zero fuel weight of the aircraft [dimensionless]
            wt_zf - zero fuel weight of the aircraft [kilograms]
            wt_wing - weight of the wing of the aircraft [kilograms]
            wt_propulsion - weight of the entire propulsion system of the aircraft [kilograms]
            wing_c_r - wing root chord [meters]
            
        Outputs:
            weight - weight of the fuselage [kilograms]
            
        Assumptions:
            fuselage in a standard wing and tube configuration 
    """
    # unpack inputs

    diff_p = diff_p_fus / (Units.force_pound / Units.ft ** 2)  # Convert Pascals to lbs/ square ft
    width = w_fus / Units.ft  # Convert meters to ft
    height = h_fus / Units.ft  # Convert meters to ft

    # setup
    length = l_fus - wing_c_r / 2.
    length = length / Units.ft  # Convert meters to ft
    weight = (wt_zf - wt_wing - wt_propulsion) / Units.lb  # Convert kg to lbs
    area = S_fus / Units.ft ** 2  # Convert square meters to square ft

    # process

    # Calculate fuselage indices
    I_p = 1.5 * 10 ** -3. * diff_p * width
    I_b = 1.91 * 10 ** -4. * Nlim * weight * length / height ** 2.

    if I_p > I_b:
        I_f = I_p
    else:
        I_f = (I_p ** 2. + I_b ** 2.) / (2. * I_b)

    # Calculate weight of wing for traditional aircraft vertical tail without rudder
    fuselage_weight = ((1.051 + 0.102 * I_f) * area) * Units.lb  # Convert from lbs to kg

    h_gf = 2 * 1.5  # m - factor of 2 because there are two bays
    w_gf = 1.5  # m
    # d_gf = np.sqrt(h_gf*w_gf)
    R_gf = (h_gf - w_gf) / (h_gf + w_gf)
    d_gf = 0.5 * (w_gf + h_gf) * (63 - 3 * R_gf ** 4) / (64 - 16 * R_gf ** 2)
    l1 = 0.5 * d_gf + 0.05
    l2 = l1
    l_gf = (h_gear - l2) + l1 + l2  # m
    Sw_gf = 0.75 * np.pi * l1 * d_gf + np.pi * d_gf * (h_gear - l2) + 0.72 * np.pi * l2
    # k1_gf = l1/l_gf
    # k2_gf = l2/l_gf
    # eta1_gf = np.sqrt(1-((d_gf/l_gf)/(2*k1_gf))**2)
    # eta2_gf = np.sqrt(1-((d_gf/l_gf)/(2*k2_gf))**2)
    # fe1_gf = np.arcsin(eta1_gf)/eta1_gf
    # fe2_gf = np.arcsin(eta2_gf)/eta2_gf
    # Sw_gf = (0.5*np.pi*d_gf**2)*(1+(l_gf/d_gf)*(k1_gf*(fe1_gf-2)+k2_gf*(fe2_gf-2)+2))* np.sqrt(h_gf/w_gf + w_gf/h_gf)/np.sqrt(2)

    Klg = 1.12  # for fuselage mounteg gears
    R = (h_fus - w_fus) / (h_fus + w_fus)
    d_fus = 0.5 * (w_fus + h_fus) * (63 - 3 * R ** 4) / (64 - 16 * R ** 2)
    # d_fus = np.sqrt(h_fus*w_fus)
    # k1 = l_nose/l_fus
    # k2 = l_tail/l_fus
    # eta1 = np.sqrt(1-((d_fus/l_fus)/(2*k1))**2)
    # eta2 = np.sqrt(1-((d_fus/l_fus)/(2*k2))**2)
    # fe1 = np.arcsin(eta1)/eta1
    # fe2 = np.arcsin(eta2)/eta2

    tc_hor = 0.11
    tc_ver = 0.11
    c_root_h = 3.58  # m
    c_root_v = 2.9  # m
    t_hor = tc_hor * c_root_h * 2.5  # m - increase thickness to accomodate tail
    # print 't_hor = ', t_hor, 'm'
    t_ver = tc_ver * c_root_v * 2.5  # m
    # print 't_ver = ', t_ver, 'm'

    # Sw_fus = (0.5*np.pi*d_fus**2)*(1+(l_fus/d_fus)*(k1*(fe1-2)+k2*(fe2-2)+2)) + Sw_gf #m^2 -- Southhammpton method
    # Sw_fus = 0.75*np.pi*d_fus*l_nose + np.pi*d_fus*l_center + 0.72*np.pi*d_fus*l_tail + Sw_gf # -- Stamford method
    k_ar = np.pi  # Raymer Method
    A_side = 0.5 * h_fus * l_nose * 1.05 + h_fus * l_center + 0.2 * l_tail * (
        h_fus + 0.6 * h_fus) / 2 + 0.8 * l_tail * (0.6 * h_fus + 1.1 * t_hor) / 2
    A_top = 0.5 * w_fus * l_nose * 1.05 + w_fus * l_center + 0.2 * l_tail * (w_fus + 0.9 * w_fus) / 2 + 0.8 * l_tail * (
        0.9 * w_fus + 1.1 * t_ver) / 2
    Sw_fus = 1.2 * k_ar * (A_side + A_top) / 2. + Sw_gf
    W_fus = 0.92 * 0.9 * 0.328 * Klg * (MTOW * 2.20462262 * Nlim) ** 0.5 * (l_fus / 0.3048) ** 0.25 * (Sw_fus / (
        0.3048 ** 2)) ** 0.302 * (l_fus / d_fus) ** 0.1 * 0.45359237  # kg
    fuselage_weight = W_fus
    return fuselage_weight
