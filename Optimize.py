# Optimize.py
# Created:  Feb 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE.Optimization.Package_Setups.scipy_setup as scipy_setup
import matplotlib.pyplot as plt
import numpy as np
from SUAVE.Core import Units, Data
from SUAVE.Optimization import Nexus, carpet_plot

import Analyses
import Mission
import Plot_Mission
import Procedure
import Vehicles

# ----------------------------------------------------------------------
#   Run the whole thing
# ----------------------------------------------------------------------


AVL_analysis = False  # AVL Analysis switch


def main():
    print "SUAVE initialized...\n"
    problem = setup()  # "problem" is a nexus

    # problem.optimization_problem.inputs = np.array([
    #     # Variable inputs
    #     ['wing_area', 700., (650., 750.), 500., Units.meter ** 2],
    #     ['MTOW', 207, (190, 210), 200, Units['tonne']],
    #     ['alt_outgoing_cruise', 13.14, (9., 14.), 13., Units.km],  # 13.15 #explain the physics behing the optimizer
    #     ['design_thrust', 110e3, (100e3, 120e3), 100e3, Units.N],
    #     ['outgoing_cruise_speed', 190., (180., 212.), 200., Units['m/s']],  # 191
    #     ['spray_cruise_speed', 210., (205., 212.), 200, Units['m/s']],
    #
    #     ['cruise1_distance', 1050., (1000., 1200.), 1075., Units.km],
    #     ['cruise2_distance', 1173., (1000., 1300.), 1225., Units.km],
    #     ['cruise3_distance', 1001., (900., 1200.), 1000., Units.km],
    #
    #     ['cruise_outgoing_distance', 3393., (3200., 3500.), 3300., Units.km],
    #     # climb throttle as input?
    #
    #     # "Set" inputs
    #     ['AR', 13., (12., 14.), 13., Units.less],  # aerosol released per kg of fuel ratio max?
    #     ['payload', 35e3, (35e3, 35e3), 30e3, Units.kg],
    #     # speeds???
    # ])
    #
    # variable_sweep(problem,"Fuel burn [kg]", "Fuel margin","Wing area [$m^2$]","MTOW [tonne]","MTOWS")


    output = problem.objective()  # uncomment this line when using the default inputs
    # variable_sweep(problem)  # uncomment this to view some contours of the problem
    # output = scipy_setup.SciPy_Solve(problem, solver='SLSQP')  # uncomment this to optimize the values

    print 'constraints=', problem.all_constraints()

    Plot_Mission.plot_mission(problem.results, show=False)

    return


# ----------------------------------------------------------------------
#   Inputs, Objective, & Constraints
# ----------------------------------------------------------------------  

def setup():
    nexus = Nexus()
    problem = Data()
    nexus.optimization_problem = problem

    # -------------------------------------------------------------------
    # Inputs
    # -------------------------------------------------------------------

    problem.inputs = np.array([
        # Variable inputs
        ['wing_area', 700., (650., 725.), 500., Units.meter ** 2],
        ['MTOW', 207e3, (207e3, 207e3), 200e3, Units.kg],
        ['alt_outgoing_cruise', 13.14, (9., 14.), 13., Units.km],  # 13.15 #explain the physics behing the optimizer
        ['design_thrust', 110e3, (100e3, 120e3), 100e3, Units.N],
        ['outgoing_cruise_speed', 190., (180., 212.), 200., Units['m/s']],  # 191
        ['spray_cruise_speed', 210., (205., 212.), 200, Units['m/s']],

        ['cruise1_distance', 1050., (1000., 1200.), 1075., Units.km],
        ['cruise2_distance', 1173., (1000., 1300.), 1225., Units.km],
        ['cruise3_distance', 1001., (900., 1200.), 1000., Units.km],

        ['cruise_outgoing_distance', 3393., (3200., 3500.), 3300., Units.km],
        # climb throttle as input?

        # "Set" inputs
        ['AR', 13., (12., 14.), 13., Units.less],  # aerosol released per kg of fuel ratio max?
        ['payload', 35e3, (35e3, 35e3), 30e3, Units.kg],
        # speeds???
    ])

    # -------------------------------------------------------------------
    # Objective
    # -------------------------------------------------------------------

    # throw an error if the user isn't specific about wildcards
    # [ tag, scaling, units ]
    problem.objective = np.array([
        ['fuel_burn', 60000., Units.kg]
    ])

    # -------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------

    # [ tag, sense, edge, scaling, units ]
    problem.constraints = np.array([

        # ['min_throttle', '>', 0., 1e-1, Units.less],
        ['max_throttle', '<', 1., 1., Units.less],
        # ['main_mission_time', '<', 11.1, 10, Units.h],
        ['design_range_fuel_margin', '>', 0.1, 1E-1, Units.less],
        # ['take_off_field_length', '<', 2500., 2500, Units.m],
        # ['landing_field_length', '<', 2500., 2500, Units.m],
        ['clmax', '<', 1.1, 1, Units.less],
        ['non_spraying_range', '>', 3500., 3500., Units.km],
        ['spraying_range', '>', 3500., 3500., Units.km]
        # main mission range

    ])

    # -------------------------------------------------------------------
    #  Aliases
    # -------------------------------------------------------------------

    # [ 'alias' , ['data.path1.name','data.path2.name'] ]

    problem.aliases = [
        ['wing_area', ['vehicle_configurations.*.wings.main_wing.areas.reference',
                       'vehicle_configurations.*.reference_area']],

        ['MTOW', ['vehicle_configurations.*.mass_properties.takeoff',
                  "vehicle_configurations.*.mass_properties.max_takeoff"]],

        ['alt_outgoing_cruise', 'missions.base.segments.final_outgoing.altitude_end'],

        ['design_thrust', 'vehicle_configurations.*.propulsors.turbofan.thrust.total_design'],

        ['spray_cruise_speed', ['missions.base.segments.cruise_1.air_speed',
                                'missions.base.segments.cruise_2.air_speed',
                                'missions.base.segments.cruise_final.air_speed']],

        ['outgoing_cruise_speed', 'missions.base.segments.cruise_outgoing.air_speed'],

        ['AR', 'vehicle_configurations.*.wings.main_wing.aspect_ratio'],

        ['payload', ['vehicle_configurations.*.mass_properties.max_payload',
                     'vehicle_configurations.*.mass_properties.payload']],

        ['fuel_burn', 'summary.base_mission_fuelburn'],

        ['min_throttle', 'summary.min_throttle'],

        ['max_throttle', 'summary.max_throttle'],

        ['main_mission_time', 'summary.main_mission_time'],

        ['mission_range', 'summary.mission_range'],

        ['clmax', 'summary.clmax'],

        ['design_range_fuel_margin', 'summary.max_zero_fuel_margin'],

        ['take_off_field_length', 'summary.field_length_takeoff'],

        ['landing_field_length', 'summary.field_length_landing'],

        ['MTOW_delta', 'summary.MTOW_delta'],

        ['cruise_speed', 'missions.base.segments.cruise_empty.air_speed'],

        ['cruise1_distance', 'missions.base.segments.cruise_1.distance'],
        ['cruise2_distance', 'missions.base.segments.cruise_2.distance'],
        ['cruise3_distance', 'missions.base.segments.cruise_final.distance'],
        ['cruise_outgoing_distance', 'missions.base.segments.cruise_outgoing.distance'],

        ['non_spraying_range', 'summary.empty_range'],
        ['spraying_range', 'summary.spray_range'],

        # [
        #    "missions.base.segments.cruise_highlift.air_speed",
        #
        #    "missions.base.segments.cruise_2.air_speed"]],
        # ['return_cruise_speed', "missions.base.segments.cruise_final.air_speed"],

        ['oswald', 'vehicle_configurations.*.wings.main_wing.span_efficiency'],
        ['cruise_altitude', "missions.base.segments.climb_8.altitude_end"],

        ['return_cruise_alt', 'missions.base.segments.descent_1.altitude_end'],

        ['bypass', 'vehicle_configurations.*.propulsors.turbofan.bypass_ratio'],
        ['wing_sweep', 'vehicle_configurations.*.wings.main_wing.sweep'],
        ['oew', 'summary.op_empty'],
        ['Nothing', 'summary.nothing'],

    ]

    # -------------------------------------------------------------------
    #  Vehicles
    # -------------------------------------------------------------------
    nexus.vehicle_configurations = Vehicles.setup()

    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    nexus.analyses = Analyses.setup(nexus.vehicle_configurations)

    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
    nexus.missions = Mission.setup(nexus.analyses)

    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.procedure = Procedure.setup()

    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary = Data()

    return nexus


def variable_sweep(problem, color_label, bar_label, xlabel, ylabel, title):
    number_of_points = 5
    outputs = carpet_plot(problem, number_of_points, 0, 0)  # run carpet plot, suppressing default plots
    inputs = outputs.inputs
    objective = outputs.objective
    constraints = outputs.constraint_val
    plt.figure(0)
    CS = plt.contourf(inputs[0, :], inputs[1, :], objective, 20, linewidths=2, cmap='hot')
    cbar = plt.colorbar(CS)
    cbar.ax.set_ylabel(color_label)
    # cbar.ax.set_ylabel('fuel burn (kg)')

    if bar_label != "unknown":
        CS_const = plt.contour(inputs[0, :], inputs[1, :], constraints[0, :, :])
        plt.clabel(CS_const, inline=1, fontsize=10)
        cbar = plt.colorbar(CS_const)
        # cbar.ax.set_ylabel('fuel margin')
        cbar.ax.set_ylabel(bar_label)

    # plt.xlabel('wing area (m^2)')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.ylabel('cruise_speed (km)')

    '''
    #now plot optimization path (note that these data points were post-processed into a plottable format)
    wing_1  = [95          ,	95.00000149 ,	95          ,	95          ,	95.00000149 ,	95          ,	95          ,	95.00000149 ,	95          ,	106.674165  ,	106.6741665 ,	106.674165  ,	106.674165  ,	106.6741665 ,	106.674165  ,	106.674165  ,	106.6741665 ,	106.674165  ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	105.6274294 ,	105.6274309 ,	105.6274294 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	106.9084316 ,	106.9084331 ,	106.9084316 ,	110.520489  ,	110.5204905 ,	110.520489  ,	110.520489  ,	110.5204905 ,	110.520489  ,	110.520489  ,	110.5204905 ,	110.520489  ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	113.2166831 ,	113.2166845 ,	113.2166831 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.1649262 ,	114.1649277 ,	114.1649262 ,	114.2149828]
    alt_1   = [11.0              ,	11.0              ,	11.000000149011612,	11.0              ,	11.0              ,	11.000000149011612,	11.0              ,	11.0              ,	11.000000149011612,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	9.540665954351425 ,	9.540665954351425 ,	9.540666103363037 ,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.023015652305284,	10.023015652305284,	10.023015801316896,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.190994033521863,	10.190994033521863,	10.190994182533474,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.440582829327589,	10.440582829327589,	10.4405829783392  ,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.536514606250261,	10.536514606250261,	10.536514755261873,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.535957839878783,	10.535957839878783,	10.535957988890395,	10.52829047]
    wing_2  = [128        ,	128.0000015,	128        ,	128        ,	128.0000015,	128        ,	128        ,	128.0000015,	128        ,	130        ,	130.0000015,	130        ,	130        ,	130.0000015,	130        ,	130        ,	130.0000015,	130        ,	122.9564124,	122.9564139,	122.9564124,	122.9564124,	122.9564139,	122.9564124,	122.9564124,	122.9564139,	122.9564124,	116.5744347,	116.5744362,	116.5744347,	116.5744347,	116.5744362,	116.5744347,	116.5744347,	116.5744362,	116.5744347,	116.3530891,	116.3530906,	116.3530891,	116.3530891,	116.3530906,	116.3530891,	116.3530891,	116.3530906,	116.3530891]
    alt_2   = [13.8,	13.799999999999999,	13.80000014901161,	13.799999999999999,	13.799999999999999,	13.80000014901161,	13.799999999999999,	13.799999999999999,	13.80000014901161,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.302562430674953,	11.302562430674953,	11.302562579686565,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.158808932491421,	11.158808932491421,	11.158809081503033,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.412913394878741,	11.412913394878741,	11.412913543890353,	11.402627869388722,	11.402627869388722,	11.402628018400334,	11.402627869388722,	11.402627869388722,	11.402628018400334,	11.402627869388722,	11.402627869388722,	11.402628018400334]

    
    opt_1   = plt.plot(wing_1, alt_1, label='optimization path 1')
    init_1  = plt.plot(wing_1[0], alt_1[0], 'ko')
    final_1 = plt.plot(wing_1[-1], alt_1[-1], 'kx')
    
    opt_2   = plt.plot(wing_2, alt_2, 'k--', label='optimization path 2')
    init_2  = plt.plot(wing_2[0], alt_2[0], 'ko', label= 'initial points')
    final_2 = plt.plot(wing_2[-1], alt_2[-1], 'kx', label= 'final points')
    '''
    plt.legend(loc='upper left')
    plt.savefig(title + ".eps")
    plt.show()

    return


if __name__ == '__main__':
    main()
