from numpy.fft import fft, fftshift
import math as mt
import numpy as np
import matplotlib.pyplot as plt

#константы
W0 = 120.0 * np.pi
Sc = 1.0
C = 300000000
maxSizeM = 0.8
dx = 5e-3
maxSize = mt.floor(maxSizeM / dx + 0.5)
d0M = 0.2
d1M = 0.21
d2M = 0.34
Fmin = 1e9
Fmax = 4e9
#Функции
def sampler(obj, dObj: float) -> int:
    return mt.floor(obj / dObj + 0.5)

def gaus(q, m, dG, wG, dT, eps=1, mu=1, Sc=1):
    return np.exp(-((((q - m*np.sqrt(eps*mu)/Sc)-(dG / dT)) / (wG / dt)) ** 2))
#основная часть кода
posL1min = sampler(d0M, dx)
posL2min = sampler(d0M + d1M, dx)
posL3min = sampler(d0M + d1M + d2M, dx)
eps = np.ones(maxSize)
eps[posL1min:posL2min] = 7.8
eps[posL2min:posL3min] = 4.2
eps[posL3min:] = 5.5
mu = 1.0
maxTimeS = 100e-9
dt = Sc * dx / C
maxTime = sampler(maxTimeS, dt)
tlist = np.arange(0, maxTime * dt, dt)
df = 1.0 / (maxTime * dt)
flist = np.arange(-maxTime / 2 * df, maxTime / 2 * df, df)
A0 = 100
Amax = 100
Fmax = 3e9
wg = np.sqrt(np.log(Amax)) / (np.pi * Fmax)
dg = wg * np.sqrt(np.log(A0))
sourcePosM = 0.1
sourcePos = mt.floor(sourcePosM / dx + 0.5)
probe1PosM = 0.05
probe1Pos = sampler(probe1PosM, dx)
probe1Ez = np.zeros(maxTime)
Ez = np.zeros(maxSize)
Hy = np.zeros(maxSize - 1)
Ez0 = np.zeros(maxTime)
Sc1 = Sc / np.sqrt(mu * eps)
k1 = -1 / (1 / Sc1 + 2 + Sc1)
k2 = 1 / Sc1 - 2 + Sc1
k3 = 2 * (Sc1 - 1 / Sc1)
k4 = 4 * (1 / Sc1 + Sc1)
prevEzL1 = np.zeros(3)
prevEzL2 = np.zeros(3)
prevEzR1 = np.zeros(3)
prevEzR2 = np.zeros(3)
for t in range(1, maxTime):
    Hy = Hy + (Ez[1:] - Ez[:-1]) * Sc / (W0 * mu)
    Hy[sourcePos - 1] -= (Sc / W0) * gaus(t, sourcePos, dg, wg, dt, eps=eps[sourcePos], mu=mu)
    Ez[1:-1] = Ez[1: -1] +  (Hy[1:] - Hy[: -1]) * Sc * W0 / eps[1: -1]
    Ez0[t] = Sc * gaus(t + 1, sourcePos, dg, wg, dt, eps=eps[sourcePos], mu=mu)
    Ez[sourcePos] += Ez0[t]
    Ez[0] = (k1[0] * (k2[0] * (Ez[2] + prevEzL2[0]) + k3[0] * (prevEzL1[0] + prevEzL1[2] - Ez[1] - prevEzL2[1]) - k4[0] * prevEzL1[1]) - prevEzL2[2])
    prevEzL2[:] = prevEzL1[:]
    prevEzL1[:] = Ez[0: 3]
    Ez[-1] = (k1[-1] * (k2[-1] * (Ez[-3] + prevEzR2[-1]) + k3[-1] * (prevEzR1[-1] + prevEzR1[-3] - Ez[-2] - prevEzR2[-2]) - k4[-1] * prevEzR1[-2]) - prevEzR2[-3])
    prevEzR2[:] = prevEzR1[:]
    prevEzR1[:] = Ez[-3:]
    probe1Ez[t] = Ez[probe1Pos]
Ez1Spec = fftshift(np.abs(fft(probe1Ez)))
Ez0Spec = fftshift(np.abs(fft(Ez0)))
Gama = Ez1Spec / Ez0Spec
#вывод графики
fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
ax0.set_xlim(0, 0.15 * maxTime * dt)
ax0.set_ylim(-0.6, 1.1)
ax0.set_xlabel('t, с')
ax0.set_ylabel('Ez, В/м')
ax0.plot(tlist, Ez0)
ax0.plot(tlist, probe1Ez)
ax0.legend(['Падающий сигнал', 'Отраженный сигнал'], loc='upper right')
ax0.minorticks_on()
ax0.grid()
ax1.set_xlim(Fmin, 1.5 * Fmax)
ax1.set_xlabel('f, Гц')
ax1.set_ylabel('|F{Ez}|, В*с/м')
ax1.plot(flist, Ez0Spec)
ax1.plot(flist, Ez1Spec)
ax1.legend(['падающий спектр','отраженный спектр'],loc='upper right')
ax1.minorticks_on()
ax1.grid()
ax2.set_xlim(Fmin, Fmax)
ax2.set_ylim(0, 1.0)
ax2.set_xlabel('f, Гц')
ax2.set_ylabel('|Г|, б/р')
ax2.plot(flist, Gama)
ax2.minorticks_on()
ax2.grid()
plt.subplots_adjust(hspace=0.5)
plt.show()
