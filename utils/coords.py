# --- coords.py ---

import mpmath
from mpmath import mpf
import numpy as np

def tcoord(E, N):
    """
    Perform conversion from SC63 (local projection) coordinates to SK-42 intermediate system.

    Args:
        E (float): Easting coordinate in meters (SC63).
        N (float): Northing coordinate in meters (SC63).

    Returns:
        list: [longitude (deg), latitude (deg), 0.0, zone number]
    """
    # Constants
    a = mpf(6378245.000)  # Semi-major axis
    f = mpf(1.0) / 298.3  # Flattening
    b = a - a * f
    e = mpmath.sqrt((a**2 - b**2) / a**2)
    e_2 = mpmath.sqrt((a**2 - b**2) / b**2)
    k0 = 1.0

    # Define zone
    zone = int(E / 1000000)
    l = 0.0
    if zone == 1:
        l = 23.5
        FE = 1300000.0
    elif zone == 2:
        l = 26.5
        FE = 2300000.0
    elif zone == 3:
        l = 29.5
        FE = 3300000.0
    elif zone == 4:
        l = 32.5
        FE = 4300000.0
    elif zone == 5:
        l = 35.5
        FE = 5300000.0
    elif zone == 6:
        l = 38.5
        FE = 6300000.0
    else:
        l = 29.5  # Default central meridian
        FE = 0.0  # Default false easting

    FN = mpf(-9214.6880)  # False northing
    FE = mpf(FE)
    l = mpf(l)

    L0 = mpmath.radians(l)

    # Auxiliary calculations
    sin = mpmath.sin
    cos = mpmath.cos
    tan = mpmath.tan
    atan = mpmath.atan

    # Step 1: Calculate latitude/longitude in SK-42
    M1 = mpf(N) - FN
    m1 = M1 / (a * (1 - (e**2 / 4) - (3 * (e**4) / 64) - (5 * (e**6) / 256)))
    e1 = (1 - mpmath.sqrt(1 - e**2)) / (1 + mpmath.sqrt(1 - e**2))
    B1 = m1 + ((3 * e1 / 2) - (27 * e1**3 / 32)) * sin(2 * m1) + \
         ((21 * e1**2 / 16) - (55 * e1**4 / 32)) * sin(4 * m1) + \
         (151 * (e1**3 / 96)) * sin(6 * m1) + \
         (1097 * (e1**4 / 512)) * sin(8 * m1)

    T1 = tan(B1)**2
    C1 = e_2**2 * (cos(B1)**2)
    V1 = a / (mpmath.sqrt(1 - e**2 * (sin(B1)**2)))
    p1 = (a * (1 - e**2)) / (1 - e**2 * (sin(B1)**2))**1.5
    D = (mpf(E) - FE) / (V1 * k0)

    Bsk42_rad = B1 - ((V1 * tan(B1)) / p1) * ((D**2 / 2) - ((5 + 3 * T1 + 10 * C1 - 4 * C1**2 - 9 * e_2**2) * D**4 / 24) + ((61 + 90 * T1 + 298 * C1 + 45 * T1**2 - 252 * e_2**2) * D**6 / 720))
    Lsk42_rad = L0 + (D - (1 + 2 * T1 + C1) * D**3 / 6 + (5 - 2 * C1 + 28 * T1 - 3 * C1**2 + 8 * e_2**2 + 24 * T1**2) * D**5 / 120) / cos(B1)

    Bsk42_ddeg = mpmath.degrees(Bsk42_rad)
    Lsk42_ddeg = mpmath.degrees(Lsk42_rad)

    # Step 2: Convert to Cartesian coordinates (X, Y, Z)
    V = a / (mpmath.sqrt(1 - (e**2 * sin(Bsk42_rad)**2)))

    X = V * cos(Bsk42_rad) * cos(Lsk42_rad)
    Y = V * cos(Bsk42_rad) * sin(Lsk42_rad)
    Z = (1 - e**2) * V * sin(Bsk42_rad)

    # Step 3: Apply Helmert transformation to WGS84
    tX, tY, tZ = 30.918, -119.346, -93.514
    rX = mpmath.radians(-0.636831 / 3600)
    rY = mpmath.radians(0.242067 / 3600)
    rZ = mpmath.radians(-0.56995 / 3600)
    m = 0.00000009

    XYZsk42 = np.matrix([X, Y, Z])
    Helm = np.matrix([[m, -rZ, rY], [rZ, m, -rX], [-rY, rX, m]])
    dDelta = np.matrix([tX, tY, tZ])

    XYZwgs = XYZsk42 + XYZsk42 * Helm + dDelta
    Xwgs = XYZwgs.item((0, 0))
    Ywgs = XYZwgs.item((0, 1))
    Zwgs = XYZwgs.item((0, 2))

    # Step 4: Convert (X, Y, Z) to (lat, lon)
    aWGS = 6378137.0000
    fWGS = 1 / 298.2572236
    bWGS = aWGS - aWGS * fWGS
    eWGS = mpmath.sqrt((aWGS**2 - bWGS**2) / aWGS**2)
    ePSL = eWGS**2 / (1 - eWGS**2)

    p = mpmath.sqrt(Xwgs**2 + Ywgs**2)
    q = atan((Zwgs * aWGS) / (p * bWGS))
    Bwgs_rad = atan((Zwgs + ePSL * bWGS * (sin(q))**3) / (p - eWGS**2 * aWGS * (cos(q))**3))

    Bwgs = mpmath.degrees(Bwgs_rad)
    Lwgs = mpmath.degrees(atan(Ywgs / Xwgs))

    return [round(Lwgs, 13), round(Bwgs, 13), 0.0, zone]

def sc63_to_wgs84(x, y):
    """
    Wrapper function to convert SC63 coordinates to WGS84.

    Args:
        x (float): Easting coordinate.
        y (float): Northing coordinate.

    Returns:
        tuple: (latitude, longitude, zone number)
    """
    lon, lat, _, zone = tcoord(x, y)
    return lat, lon, zone
