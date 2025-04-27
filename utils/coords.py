import mpmath
from mpmath import mpf
import numpy as np

def tcoord(E,N):
    # help function
    Z = 0.0
    N = mpf(N)
    E = mpf(E)
    sin = mpmath.sin
    cos = mpmath.cos
    tan = mpmath.tan
    atan = mpmath.atan
    lat = 0
    lon = 0
    B = mpmath.radians(lat)
    L = mpmath.radians(lon)
    def decdeg2dms(dd):
        dd = float(dd)
        is_positive = dd >= 0
        dd = abs(dd)
        minutes,seconds = divmod(dd*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        seconds = round(seconds,4)
        return (degrees,minutes,seconds)


    # constant
    a = mpf(6378245.000) # meter # велика піввісь еліпса
    f = mpf(1.0)/298.3 # стиснення еліпса
    b = a - a*f
    e = mpmath.sqrt((a**2-b**2)/a**2)
    e_2 = mpmath.sqrt((a**2-b**2)/b**2) # e'
    B0 = 0                  # fi0
    L0 = mpmath.radians(29.5) # lambda0
    FN = mpf(-9214.6880) #meter
    FE = 0.0 #meter

    # Перевірка зони
    zone = int(E/1000000)
    l = 0

    #=IF(D5=1,RADIANS(23.5),IF(D5=2,RADIANS(26.5),IF(D5=3,RADIANS(29.5),IF(D5=4,RADIANS(32.5),IF(D5=5,RADIANS(35.5),IF(D5=6,RADIANS(38.5),""))))))
    try:
        if zone == 1:
            l = 23.5
        elif zone == 2:
            l = 26.5
        elif zone == 3:
            l = 29.5
        elif zone == 4:
            l = 32.5
        elif zone == 5:
            l = 35.5
        elif zone == 6:
            l = 38.5
    except NameError:
       print( NameError, u"error: Координати не містять номера зони СК64, за потреби зверніться до Автора Програми: pavlo.dazru@gmail.com")

    #=IF(D5=1,1300000,IF(D5=2,2300000,IF(D5=3,3300000,IF(D5=4,4300000,IF(D5=5,5300000,IF(D5=6,6300000,""))))))
    try:
        if zone == 1:
            FE = 1300000.0
        elif zone == 2:
            FE = 2300000.0
        elif zone == 3:
            FE = 3300000.0
        elif zone == 4:
            FE = 4300000.0
        elif zone == 5:
            FE = 5300000.0
        elif zone == 6:
            FE = 6300000.0
    except NameError:
       print( NameError, u"error: Координати не містять номера зони СК64, за потреби зверніться до Автора Програми: pavlo.dazru@gmail.com")
    FN = mpf(FN)
    FE = mpf(FE)
    l  = mpf(l)


    L0 = mpmath.radians(l)
    k0 = 1.0
    M1 = N - FN
    m1 = M1 / (a*(1-(e**2/4)-(3*(e**4/64))-(5*(e**6/256))))
    e1 = (1-mpmath.sqrt(1-e**2))/(1+mpmath.sqrt(1-e**2))
    B1 = m1 + ((3*e1/2)-(27*e1**3/32))*sin(2*m1)+((21*e1**2/16)-(55*e1**4/32))*sin(4*m1)+(151*(e1**3/96)*sin(6*m1))+((1097*e1**4/512)*sin(8*m1))
    T1 = tan(B1)**2
    C1 = e_2**2*(cos(B1)**2)
    V1 = a / (mpmath.sqrt(1-e**2*(sin(B1)**2)))
    p1 = (a*(1-e**2))/(1-e**2*(sin(B1)**2))**1.5
    D = (E-FE)/(V1*k0)
    Bsk42_rad = B1-((V1*tan(B1))/p1)*(((D**2)/2)-(((5+3*T1+10*C1-4*C1**2-9*e_2**2)*D**4)/24)+(((61+90*T1+298*C1+45*T1**2-252*e_2**2)*D**6)/720))
    Lsk42_rad = L0 + ((D-((1+2*T1+C1)*D**3)/6)+((5-2*C1+28*T1-3*C1**2+8*e_2**2+24*T1**2)*(D**5)/120))/cos(B1)
    #=D13+(D27-(1+2*D23+D24)*POWER(D27,3)/6+(5-2*D24+28*D23-3*POWER(D24,2)+8*POWER(D11,2)+24*POWER(D23,2))*POWER(D27,5)/120)/COS(D22)
    Bsk42_ddeg = mpmath.degrees(Bsk42_rad)
    Lsk42_ddeg = mpmath.degrees(Lsk42_rad)

    # Перевірка заокруглень до еселя

    # print( "L0", round(L0,15)-float(0.51487212933832700000), L0
    # print( "D ", round(D,16)  - mpf(0.01110154954724890000), D
    # print( "T1", round(T1,14)  -mpf(1.47205393116797000000), T1
    # print( "C1", round(C1,16)  -mpf(0.00272588123168480000), C1
    # print( "e_2", round(e_2,16) -mpf(0.08208852182055300000), e_2
    # print( "cos(B1)", round(cos(B1),15) -mpf(0.63602037621171300000), cos(B1)
    # print( Bsk42_rad, '\t', Lsk42_rad
    # print( round(Bsk42_rad,15)-0.88139127223893300000,'\t\t\t\t', round(Lsk42_rad,15)-0.53232542185590200000
    # print( Bsk42_ddeg, Lsk42_ddeg
    # print( round(Bsk42_ddeg,15)-50.49999999895700000000, round(Lsk42_ddeg,13)-30.49999999986430000000
    # print( "Lsk42", decdeg2dms(Lsk42_ddeg)
    # print( "Bsk42", decdeg2dms(Bsk42_ddeg)
    #print( Btemp[0],Btemp[1], Btemp[2]


    #  # # # # # # # # # включити заокруглення
    # Bg = int(Bsk42_ddeg); Bminut = round((Bsk42_ddeg-Bg)*60,0); Bsec = round((60*(Bsk42_ddeg-Bg)-Bminut)*60,4)
    # Lg = int(Lsk42_ddeg); Lminut = round((Lsk42_ddeg-Lg)*60,0); Lsec = round((60*(Lsk42_ddeg-Lg)-Lminut)*60,4)
    # Bround = Bg + Bminut/60 + Bsec/3600
    # Lround = Lg + Lminut/60 + Lsec/3600
    # B = mpmath.radians(Bround)
    # L = mpmath.radians(Lround)


    #print( Bg, Bminut, Bsec
    #print( Lg, Lminut, Lsec
    #print( Bround
    #print( Lround

    # # Якшо не коментоване заокрулгення вимкнуте
    B = Bsk42_rad
    L = Lsk42_rad


    # Крок 2 конвертація B,L до X,Y,Z
     #=D9/SQRT((1-POWER(D12,2)*POWER(SIN(D4),2)))
    V = a / (mpmath.sqrt(1-(e**2*(sin(B)**2))))
    #print( "V" , round(V,8)-6390992.7038410900, V

    X = V*cos(B)*cos(L)
    Y = V*cos(B)*sin(L)
    Z = ((1-e**2)*V)*sin(B)

    # Перевірка заокруглень
    # print( "type x", type(X), type(Y)
    # print( "x", round(X,8)-3502670.1039987200, X
    # print( "y", round(Y,8)-2063230.3689257000, Y
    # print( "z", round(Z,8)-4898438.8280005800, Z


    # Крок 3 застосування трансформації Гельмерта

    # Параметри трансформації
    tX = 30.918
    tY = -119.346
    tZ = -93.514
    rX = mpmath.radians(-0.636831/3600)
    rY = mpmath.radians(0.242067/3600)
    rZ = mpmath.radians(-0.56995/3600)
    m = 0.00000009

    XYZsk42 = np.matrix([X,Y,Z])
    Helm = np.matrix([[m,-rZ,+rY],[+rZ,m,-rX],[-rY,+rX,m]])
    dDelta = np.matrix([tX,tY,tZ])
    XYZwgs = XYZsk42 + XYZsk42*Helm + dDelta
    Xwgs = XYZwgs.item((0,0))
    Ywgs = XYZwgs.item((0,1))
    Zwgs = XYZwgs.item((0,2))

    # Перевірка заокруглень
    # print( "Xwgs", round(Xwgs,8)-3502689.88744988000, Xwgs
    # print( "Ywgs", round(Ywgs,8)-2063105.76352431000, Ywgs
    # print( "Zwgs", round(Zwgs,8)-4898356.23561025000, Zwgs



    # Крок 4 Конвертація X,Y,Z до B,L
    aWGS = 6378137.0000
    fWGS = 1/298.2572236
    bWGS = aWGS - aWGS*fWGS
    eWGS = mpmath.sqrt((aWGS**2-bWGS**2)/aWGS**2)
    eWGS_2 = mpmath.sqrt((aWGS**2-bWGS**2)/bWGS**2)
    ePSL = eWGS**2/(1-eWGS**2)
    p = mpmath.sqrt(Xwgs**2+Ywgs**2)
    q = atan((Zwgs*aWGS)/(p*bWGS))
    Bwgs_rad = atan((Zwgs+ePSL*bWGS*(sin(q))**3)/(p-(eWGS**2)*aWGS*(cos(q)**3)))
    Bwgs = mpmath.degrees(Bwgs_rad)
    Lwgs_rad = atan(Ywgs/Xwgs)
    Lwgs = mpmath.degrees(Lwgs_rad)

    # print( N, E, Bwgs, Lwgs
    # print( decdeg2dms(Bwgs), decdeg2dms(Lwgs)
    return ([round(Lwgs,13),round(Bwgs,13),0.0,zone])

def sc63_to_wgs84(x, y):
    lon, lat, _, zone = tcoord(x, y)
    return lat, lon, zone