import os
import sys
from ctypes import *
import soundfile as sf
import numpy as np
import math	
import random

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
	mu1, mu0, m_vec_bin = module_2(M, Lm, fp, fz, tau, u, len(C)) #msg_c, Lm_c, fp_c, fz_c, tau_c, u_c, C_c
	
	S = module_3(m_vec_bin, Lm, Nb, SC1, SC0, mu1, mu0)
	
	ans = stack(S, C, None)
	sf.write('ans.wav', ans, fd)


	data2, fd2 = sf.read('ans.wav')
	module_out(Nb, data2, d1, d0)
	
	
	
	

def module_1(tau_c, T_c):
	fp = np.zeros(tau_c)
	for n in range(tau_c):
		if tau_c > 0:
			fp[n] = ((n - tau_c)/tau_c)
		if tau_c == 0:
			fp[0] = 0

	u = np.array([1 for i in range(T_c - tau_c)])

	fz = np.zeros(tau_c)
	for n in range(tau_c):
		if tau_c > 0:
			fz[n] = (n - tau_c)/(-tau_c)
		if tau_c == 0:
			fz[0] = 0

	return fp, u, fz

def module_2(msg_c, Lm_c, fp_c, fz_c, tau_c, u_c, len_C_c):
	#######
	#str2bin(msg_c)
	m_vec = str2bin(msg_c)
	if m_vec[0] == 0:
		#mu1 = np.zeros(tau_c - (round(tau_c / 2) + 1) + len(u_c))
		mu1 = stack(0 * submatrix(fz_c, round(tau_c / 2) + 1, tau_c, 1, 1), 0 * u_c, None)
		#mu1 = #submatrix(mu1, )
	if m_vec[0] == 1:
		#mu1 = np.zeros(tau_c - (round(tau_c / 2) + 1) + len(u_c))
		mu1 = stack(0 * submatrix(fp_c, round(tau_c / 2) + 1, tau_c, 1, 1) + 1, u_c, None)
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
		if m_vec[m] != m_vec[m - 1] and m_vec[m] == 1 ^ m_vec[m]:
			mu1 = stack(mu1, 0 * fp_c + 1, u_c)
	
	while len(mu1) <= len_C_c:
		if m_vec[Lm_c - 1] == 0:
			mu1 = stack(mu1, 0 * fp_c, 0 * u_c)
		if m_vec[Lm_c - 1] == 1:
			mu1 = stack(mu1, 0 * fp_c + 1, u_c)
	
	mu2 = (-1 * mu1) + 1

	return mu1, mu2, m_vec



def module_3(m_vec_c, Lm_c, Nb_c, SC1_c, SC0_c, mu1_c, mu0_c):
	Sn = np.zeros(Nb_c)
	for m in range(Lm_c):
		if m_vec_c[m] == 0:
			S = submatrix(SC0_c, (Nb_c*(m) + 1), Nb_c * (m + 1), 1, 1)
			mu = submatrix(mu0_c, (Nb_c*(m) + 1), Nb_c * (m + 1), 1, 1)
			for n in range(Nb_c - 1):
				Sn[n] = S[n] * mu[n]
		if m_vec_c[m] == 1:
			S = submatrix(SC1_c, (Nb_c*(m) + 1), Nb_c * (m + 1), 1, 1)
			mu = submatrix(mu1_c, (Nb_c*(m) + 1), Nb_c * (m + 1), 1, 1)
			for n in range(Nb_c - 1):
				Sn[n] = S[n] * mu[n]
		if m == 1:
			S = Sn
		if m > 1:
			S = stack(S, Sn, None)
		
	return S
	
		
def str2bin(text):
	bin_words = [bin(c)[2:].rjust(8, '0') for c in text.encode('cp1251')]
	ans = ' '.join(bin_words)
	answ = []
	for i in range(len(ans)):
		if ans[i] == ' ':
			continue
		answ.append(int(ans[i]))
	return answ
	
def module_out(Nb_c, S_c, d1_c, d0_c):
	m = 1
	B = []
	M_vec = []
	while (Nb_c * m < len(S_c)):
		s = submatrix(S_c, ((Nb_c * (m - 1)) + 1), (Nb_c * (m)), 1, 1)
		F = np.fft.fft(s)
		L = 2 * np.log(F + pow(10, -20))
		AC = np.fft.ifft(L)
		ans0 = sum_S(d0_c, AC)
		ans1 = sum_S(d1_c, AC)
		if ans1 > ans0:
			B.append(1)
		if ans0 > ans1:
			B.append(0)
		if ans0 == ans1:
			B.append(random.random())
		m += 1
		
	j = 1
	while j < (int(len(B) / 8)):
		M_vec.append(submatrix(B, (8 * j - 7), 8 * j, 1, 1))
		j += 1
	
	return False


def sum_S(d_c, AC_c):
	j = d_c - 2
	ans = 0
	while j < d_c + 2:
		ans += abs(AC_c[j])
		j += 1
	return ans
	

def submatrix(array_c, di1, di2, dj1, dj2):
	di1 -= 1
	di2 -= 1
	dj1 -= 1
	dj2 -= 1
	out = np.empty(di2 - di1 + 1)
	ixgrid = np.ix_([di1, di2])#, [dj1, dj2])
	i = 0
	while(di1 <= di2):
		out[i] = array_c[di1]
		di1 += 1
		i += 1
	#out = array_c[ixgrid]
	return out
	

def stack(c1, c2, c3):
	if c3 is None:
		c1 = np.append(c1, c2)
		return c1
	c2 = np.append(c2, c3)
	c1 = np.append(c1, c2)
	return c1

#print(str2bin("Опасность"))
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
first_step("HELL")



	