import numpy as np

class receptorGrid:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.yMesh,self.zMesh,self.xMesh = np.meshgrid(y,z,x)
    
class pointSource:
    def __init__(self,x,y,z,rate,H):
        self.x = x
        self.y = y
        self.z = z
        self.rate = rate
        self.H = H
        self.sourceType = 'point'

class areaSource:
    def __init__(self,x0,dx,nx,y0,dy,ny,z,rate,H):
        self.x = np.linspace(x0,nx*dx,nx+1)
        self.y = np.linspace(y0,ny*dy,ny+1)
        self.z = z
        self.sourceType = 'area'
        self.yMesh,self.zMesh,self.xMesh = np.meshgrid(self.y,z,self.x)
        self.H = H
        self.rate = rate
        self.dx = dx
        self.dy = dy

class stabilityClass:
    def __init__(self,letter):
        self.letter = letter

        
        if letter == 'A':
            Iy = -1.104
            Jy = 0.9878
            Ky = -0.0076

            Iz = 4.679
            Jz = -1.7172
            Kz = 0.2770

        elif letter == 'B':
            Iy = -1.634
            Jy = 1.0350
            Ky = -0.0096

            Iz = -1.999
            Jz = 0.8752
            Kz = 0.0136

        elif letter == 'C':
            Iy = -2.054
            Jy = 1.0231
            Ky = -0.0076

            Iz = -2.341
            Jz = 0.9477
            Kz = -0.0020

        elif letter == 'D':
            Iy = -2.555
            Jy = 1.0423
            Ky = -0.0087

            Iz = -3.186
            Jz = 1.1737
            Kz = -0.0316

        elif letter_ == 'E':
            Iy = -2.754 
            Jy = 1.0106
            Ky = -0.0064

            Iz = -3.783
            Jz = 1.3010
            Kz = -0.0450

        elif letter == 'F':
            Iy = -3.143
            Jy = 1.0148
            Ky = -0.0070

            Iz = -4.490
            Jz = 1.4024
            Kz = -0.0540

        def sy(dist):
            return np.exp(Iy + Jy*np.log(dist) + Ky*(np.log(dist)**2))

        def sz(dist):
            return np.exp(Iz + Jz*np.log(dist) + Kz*(np.log(dist)**2))

        self.sz = sz
        self.sy = sy

class gaussianPlume:
    def __init__(self,source,grid,stability,U):
        self.grid = grid
        self.source = source
        self.stability = stability
        self.U = U

    def calculateConcentration(self):
        conc = np.zeros_like(self.grid.xMesh,dtype=float)

        if self.source.sourceType == 'area':
            for x in self.source.x:
                for y in self.source.y:
                        a = self.source.rate*self.source.dx*self.source.dy / (2 * np.pi * self.U * self.stability.sy(self.grid.xMesh -x) * self.stability.sz(self.grid.xMesh - x))
                        b = np.exp(-(self.grid.yMesh - y)**2/(2*self.stability.sy(self.grid.xMesh -x)**2))
                        c = np.exp(-(self.grid.zMesh-self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2)) + np.exp(-(self.grid.zMesh+self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2))
                        conc += a*b*c


        if self.source.sourceType == 'point':
            x = self.source.x
            y = self.source.y
            a = self.source.rate / (2 * np.pi * self.U * self.stability.sy(self.grid.xMesh -x) * self.stability.sz(self.grid.xMesh - x))
            b = np.exp(-(self.grid.yMesh - y)**2/(2*self.stability.sy(self.grid.xMesh -x)**2))
            c = np.exp(-(self.grid.zMesh-self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2)) + np.exp(-(self.grid.zMesh+self.source.H)**2/(2*self.stability.sz(self.grid.xMesh - x)**2))
            conc += a*b*c



        return conc
