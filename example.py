import numpy as np
import matplotlib.pyplot as plt
import gaussianPlume

rate = 1. # g/s/m2
H = 0. # m
U = 5. # m/s
xGrid = np.linspace(0,2000,100) # m
yGrid = np.linspace(-500,500,100) # m
zGrid = 10. #m

areaSource = gaussianPlume.areaSource(0,1,50,-100,10,20,0,rate,H)
pointSource = gaussianPlume.pointSource(0,0,0,rate,H)
grid = gaussianPlume.receptorGrid(xGrid,yGrid,zGrid)
stability = gaussianPlume.stabilityClass('C')

a = gaussianPlume.gaussianPlume(areaSource,grid,stability,U)

concField = a.calculateConcentration()

fig = plt.figure()
ax = fig.add_subplot(111)
c = ax.contourf(grid.xMesh[0],grid.yMesh[0],concField[0],100)
cb = fig.colorbar(c)
cb.set_label('Concentration g/m3')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
fig.show()
