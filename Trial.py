import pyaudio
import wave
import time
import sys
import opuslib
import struct

filename = 'audio.wav'
filename_coded = 'audio_encoded.wav'
filename_opus_coded = 'audio_encoded_opus.bin'
# Open the sound file 
wf = wave.open(filename, 'rb')
wf_coded = wave.open(filename_coded, 'wb')
wf_opus_coded = open(filename_opus_coded, 'wb')

sample_width = wf.getsampwidth()
num_of_channels = wf.getnchannels()
sample_rate = wf.getframerate()

SAMPLE_FREQUENCY = sample_rate
NUM_OF_CHANNEL = num_of_channels
NUM_OF_FRAMES = 480
BITRATE = 256000
#print "Audio configuration : "+str(sample_width)+" "+str(sample_rate)+" "+str(num_of_channels)
print("BITRATE:"+str(BITRATE))
print("sample_width:"+str(sample_width))
# Create an interface to PortAudio
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    pcm_data = wf.readframes(frame_count)
    return (pcm_data, pyaudio.paContinue)

# Encode and Decode PCM Audio by Opus
wf_coded.setnchannels(NUM_OF_CHANNEL)
wf_coded.setsampwidth(sample_width)
wf_coded.setframerate(SAMPLE_FREQUENCY)

print("Sample Frquency:"+str(SAMPLE_FREQUENCY))
print("Number of channel:"+str(NUM_OF_CHANNEL))

enc = opuslib.api.encoder.create(SAMPLE_FREQUENCY, NUM_OF_CHANNEL, 2049)
opuslib.api.encoder.ctl(enc, opuslib.api.ctl.set_bitrate, BITRATE)
opuslib.api.encoder.ctl(enc, opuslib.api.ctl.set_vbr, 0)
bitrate = opuslib.api.encoder.ctl(enc, opuslib.api.ctl.get_bitrate)
vbr = opuslib.api.encoder.ctl(enc, opuslib.api.ctl.get_vbr)
print("Bitrate = " + str(bitrate) + ", vbr = " + str(vbr))
dec = opuslib.api.decoder.create(SAMPLE_FREQUENCY, NUM_OF_CHANNEL)
data = wf.readframes(NUM_OF_FRAMES)
count = 0
while data and len(data) == NUM_OF_FRAMES*sample_width*NUM_OF_CHANNEL:
    # Opus Encoding
    encoded_data = opuslib.api.encoder.encode(enc, data, NUM_OF_FRAMES, len(data))
    seq_num = struct.pack("B", count % 256)
    encoded_data_with_seq = seq_num + encoded_data
    wf_opus_coded.write(encoded_data_with_seq) 
    # print(encoded_data)
    # Opus Decoding
    decoded_data = opuslib.api.decoder.decode(dec, encoded_data, len(encoded_data), NUM_OF_FRAMES, 0, 1)

	# Write Encoded/Decoded Audio Frames into File
    wf_coded.writeframesraw(decoded_data)
    #print encoded_data.encode('hex_codec')

	# Read Next Chunk of Audio Frames
    data = wf.readframes(NUM_OF_FRAMES)

    
    #if count == 99:
    #    break
    count += 1


print("Count:"+str(count))
print("Num_of_frames = " + str(count))
opuslib.api.encoder.destroy(enc)
opuslib.api.decoder.destroy(dec)

wf.close()
wf_coded.close()
wf_opus_coded.close()

wf = wave.open(filename_coded, 'rb')

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(sample_width),
                channels = num_of_channels,
                rate = sample_rate,
                output = True,
                frames_per_buffer = NUM_OF_FRAMES,
                stream_callback = callback)
# start the stream
stream.start_stream()

# wait for stream to finish
while stream.is_active():
    time.sleep(0.1)

# Close and terminate the stream
stream.stop_stream()
stream.close()

p.terminate()
