import numpy as np

def update_weights_sprayer(segment,state):

    # unpack
    conditions = state.conditions
    m0        = conditions.weights.total_mass[0,0]
    m_empty   = segment.analyses.weights.mass_properties.operating_empty
    mdot_fuel = conditions.weights.vehicle_mass_rate
    I         = state.numerics.time.integrate
    g         = conditions.freestream.gravity

    # Add in the sprayer mass rate
    sprayer   = segment.sprayer_rate
    mdot      = mdot_fuel + sprayer

    # calculate
    m = m0 + np.dot(I, -mdot )

    # weight
    W = m*g

    # pack
    conditions.weights.total_mass[1:,0]                  = m[1:,0] # don't mess with m0
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    return