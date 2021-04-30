# audio_visualizer

A Python script to read computer audio and perform a FFT on data. Then frequency values are parsed and
add to their respective bins to create audio bands. The script then connects to an Arduino via a
Serial port and light up led strips according to audio bands. 
