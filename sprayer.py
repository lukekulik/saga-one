import numpy as np

def update_weights_sprayer(segment,state):

    # unpack
    conditions = state.conditions
    m0        = conditions.weights.total_mass[0,0]
    m_empty   = segment.analyses.weights.mass_properties.operating_empty
    mdot_fuel = conditions.weights.vehicle_mass_rate
    I         = state.numerics.time.integrate
    g         = conditions.freestream.gravity
    # add some global counter of spray mass

    # Add in the sprayer mass rate
    if hasattr(segment, 'distance'):
        segment.sprayer_rate=segment.sprayer_rate = segment.aerosol_mass_initial/ ((segment.distance / segment.air_speed ))
    elif hasattr(segment,'sprayrate_override'):
        segment.sprayer_rate=segment.sprayrate_override
    else:
        segment.sprayer_rate=0.0


    sprayer   = segment.sprayer_rate * state.ones_row(1)

    # Integrate the masses
    fuel  = np.dot(I, mdot_fuel )
    spray = np.dot(I, sprayer )

    # calculate
    m = m0 - fuel - spray

    # weight
    W = m*g

    # pack
    conditions.weights.total_mass[1:,0]                  = m[1:,0] # don't mess with m0
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    # pack sprayer mass and fuel burn
    conditions.weights.fuel_burn = fuel
    conditions.weights.spray     = spray
    conditions.weights.sprayer = sprayer

    return