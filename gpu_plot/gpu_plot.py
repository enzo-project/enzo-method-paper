import matplotlib.pyplot as plt

X = [1.0,2.0,4.0,8.0]
cpu = [1.92,3.94,7.73,14.0]
gpu = [11.73,28.44,46.93,55.0]

gpunode = []
cpunode = []

for n in range(len(cpu)):
    gpunode.append(1.0e6*gpu[n]/X[n])
    cpunode.append(1.0e6*cpu[n]/X[n])

print gpunode
print cpunode

plt.plot(X,cpunode,color='blue',linewidth=2.0,marker='o')
plt.plot(X,gpunode,color='red',linewidth=2.0,marker='o')
plt.loglog()
plt.axis([0,10,1e6,5e7])
plt.xlabel('N$_{node}$')
plt.ylabel('Cells/s/node')
plt.text(7.0, 2.0e7, 'CPU', size=15, color='blue')
plt.text(7.0, 3.0e7, 'GPU', size=15, color='red')
plt.savefig('gpu_scaling.eps')

