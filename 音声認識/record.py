# -*- coding: utf-8 -*-
# 

# [setup] 

#   pip install pyaudio 

# 

import sys 

import pyaudio 

import wave 

  

# 

# 録音に必要なパラメータ設定 

# 

record_time = 3           # 録音時間 

outFile = "result.wav"    # 結果ファイル名 

 

samp_freq = 44100         # サンプリング周波数 

bit = pyaudio.paInt16     # 量子化ビット 

channel_num = 1           # チャンネル数 

buffer_size = 2**10       # 録音バッファサイズ 

  

# 

# コマンドライン引数のチェック 

# 

args = sys.argv 

if (len(args) > 1): 

    if (len(args) > 3 or args[1] == "-h"): 

        print('Usage: ', args[0], ' [out_file] [record_time(sec)]') 

        sys.exit() 

    if (len(args) >= 2): 

        outFile = args[1] 

    if (len(args) >= 3): 

        record_time = int(args[2]) 

 

# 

# 録音開始 

# 

pa = pyaudio.PyAudio() 

stream = pa.open( 

    rate=samp_freq, 

    format=bit, 

    channels=channel_num, 

    frames_per_buffer=buffer_size, 

    input=True, 

    output=False, 

    ) 

  

# 

# 必要な時間だけ波形を記録する 

# 

x = [] 

for i in range(0, int(record_time * samp_freq / buffer_size)): 

    data = stream.read(buffer_size) 

    x.append(data) 

  

# 

# 録音終了 

# 

stream.stop_stream() 

stream.close() 

pa.terminate() 

  

# 

# 録音内容をwavファイルに保存 

# 

with wave.open(outFile, "wb") as wo: 

    wo.setnchannels(channel_num) 

    wo.setsampwidth(pa.get_sample_size(bit)) 

    wo.setframerate(samp_freq) 

    wo.writeframes(b''.join(x)) 

    wo.close() 