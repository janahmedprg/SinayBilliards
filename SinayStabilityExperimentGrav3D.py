import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

pi=np.pi

def cos(x):
    return np.cos(x)

def sin(x):
    return np.sin(x)

def make_ngon(n):
    if n == 4:
        return ([1, 1, -1, -1, 1],[-1, 1, 1, -1, -1])
    # Makes the heaxagonal bounds
    tabX=[1]
    tabY=[0]
    for i in range(1,n+1):
        tabX+=[np.cos(i*2*np.pi/n)]
        tabY+=[np.sin(i*2*np.pi/n)]
    # print(tabX)
    # print(tabY)
    return (tabX,tabY)

def getLines(tabX,tabY,n):
    # Gets the vertices and vectors of the hexagonal table for plotting
    lineEqs=[]
    for i in range(0,n):
        vX=tabX[i+1]-tabX[i]
        vY=tabY[i+1]-tabY[i]
        lineEqs.append([tabX[i],tabY[i],vX,vY])
    return lineEqs

def mat_mul(Rinv,T,R,vX,vY,vS):
    # Matrix multiplication function
    V=[[vS],[vX],[vY]]
    V= np.matmul(R,V)
    V = np.matmul(T,V)
    V = np.matmul(Rinv,V)
    return (float(V[1][0]),float(V[2][0]),float(V[0][0]))

def rotate(x):
    # Creates a rotational matrix
    return np.matrix([[1,0,0],[0,cos(x),sin(x)],[0,-sin(x),cos(x)]],dtype=float)

def reflect(pX,pY,vX,vY,vS,type):
    # No-slip reflection on the disperser
    if type == 0:
        Tr = [[-cos(eta*pi),sin(eta*pi),0],[sin(eta*pi),cos(eta*pi),0],[0,0,-1]]
        if pX==0 and pY>0:
            Rinv=rotate(0)
            R=rotate(0)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        elif pX==0 and pY<0:
            Rinv=rotate(-np.pi)
            R=rotate(np.pi)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        else:
            if (pX>0 and pY>=0):
                normalAng=np.arctan(pY/pX)
            elif(pX<0 and pY>=0):
                normalAng=np.pi+np.arctan(pY/pX)
            elif (pX<0 and pY<=0):
                normalAng=np.pi+np.arctan(pY/pX)
            else:
                normalAng=2*np.pi+np.arctan(pY/pX)
            Rinv=rotate(np.pi/2-normalAng)
            R=rotate(normalAng-np.pi/2)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        return (vX,vY,vS,1)
    else:
        pX=pX-2
        Tr = [[-cos(eta*pi),sin(eta*pi),0],[sin(eta*pi),cos(eta*pi),0],[0,0,-1]]
        if pX==0 and pY>0:
            Rinv=rotate(0)
            R=rotate(0)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        elif pX==0 and pY<0:
            Rinv=rotate(-np.pi)
            R=rotate(np.pi)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        else:
            if (pX>0 and pY>=0):
                normalAng=np.arctan(pY/pX)
            elif(pX<0 and pY>=0):
                normalAng=np.pi+np.arctan(pY/pX)
            elif (pX<0 and pY<=0):
                normalAng=np.pi+np.arctan(pY/pX)
            else:
                normalAng=2*np.pi+np.arctan(pY/pX)
            Rinv=rotate(np.pi/2-normalAng)
            R=rotate(normalAng-np.pi/2)
            (vX,vY,vS)=mat_mul(Rinv,Tr,R,vX,vY,vS)
        return (vX,vY,vS,0)


def BilliardIte(pX,pY,vX,vY,vS,r,isTorus,time,disp,type):
    bestTime=1000
    bestTime1=1000

    if(not isTorus):
        # if we pass in a point on the disperser we call reflect
        vX,vY,vS,type=reflect(pX,pY,vX,vY,vS,type)

    # This checks the collision with the disperser by solving for time t
    # We will have 4 different times because we have a parabolic trajectory

    if disp == 0:
        coeff=[0.25*(gravity**2),-vY*gravity,-pY*gravity+vX**2+vY**2,2*pX*vX+2*pY*vY,pX**2+pY**2-r**2]
        intersect = np.roots(coeff)
        for ti in intersect:
            if np.iscomplex(ti) or ti<10**(-9):
                continue
            ti = float(ti.real)
            if ti < bestTime:
                bestTime = ti
                bestxTravel=[]
                bestyTravel=[]
                for j in np.linspace(0,ti,10*int(math.exp(ti))):
                    bestxTravel.append(pX + vX*j)
                    bestyTravel.append(pY + vY*j - 0.5*(j**2)*gravity)
                bestPx = pX + vX*ti
                bestPy = pY + vY*ti - 0.5*(ti**2)*gravity

    elif disp == 1:
        coeff1=[0.25*(gravity**2),-vY*gravity,-pY*gravity+vX**2+vY**2,2*pX*vX+2*pY*vY-4*vX,pX**2+pY**2-r**2-4*pX+4]
        intersect1 = np.roots(coeff1)
        for ti in intersect1:
            if np.iscomplex(ti) or ti<10**(-9):
                continue
            ti = float(ti.real)
            if ti < bestTime1:
                bestTime1 = ti
                bestxTravel=[]
                bestyTravel=[]
                for j in np.linspace(0,ti,10*int(math.exp(ti))):
                    bestxTravel.append(pX + vX*j)
                    bestyTravel.append(pY + vY*j - 0.5*(j**2)*gravity)
                bestPx = pX + vX*ti
                bestPy = pY + vY*ti - 0.5*(ti**2)*gravity

    if disp == 0 and bestTime>10**(-9) and bestTime != 1000:
        time+=bestTime
        return (bestPx,bestPy,vX,vY-bestTime*gravity,vS,False,time,bestxTravel,bestyTravel,1,type)
    elif disp == 1 and bestTime1>10**(-9) and bestTime1 != 1000:
        time+=bestTime1
        return (bestPx,bestPy,vX,vY-bestTime1*gravity,vS,False,time,bestxTravel,bestyTravel,0,type)
    else:
        return (0,0,0,0,0,False,0,0,0,-1,type)


def torus(pX,pY,wall):
    # Makes the torus effect. Instead of reflecting it starts on the opposite side of the hexagonal bounds.
    if(isTorus):
        if(wall==1 or wall==4):
            pY=-pY
            if wall==1:
                wall=4
            else:
                wall=1
        elif(wall==0 or wall==3):
            rDis=(pX**2+pY**2)**0.5
            if wall==0:
                ang=np.arctan(pY/pX)
                pX=rDis*np.cos(4/3*np.pi-ang)
                pY=rDis*np.sin(4/3*np.pi-ang)
                wall=3
            else:
                ang=np.arctan(pY/pX)
                pX=rDis*np.cos(1/3*np.pi-ang)
                pY=rDis*np.sin(1/3*np.pi-ang)
                wall=0
        elif(wall==2 or wall==5):
            rDis=(pX**2+pY**2)**0.5
            if wall==2:
                ang=np.arctan(pY/pX)
                pX=rDis*np.cos(10/6*np.pi-ang)
                pY=rDis*np.sin(10/6*np.pi-ang)
                wall=5
            else:
                ang=np.arctan(pY/pX)
                pX=rDis*np.cos(2/3*np.pi-ang)
                pY=rDis*np.sin(2/3*np.pi-ang)
                wall=2

        else:
            print("WARNING: VERTEX HIT")
    return (pX,pY,wall)

def box(pX,pY,wall):
    # Makes the torus effect. Instead of reflecting it starts on the opposite side of the hexagonal bounds.
    if(wall==0 or wall==2):
        pX=-pX
        if wall==0:
            wall=2
        else:
            wall=0
    elif(wall==1 or wall==3):
        pY=-pY
        if wall==1:
            wall=3
        else:
            wall=1
    else:
        print("WARNING: VERTEX HIT")
    return (pX,pY,wall)

def getXYAng(r,epsilon,n):
    # Gets initial positions with angles.
    xyPos=[[],[],[],[]]
    for sang in np.linspace(0.1,np.pi/2-0.2,n):
        for phi in np.linspace(0.1,np.pi/2-0.2,n):
            x=r*cos(phi)
            y=r*sin(phi)
            if(y<0):
                y-=epsilon
            else:
                y+=epsilon

            xyPos[0].append(x)
            xyPos[1].append(y)
            xyPos[2].append(sang)
            xyPos[3].append(phi)
    return xyPos
################################################################################
################################ Interact ######################################
################################################################################
r=0
sides=4
eta= np.arccos(1/3)/np.pi
N=10
grid=10
perturbation = 0.01
gravity = 1
################################################################################
################################################################################
epsilon=0.0001
########################## TRAJECTORY MAP ######################################


fname='sinayGravExp('+str(round(eta,3))+')_p'+str(round(perturbation,3))+'_grid' + str(grid)+'_maxIte'+str(N)+'3d'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
data = np.zeros((4,grid*grid*grid))
rAx = np.linspace(0,0.99,grid) #start and end needs to be same as in r in linspace below steps needs to be +1


idx=0

for r in rAx:
    xyang=getXYAng(r,epsilon,grid)
    for px,py,startAng,phiAng in zip(xyang[0],xyang[1],xyang[2],xyang[3]):
        h = (1-px)
        speed = ((2*gravity*h)/np.sin(2*startAng))**0.5
        pX=px
        pY=py
        vX=speed*np.cos(startAng)
        vY=speed*np.sin(startAng)
        vS=(speed/(((1-np.cos(np.pi*eta))/(np.cos(np.pi*eta)+1))**0.5))*(-np.cos(startAng)*np.sin(phiAng) + np.sin(startAng)*np.cos(phiAng)) + perturbation
        trajX=[]
        trajY=[]
        isTorus=True # Don't change unless we are starting on the disperses
        time=0
        disp = 1
        type = 1
        nCol = -1

        (tabX,tabY)=make_ngon(sides)
        tabLineEqs=getLines(tabX,tabY,sides)

        for i in range(0,N):
            (pX,pY,vX,vY,vS,isTorus,time,xTravel,yTravel,disp,type)=BilliardIte(pX,pY,vX,vY,vS,r,isTorus,time,disp,type)
            if disp == -1:
                nCol = i
                break
        if nCol == -1:
            nCol = N
        data[0][idx]=startAng
        data[1][idx]=phiAng
        data[2][idx]=r
        data[3][idx]=nCol/N
        idx+=1;

# print(data)
ax.scatter(xs=data[0],ys=data[1],zs=data[2],c=data[3])
############################## Save of Show ###################################
plt.savefig(fname+'.eps')
plt.show()
plt.close('all')
