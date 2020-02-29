import os
import sys
from ctypes import *
import soundfile as sf
import numpy as np
import math

def first_step(M):
	a = 1.1
	data, fd = sf.read('90.wav')
	C = data
	rowsC = len(data)
	Nm = len(M)
	Lm = 8 * Nm
	d0 = 20
	d1 = 30
	C0 = np.array([0 for x in range(d0)])
	C0 = np.concatenate((C0, C), axis=0) * a
	C1 = np.array([0 for x in range(d1)])
	C1 = np.concatenate((C1, C), axis=0) * a

	SC0 = np.array([0 for x in range(rowsC)])	

	for i in range(rowsC):
		SC0[i] = C[i] + C0[i]

	SC1 = np.array([0 for x in range(rowsC)])	

	for i in range(rowsC):
		SC1[i] = C[i] + C1[i]

	Nb = math.floor(rowsC/Lm)

	U = 1
	tau = 20
	T = Nb - tau
	
	fp, u, fz = module_1(tau, T)
	a = module_2(M, Lm)
	
	

def module_1(tau_c, T_c):
	fp = np.zeros(tau_c)
	for n in range(tau_c):
		if tau_c > 0:
			fp[n] = ((n - tau_c)/tau_c)
		if tau_c == 0:
			fp[0] = 0

	u = np.array(1 for i in range(T_c - tau_c))

	fz = np.zeros(2 * tau_c)
	for n in range(2 * tau_c):
		if tau_c > 0:
			fz[n] = (n - tau_c)/(-tau_c)
		if tau_c == 0:
			fz[0] = 0

	return fp, u, fz

def module_2(msg_c, Lm_c, fp_c, fz_c, tau_c, u_c, C_c):
	a_bytes = bytes(msg_c, "utf-8")
	m_vec = ' 0'.join(format(ord(i), 'b') for i in msg_c)
	m_vec = m_vec.replace(' ', '') 
	m_vec = '0' + m_vec
	print(str(res), Lm_c)
	if m_vec[0] == 0:
		mu1 = np.zeros(tau_c - (round(tau_c / 2) + 1) + len(u_c))
	if m_vec[0] == 1:
		mu1 = np.zeros(tau_c - (round(tau_c / 2) + 1) + len(u_c))
		i = tau_c - (round(tau_c / 2) + 1)
		while i < len(u_c):
			mu1[i] = 1
			i += 1
	

	for m in range(Lm_c):
		if m == 0:
			continue
		if m_vec[m] != m_vec[m - 1] and m_vec[m] == 0 ^ m_vec[m]:
			mu1 = stack(mu1, fz_c, 0 * u_c)
		if m_vec[m] == m_vec[m - 1] and m_vec[m] == 0 ^ m_vec[m]:
			mu1 = stack(mu1, 0 * fz_c, 0 * u_c)
		if m_vec[m] != m_vec[m - 1] and m_vec[m] == 1 ^ m_vec[m]:
			mu1 = stack(mu1, fp_c, u_c)
		if m_vec[m] != m_vec[m - 1] and m_vec[m] == 0 ^ m_vec[m]:
			mu1 = stack(mu1, 0 * fp_c, u_c)
	
	while len(mu1) <= len(C_c):
		if m_vec[Lm_c - 1] == 0:
			mu1 = stack(mu1, 0 * fp_c, 0 * u)
		if m_vec[Lm_c - 1] == 1:
			mu1 = stack(mu1, 0 * fp_c, u)

	return mu1, mu2
		
def stack(c1, c2, c3):
	c2.np.append(c3)
	c1.np.append(c2)
	return c1
	



filename = '90.wav'
#data, fd = sf.read('90.wav')
#sf.write('901.wav', data, fd)
workLib = cdll.LoadLibrary("Steganka.dll")
filename_in = c_char * len(filename)											
filename_c = filename_in()														
filename_c.value = filename.encode('utf-8')										
len_item = c_int(len(filename))		
#filename_p = c_wchar_p(filename)
rc = c_int(-1)
rc_p = pointer(rc)

sample_rate = c_int(-1)
sample_rate_p = pointer(sample_rate)

bits_per_sample = c_int(-1)
bits_per_sample_p = pointer(bits_per_sample) 

#workLib.print()
workLib.get_params(rc_p, filename_c, len_item, sample_rate_p, bits_per_sample_p)

print(rc_p.contents.value)
print(sample_rate_p.contents.value)
print(bits_per_sample_p.contents.value)

Q = bits_per_sample_p.contents.value
fd = sample_rate_p.contents.value
first_step("Name")



	