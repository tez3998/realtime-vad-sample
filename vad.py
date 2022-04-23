from typing import List
import soundcard as sc
import numpy as np
import webrtcvad

SAMPLE_RATE: int = 48000
RECORD_SEC: float = 1 / 100
NUM_FRAME: int = int(SAMPLE_RATE * RECORD_SEC)
MAX_SILENCE_DURATION_SEC: float = 0.5

is_speaking: bool = False
silence_duration_sec: float = 0.0
mic_list: List = sc.all_microphones(include_loopback=True)
mic_index: int = 0

print("\nSelect microphone:")
for mi, mic in enumerate(mic_list):
    print("[{}]: {}".format(mi, mic.name))
    
print("\nInput a number")
mic_index = int(input())

try:
    vad: webrtcvad.Vad = webrtcvad.Vad(mode=0)
    print("\nSay something")
    
    with sc.all_microphones(include_loopback=True)[mic_index].recorder(samplerate=SAMPLE_RATE) as mic:
        while(True):
            buf = mic.record(numframes=NUM_FRAME)
            buf = buf[:, 0]
            buf = map(lambda x: (x+1)/2, buf)
            buf = np.fromiter(buf, np.float16)
            buf: bytes = buf.tobytes()
            
            if vad.is_speech(buf=buf, sample_rate=SAMPLE_RATE):
                silence_duration_sec = 0.0
                if is_speaking == False:
                    is_speaking = True
                    print(">>>>")
            else:
                silence_duration_sec += RECORD_SEC
                if (is_speaking == True) and (silence_duration_sec >= MAX_SILENCE_DURATION_SEC):
                    is_speaking = False
                    print("<<<<")
except KeyboardInterrupt:
    print("\nDone")