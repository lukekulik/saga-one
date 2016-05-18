# Optimize.py
# Created:  Feb 2016, M. Vegh
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import SUAVE
from SUAVE.Core import Units, Data
import numpy as np
import Vehicles
import Analyses
import Missions
import Procedure
import Plot_Mission
import matplotlib.pyplot as plt
from SUAVE.Optimization import Nexus, carpet_plot
import SUAVE.Optimization.Package_Setups.scipy_setup as scipy_setup
from SUAVE.Input_Output.Results import  print_parasite_drag,  \
     print_compress_drag, \
     print_engine_data,   \
     print_mission_breakdown, \
     print_weight_breakdown

# ----------------------------------------------------------------------        
#   Run the whole thing
# ----------------------------------------------------------------------

output_folder = "output/"

def main():

    problem = setup() # "problem" is a nexus

    output = problem.objective()  #uncomment this line when using the default inputs
    
    '''
    #uncomment these lines when you want to start an optimization problem from a different initial guess
    inputs                                   = [1.28, 1.38]
    scaling                                  = problem.optimization_problem.inputs[:,3] #have to rescale inputs to start problem from here
    scaled_inputs                            = np.multiply(inputs,scaling)
    problem.optimization_problem.inputs[:,1] = scaled_inputs
    '''
    # output = scipy_setup.SciPy_Solve(problem,solver='SLSQP')

 
    
    # variable_sweep(problem)  #uncomment this to view some contours of the problem
    print 'fuel burn: ', problem.summary.base_mission_fuelburn
    # print 'fuel margin=', problem.all_constraints()


    
    Plot_Mission.plot_mission(problem.results)
    # print problem.results.base.segments.cruise.conditions.keys()

    # print problem.results.base.segments.cruise.conditions.propulsion

    cruise1_time =  problem.results.base.segments.cruise_2.conditions.frames.inertial.time[:,0] / Units.min #FIXME
    cruise1_dur = (cruise1_time.max()-cruise1_time.min())*Units.min/Units['h']
    # print "cruise duration=",cruise1_dur , " hours"
    print "aerosol released: ", problem.summary.base_mission_sprayed[0]  , " kg"
    # print "cruise range: ",problem.summary.cruise_range/1000., " km"


    print_weight_breakdown(problem.vehicle_configurations.base,filename = output_folder+'weight_breakdown.dat')
    #
    # # print engine data into file
    print_engine_data(problem.vehicle_configurations.base,filename = output_folder+'engine_data.dat')
    #
    # # print parasite drag data into file
    # # define reference condition for parasite drag
    ref_condition = Data()
    ref_condition.mach_number = 0.75 #FIXME
    ref_condition.reynolds_number = 7e6 # FIXME
    Analyses = Data()
    Analyses.configs = problem.analyses

    print_parasite_drag(ref_condition,problem.vehicle_configurations.cruise,Analyses,filename=output_folder+'parasite_drag.dat')
    #
    # print compressibility drag data into file

    # print Analyses
    print_compress_drag(problem.vehicle_configurations.cruise,Analyses,filename = output_folder+'compress_drag.dat')

    # print mission breakdown
    print_mission_breakdown(problem.results.base,filename=output_folder+'mission_breakdown.dat') #FIXME fuel weight adds aerosol = wrong!!!!!

    # segment.sprayer_rate

    # print problem.results.base.segments.cruise.keys()
    # print problem.results.base.segments.cruise.conditions.keys()

    # print problem.results.base.segments.cruise.conditions.stability.dynamic.cn_r #'cn_r', 'cl_p', 'cl_beta', 'cm_q', 'cm_alpha_dot', 'cz_alpha']
    # print problem.results.base.segments.cruise.conditions.stability.static.cm_alpha
    # print problem.results.base.segments.cruise.conditions.stability.static.cn_beta




    # print problem.results

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

    #   [ tag                            , initial, (lb,ub)             , scaling , units ]
    problem.inputs = np.array([
        #  [ 'wing_area'                    ,422    , (   350. ,   650.   ) ,   500. , Units.meter**2], # was 480 before
          ['cruise_speed', 756, (600., 900.), 500, Units['km/h'] ],
          ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
        # ['AR',20,(10.2,20.2),10,Units.less]

        # # []
        # [ 'cruise_altitude'              ,  19.5    , (   19.5   ,    21.   ) ,   10.  , Units.km],
        # [ 'c1_airspeed'              ,  90    , (   50   ,    250.   ) ,   100.  , Units['m/s']],
        # [ 'c1_rate'              ,  15    , (   1   ,    25.   ) ,   10.  , Units['m/s']],
        #
        # [ 'c2_airspeed'              ,  110    , (   50   ,    250.   ) ,   100.  , Units['m/s']],
        # [ 'c2_rate'              ,  11    , (   1   ,    25.   ) ,   10.  , Units['m/s']],
        #
        # [ 'c3_airspeed'              ,  120    , (   50   ,    250.   ) ,   100.  , Units['m/s']],
        # [ 'c3_rate'              ,  8    , (   1   ,    25.   ) ,   10.  , Units['m/s']],
        #
        # [ 'c4_airspeed'              ,  150    , (   50   ,    250.   ) ,   100.  , Units['m/s']],
        # [ 'c4_rate'              ,  6    , (   1   ,    25.   ) ,   10.  , Units['m/s']],
        #
        # [ 'c5_airspeed'              ,  200    , (   50   ,    250.   ) ,   100.  , Units['m/s']],
        # [ 'c5_rate'              ,  4    , (   1   ,    25.   ) ,   10.  , Units['m/s']]

# segment.altitude_end   = 3 * Units.km
#     segment.air_speed      = 118.0 * Units['m/s']
#     segment.climb_rate     = 15. * Units['m/s']


    ])
    

    
    # -------------------------------------------------------------------
    # Objective
    # -------------------------------------------------------------------

    # throw an error if the user isn't specific about wildcards
    # [ tag, scaling, units ]
    problem.objective = np.array([
        # [ 'Nothing', 1, Units.kg ]
        [ 'fuel_burn',  40000, Units.kg ]
    ])
    
    
    # -------------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------------

    # stuctural weight below some threshold
    # [ tag, sense, edge, scaling, units ]
    problem.constraints = np.array([
               # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
        [ 'fuel_burn', '<', 40000, 1, Units.kg ]
        # constraint on mission time?
        # [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less], #fuel margin defined here as fuel
    ])


    # -------------------------------------------------------------------
    #  Aliases
    # -------------------------------------------------------------------
    
    # [ 'alias' , ['data.path1.name','data.path2.name'] ]

    problem.aliases = [
        [ 'wing_area'                        ,   ['vehicle_configurations.*.wings.main_wing.areas.reference',
                                                  'vehicle_configurations.*.reference_area'                    ]],
        [ 'AR'                        ,   'vehicle_configurations.*.wings.main_wing.aspect_ratio'           ],
        [ 'cruise_speed'                  , ["missions.base.segments.cruise_2.air_speed",
                                             "missions.base.segments.cruise_highlift.air_speed"]],
        [ 'cruise_altitude'                  , "missions.base.segments.climb_5.altitude_end"                    ],
        [ 'fuel_burn'                        ,    'summary.base_mission_fuelburn'                               ],
        [ 'design_range_fuel_margin'         ,    'summary.max_zero_fuel_margin'                                ],
        [ 'return_cruise_alt'         ,    'missions.base.segments.descent_1.altitude_end'                      ],
        ['Nothing'          , 'summary.nothing' ],
        ['c1_airspeed' , 'missions.base.segments.climb_1.air_speed'],
        ['c1_rate' , 'missions.base.segments.climb_1.climb_rate'],

        ['c2_airspeed' , 'missions.base.segments.climb_2.air_speed'],
        ['c2_rate' , 'missions.base.segments.climb_2.climb_rate'],

        ['c3_airspeed' , 'missions.base.segments.climb_3.air_speed'],
        ['c3_rate' , 'missions.base.segments.climb_3.climb_rate'],

        ['c4_airspeed' , 'missions.base.segments.climb_4.air_speed'],
        ['c4_rate' , 'missions.base.segments.climb_4.climb_rate'],

        ['c5_airspeed' , 'missions.base.segments.climb_5.air_speed'],
        ['c5_rate' , 'missions.base.segments.climb_5.climb_rate']
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
    nexus.missions = Missions.setup(nexus.analyses)
    
    
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
    nexus.procedure = Procedure.setup()
    
    # -------------------------------------------------------------------
    #  Summary
    # -------------------------------------------------------------------    
    nexus.summary = Data()    
    
    return nexus
    
def variable_sweep(problem):    
    number_of_points=5
    outputs=carpet_plot(problem, number_of_points, 0, 0)  #run carpet plot, suppressing default plots
    inputs =outputs.inputs
    objective=outputs.objective
    constraints=outputs.constraint_val
    plt.figure(0)
    CS = plt.contourf(inputs[0,:],inputs[1,:], objective, 20, linewidths=2)
    cbar = plt.colorbar(CS)
    
    cbar.ax.set_ylabel('fuel burn (kg)')
    CS_const=plt.contour(inputs[0,:],inputs[1,:], constraints[0,:,:])
    plt.clabel(CS_const, inline=1, fontsize=10)
    cbar = plt.colorbar(CS_const)
    cbar.ax.set_ylabel('fuel margin')
    
    
    
    plt.xlabel('wing area (m^2)')
    plt.ylabel('cruise_altitude (km)')
    
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
    plt.show()    
    
      

    return
    

if __name__ == '__main__':
    main()
    
    
