import os
import sys
from ctypes import *
import soundfile as sf

def first_step(m):
	a = 1.1
	data, fd = sf.read('90.wav')
	C = data
	rowsC = len(data)
	Nm = len(m)
	Lm = 8 * Nm
	d0 = 20
	d1 = 30
	C0 = [0 for x in range(d0)]
	C0 = C0 + C
	C1 = [0 for x in range(d1)]


def stack(A, B):
	return A.extend(B)



filename = '90.wav'
data, fd = sf.read('90.wav')
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
first_step("Опасность")



	