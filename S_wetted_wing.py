import math


def S_wet_w(filename,taper,S,b,c_r,sections,d_fus,y_fus,twin):
    f = open(filename, 'r')
    flines = f.readlines()
    for i in range(len(flines)):
        flines[i] = flines[i][:-1]
        flines[i] = flines[i].split()
        flines[i][0] = float(flines[i][0])
        flines[i][1] = float(flines[i][1])

    b_step = b/(2.*sections)
    theta = math.atan(2.*(1-taper)/b*c_r)
    b_i = 0.
    A_wet = 0.
    if twin == "ON":
        y_fus_in = y_fus - d_fus / 2
        y_fus_out = y_fus + d_fus / 2
    else:
        y_fus_in = 0.
        y_fus_out = d_fus/2
    for i in range(sections):
        c_i_prev = c_r - b_i*math.tan(theta)
        b_i += b_step
        if y_fus_in <= b_i < y_fus_out:
            A_j = 0.
        else:
            c_i = c_r-b_i*math.tan(theta)
            dist_i = 0.
            dist_i_prev = 0.
            A_j = 0.
            for j in range(len(flines)):
                 x_j_i = c_i*flines[j][0] #Current section, current point
                 x_j_prev_i = c_i*flines[j-1][0] #Current section, previous point
                 x_j_i_prev = c_i_prev*flines[j][0] #Previous section, current point
                 x_j_prev_i_prev = c_i_prev*flines[j-1][0] #Previous section, previous point
                 y_j_i = c_i*flines[j][1]
                 y_j_prev_i = c_i*flines[j-1][1]
                 y_j_i_prev = c_i_prev*flines[j][1]
                 y_j_prev_i_prev = c_i_prev*flines[j-1][1]
                 dist_j_i = math.sqrt((x_j_i-x_j_prev_i)**2+(y_j_i-y_j_prev_i)**2)
                 dist_j_i_prev = math.sqrt((x_j_i_prev-x_j_prev_i_prev)**2+(y_j_i_prev-y_j_prev_i_prev)**2)
                 A_j += b_step*(dist_j_i+dist_j_i_prev)/2
        A_wet+= A_j
    S_wet = 2*A_wet
    return S_wet

def S_wet_fus(d_fus,l_fus):
    S_wet_fus = math.pi*d_fus*(l_fus-1.3*d_fus)
    return S_wet_fus