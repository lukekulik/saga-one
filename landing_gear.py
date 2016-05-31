# landing_gear.py
# 
# Created:  Jan 2014, A. Wendorff
# Modified: Feb 2016, E. Botero

# ----------------------------------------------------------------------
#   Landing Gear
# ----------------------------------------------------------------------

def landing_gear(TOW, d_eng, d_fus, V_descent, landing_gear_wt_factor=0.04):
    """ weight = SUAVE.Methods.Weights.Correlations.Tube_Wing.landing_gear(TOW)
        Calculate the weight of the landing gear assuming that the gear
        weight is 4 percent of the takeoff weight

        Inputs:
            TOW - takeoff weight of the aircraft [kilograms]
            landing_gear_wt_factor - landing gear weight as percentage of TOW [dimensionless]

        Outputs:
            weight - weight of the landing gear [kilograms]

        Assumptions:
            calculating the landing gear weight based on the takeoff weight
    """

    # process
    weight = landing_gear_wt_factor * TOW

    Ngear = 3.  # load factor for landing gear
    Nl = Ngear * 1.5  # landing load factor
    Nmw = 2 * 2  # number of wheels in the main gears
    Nmss = 4.  # number of shock absorbers
    Nnw = 2.  # number of wheels in the nose wheel

    V_stall = V_descent / 1.2
    MLW = 0.8 * TOW  # kg
    d_nacelle = 1.15 * d_eng
    h_pyl = 0.4  # m
    h_wing_gear = d_nacelle + h_pyl + 1.25
    h_gear = h_wing_gear - d_fus
    h_nosegear = h_gear
    W_maingear = 0.0106 * (MLW / 0.45359237) ** 0.888 * Nl ** 0.25 * (
                                                                     h_gear * 39.3700787) ** 0.4 * Nmw ** 0.321 * Nmss ** (
    -0.5) * (V_stall / 0.514444444) ** 0.1 * 0.45359237  # kg
    W_nosegear = 0.032 * (MLW / 0.45359237) ** 0.646 * Nl ** 0.2 * (
                                                                   h_nosegear * 39.3700787) ** 0.5 * Nnw ** 0.45 * 0.45359237  # kg
    W_gear = W_maingear + W_nosegear
    weight = W_gear

    return weight