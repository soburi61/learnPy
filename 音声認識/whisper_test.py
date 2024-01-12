# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 11:21:00 2024

"""

# 

# [source] 

# https://github.com/openai/whisper 

# 

# [setup] 

#    pip install git+https://github.com/openai/whisper.git  

#  

#   ffmpegのインストール： 

#    次のサイトからWindows用のffmpegをダウンロードし、 

#    展開する（今回はffmpeg-master-latest-win64-gpl.zipをダウンロード） 

#    https://github.com/BtbN/FFmpeg-Builds/releases 

#    上記zipファイルを展開した場所を仮に「c:\foo\ffmpeg」とすると、 

#     anacondaのpowershellで次のコマンドを実行してPATHを通す。 

#         $ENV:Path="c:\foo\ffmpeg\bin;"+$ENV:Path 

#        この作業はpowershellを起動する度に実行し直す必要がある。 

# 

 

import whisper 

 

model = whisper.load_model("base") 

result = model.transcribe("test.wav", language="ja") 

 

print(result["text"]) 

 

 