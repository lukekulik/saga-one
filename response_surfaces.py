# SETS OF SWEEP PROBLEMS:

# SWEEP1: bypass, AR, fuel burn
# problem.optimization_problem.inputs = np.array([
#      # [ 'wing_area', 700    , (   400. ,   700.   ) ,   500. , Units.meter**2], # was 480 before
#      # ['MTOW', 160000., (160000.,160000.), 160000., Units.kg],
#      # ['wing_sweep', 0, (0,0),5,Units.less],
#      # ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#      # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#      ['AR',20,(5,20),10,Units.less],
#     ['bypass',6,(2,8.2),6,Units.less]])
#     #wing area, vs MTOW fuel weight for different
#     # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
#
# problem.optimization_problem.objective=np.array([
#     # [ 'Nothing', 1, Units.kg ]
#     # ['max_throttle', .8 ,Units.less],
#     [ 'fuel_burn',  36000, Units.kg ]
# ])
#
# problem.optimization_problem.constraints=np.array([
#            # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#     # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#     # constraint on mission time?
#     # ['max_throttle','<',1.1,1e-1,Units.less],
#     [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
# variable_sweep(problem,"Fuel burn [kg]", "unknown","Aspect ratio","Bypass ratio","BAT")

# # SWEEP2: bypass, AR, engine mass
# problem.optimization_problem.inputs = np.array([
#      # [ 'wing_area', 700    , (   400. ,   700.   ) ,   500. , Units.meter**2], # was 480 before
#      # ['MTOW', 160000., (160000.,160000.), 160000., Units.kg],
#      # ['wing_sweep', 0, (0,0),5,Units.less],
#      # ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#      # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#      ['AR',20,(5,20),10,Units.less],
#     ['bypass',6,(2,8.2),6,Units.less]])
#     #wing area, vs MTOW fuel weight for different
#     # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
#
# problem.optimization_problem.objective=np.array([
#     # [ 'Nothing', 1, Units.kg ]
#     # ['max_throttle', .8 ,Units.less],
#     [ 'oew',  66000, Units.kg ]
# ])
#
# problem.optimization_problem.constraints=np.array([
#            # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#     # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#     # constraint on mission time?
#     # ['max_throttle','<',1.1,1e-1,Units.less],
#     [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
# variable_sweep(problem,"OEW [kg]", "unknown","Aspect ratio","Bypass ratio","BAOEW")

#     # SWEEP3: bypass, AR, engine mass
#     problem.optimization_problem.inputs = np.array([
#          [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#          # ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#          # ['AR',20,(5,20),10,Units.less],
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'fuel_burn',  36000, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
#     variable_sweep(problem,"Fuel burn [kg]", "unknown","Wing area","MTOW","MTOWS")

#     # SWEEP4: bypass, AR, engine mass
#     problem.optimization_problem.inputs = np.array([
#          # [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          ['AR',20,(5,20),10,Units.less],
#          ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#          # ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'fuel_burn',  36000, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
#     variable_sweep(problem,"Fuel burn [kg]", "unknown","Aspect ratio","MTOW","MTOWA")

# SWEEP5: bypass, AR, engine mass
#     problem.optimization_problem.inputs = np.array([
#          [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          # ['AR',20,(5,20),10,Units.less],
#          # ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#          ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'fuel_burn',  36000, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel


#     # SWEEP6: bypass, AR, engine mass
#     problem.optimization_problem.inputs = np.array([
#          [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          # ['AR',20,(5,20),10,Units.less],
#          # ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#         ['oswald',0.75, (0.5,1),0.75, Units.less],
#          # ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'fuel_burn',  36000, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
#     variable_sweep(problem,"Fuel burn [kg]", "unknown","Wing area [$m^2$]","Oswald factor [-]","oswald-area")


#     # SWEEP7: bypass, AR, engine mass
#     problem.optimization_problem.inputs = np.array([
#          [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          # ['AR',20,(5,20),10,Units.less],
#          # ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#         # ['oswald',0.75, (0.5,1),0.75, Units.less],
#          ['cruise_speed', 681., (600., 900.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'max_throttle',  0.9, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'design_range_fuel_margin' , '>', 0., 1E-1, Units.less]]) #fuel margin defined here as fuel
#
#     variable_sweep(problem,"Max. thrust required (95kN baseline) [%]", "unknown","Wing area [$m^2$]","Cruise speed [km/h]","throttle-speed-area")

# SWEEP8: cruise alt, thrust req
#     problem.optimization_problem.inputs = np.array([
#          # [ 'wing_area', 700    , (   400. ,   800.   ) ,   500. , Units.meter**2], # was 480 before
#          # ['AR',20,(5,20),10,Units.less],
#          # ['MTOW', 160000., (130000.,250000.), 160000., Units.kg],
#         ['cruise_altitude',20, (17,21),20,Units.km],
#          # ['wing_sweep', 0, (0,0),5,Units.less],
#         # ['oswald',0.75, (0.5,1),0.75, Units.less],
#          ['cruise_speed', 681., (600., 800.), 500., Units['km/h'] ], #756
#          # ['return_cruise_alt', 19.2, (8., 20.), 10, Units.km ],
#
#         # ['bypass',6,(2,8.2),6,Units.less]])
#         #wing area, vs MTOW fuel weight for different
#         # ['return_cruise_speed', 750., (750., 806.), 500., Units['km/h'] ]])
# ])
#     problem.optimization_problem.objective=np.array([
#         # [ 'Nothing', 1, Units.kg ]
#         # ['max_throttle', .8 ,Units.less],
#         [ 'max_throttle',  0.9, Units.kg ]
#     ])
#
#     problem.optimization_problem.constraints=np.array([
#                # [ 'Nothing', '=', 0. ,1E-1, Units.kg]
#         # [ 'fuel_burn', '<', 40000, 1, Units.kg ]
#         # constraint on mission time?
#         # ['max_throttle','<',1.1,1e-1,Units.less],
#         [ 'fuel_burn' , '<', 40000., 1E-1, Units.less]]) #fuel margin defined here as fuel

# variable_sweep(problem,"Max. thrust required (115kN baseline) [%]", "Fuel burn [kg]","Cruise altitude [km]","Cruise speed [km/h]","altitude-throttle")
#