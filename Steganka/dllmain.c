// dllmain.cpp : Определяет точку входа для приложения DLL.
#include "unistd.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "wave.h"
//#include <dir.h>
#define TRUE 1 
#define FALSE 0
#define _CRTDBG_MAP_ALLOC
 // WAVE header structure

unsigned char buffer4[4];
unsigned char buffer2[2];

char* seconds_to_time(float seconds);


BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

__declspec(dllexport) void print()
{
	printf("NO");
}


// добавить параметры и rc
__declspec(dllexport) void get_params(int *rc, unsigned char *path, int len_path, 
									  int *sample_rate, int *bits_per_sample)
{
	FILE *ptr;
	char *filename;
	struct HEADER header;

	filename = (char*)malloc(len_path + 1 * sizeof(char));
	/*filename = (char*)malloc(sizeof(char) * 1024);*/
	if (filename == NULL) {
		printf("Error in malloc\n");
		exit(1);
	}

	 //get file path
	//char cwd[1024];
	//if (_getcwd(cwd, sizeof(cwd)) != NULL) {

	//	strcpy(filename, cwd);

	//	// get filename from command line
	//	//if (argc < 2) {
	//	//	printf("No wave file specified\n");
	//	//	return;
	//	//}

	//	strcat(filename, "/");
	//	memcpy(filename, path, len_path);
	//	//strcat(filename, "90.wav");
	//	printf("%s\n", filename);
	//}

	// open file
	
	memcpy(filename, path, len_path);
	filename[len_path] = '\0';

	//printf("Opening  file..\n");
	ptr = fopen(filename, "rb");
	if (ptr == NULL) {
		printf("Error opening file\n");
		exit(1);
	}

	int read = 0;

	// read header parts

	read = fread(header.riff, sizeof(header.riff), 1, ptr);
	//printf("(1-4): %s \n", header.riff);

	read = fread(buffer4, sizeof(buffer4), 1, ptr);
	//printf("%u %u %u %u\n", buffer4[0], buffer4[1], buffer4[2], buffer4[3]);

	// convert little endian to big endian 4 byte int
	header.overall_size = buffer4[0] |
		(buffer4[1] << 8) |
		(buffer4[2] << 16) |
		(buffer4[3] << 24);

	//printf("(5-8) Overall size: bytes:%u, Kb:%u \n", header.overall_size, header.overall_size / 1024);

	read = fread(header.wave, sizeof(header.wave), 1, ptr);
	//printf("(9-12) Wave marker: %s\n", header.wave);

	read = fread(header.fmt_chunk_marker, sizeof(header.fmt_chunk_marker), 1, ptr);
	//printf("(13-16) Fmt marker: %s\n", header.fmt_chunk_marker);

	read = fread(buffer4, sizeof(buffer4), 1, ptr);
	//printf("%u %u %u %u\n", buffer4[0], buffer4[1], buffer4[2], buffer4[3]);

	// convert little endian to big endian 4 byte integer
	header.length_of_fmt = buffer4[0] |
		(buffer4[1] << 8) |
		(buffer4[2] << 16) |
		(buffer4[3] << 24);
	//printf("(17-20) Length of Fmt header: %u \n", header.length_of_fmt);

	read = fread(buffer2, sizeof(buffer2), 1, ptr); 
	//printf("%u %u \n", buffer2[0], buffer2[1]);

	header.format_type = buffer2[0] | (buffer2[1] << 8);
	char format_name[10] = "";
	if (header.format_type == 1)
		strcpy(format_name, "PCM");
	else if (header.format_type == 6)
		strcpy(format_name, "A-law");
	else if (header.format_type == 7)
		strcpy(format_name, "Mu-law");

	//printf("(21-22) Format type: %u %s \n", header.format_type, format_name);

	read = fread(buffer2, sizeof(buffer2), 1, ptr);
	//printf("%u %u \n", buffer2[0], buffer2[1]);

	header.channels = buffer2[0] | (buffer2[1] << 8);
	//printf("(23-24) Channels: %u \n", header.channels);

	read = fread(buffer4, sizeof(buffer4), 1, ptr);
	//printf("%u %u %u %u\n", buffer4[0], buffer4[1], buffer4[2], buffer4[3]);

	header.sample_rate = buffer4[0] |
		(buffer4[1] << 8) |
		(buffer4[2] << 16) |
		(buffer4[3] << 24);

	//printf("(25-28) Sample rate: %u\n", header.sample_rate);		//here

	read = fread(buffer4, sizeof(buffer4), 1, ptr);
	//printf("%u %u %u %u\n", buffer4[0], buffer4[1], buffer4[2], buffer4[3]);

	header.byterate = buffer4[0] |
		(buffer4[1] << 8) |
		(buffer4[2] << 16) |
		(buffer4[3] << 24);
	//printf("(29-32) Byte Rate: %u , Bit Rate:%u\n", header.byterate, header.byterate * 8);

	read = fread(buffer2, sizeof(buffer2), 1, ptr);
	//printf("%u %u \n", buffer2[0], buffer2[1]);

	header.block_align = buffer2[0] |
		(buffer2[1] << 8);
	//printf("(33-34) Block Alignment: %u \n", header.block_align);

	read = fread(buffer2, sizeof(buffer2), 1, ptr);
	//printf("%u %u \n", buffer2[0], buffer2[1]);

	header.bits_per_sample = buffer2[0] |
		(buffer2[1] << 8);
	//printf("(35-36) Bits per sample: %u \n", header.bits_per_sample);	// here

	read = fread(header.data_chunk_header, sizeof(header.data_chunk_header), 1, ptr);
	//printf("(37-40) Data Marker: %s \n", header.data_chunk_header);

	read = fread(buffer4, sizeof(buffer4), 1, ptr);
	//printf("%u %u %u %u\n", buffer4[0], buffer4[1], buffer4[2], buffer4[3]);

	header.data_size = buffer4[0] |
		(buffer4[1] << 8) |
		(buffer4[2] << 16) |
		(buffer4[3] << 24);
	//printf("(41-44) Size of data chunk: %u \n", header.data_size);


	// calculate no.of samples
	long num_samples = (8 * header.data_size) / (header.channels * header.bits_per_sample);
	//printf("Number of samples:%lu \n", num_samples);

	long size_of_each_sample = (header.channels * header.bits_per_sample) / 8;
	//printf("Size of each sample:%ld bytes\n", size_of_each_sample);

	// calculate duration of file
	float duration_in_seconds = (float)header.overall_size / header.byterate;
	//printf("Approx.Duration in seconds=%f\n", duration_in_seconds);
	//printf("Approx.Duration in h:m:s=%s\n", seconds_to_time(duration_in_seconds));


	*sample_rate = header.sample_rate;
	*bits_per_sample = header.bits_per_sample;
	*rc = 0;
}

/**
 * Convert seconds into hh:mm:ss format
 * Params:
 *	seconds - seconds value
 * Returns: hms - formatted string
 **/
char* seconds_to_time(float raw_seconds) {
	char *hms;
	int hours, hours_residue, minutes, seconds, milliseconds;
	hms = (char*)malloc(100);

	sprintf(hms, "%f", raw_seconds);

	hours = (int)raw_seconds / 3600;
	hours_residue = (int)raw_seconds % 3600;
	minutes = hours_residue / 60;
	seconds = hours_residue % 60;
	milliseconds = 0;

	// get the decimal part of raw_seconds to get milliseconds
	char *pos;
	pos = strchr(hms, '.');
	int ipos = (int)(pos - hms);
	char decimalpart[15];
	memset(decimalpart, ' ', sizeof(decimalpart));
	strncpy(decimalpart, &hms[ipos + 1], 3);
	milliseconds = atoi(decimalpart);


	sprintf(hms, "%d:%d:%d.%d", hours, minutes, seconds, milliseconds);
	return hms;
}