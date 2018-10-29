import numpy as np
import math

amp=1.66
damp=0.02
ch=270-52
dch=4

a=7.476e-04
b=5.63513e-03
A=np.array([7.01154,7.45483,7.400228])
A=A*0.0001
depth_Al=np.array([1.25789,1.24060,0.539121])
depth_Al=depth_Al*0.01
dA=(A-a)*(A-a)
dB=(depth_Al-b)*(depth_Al-b)
sigma_a=math.sqrt(np.sum(dA)/dA.shape[0])
sigma_b=math.sqrt(np.sum(dB)/dB.shape[0])
print("a={:e}+-{:e}".format(a,sigma_a))
print("depth_Al={:e}+-{:e}".format(b,sigma_b))
c=3.28325e-02
C=np.array([7.87581,7.9834,3.57659])
C=C*0.01
dc=(C-c)*(C-c)
sigma_c=math.sqrt(np.sum(dc)/dc.shape[0])
print("depth_CH={:e}+-{:e}".format(c,sigma_c))

Eth=a/amp*ch
dEth=math.sqrt((ch/amp*sigma_a)**2+(a*ch/(amp*amp)*damp)**2+(a/amp*dch)**2)
print("Eth={}+-{}".format(Eth,dEth))
