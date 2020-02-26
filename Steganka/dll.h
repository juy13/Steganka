#pragma once
__declspec(dllexport) void print();
__declspec(dllexport) void get_params(int *rc, unsigned char *path, int len_path,
	int *sample_rate, int *bits_per_sample);