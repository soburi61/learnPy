# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 11:20:22 2024

"""

# 

# [setup] 

#   pip install speechrecognition 

# 

# [library source] 

#   https://pypi.org/project/SpeechRecognition/ 

#   https://github.com/Uberi/speech_recognition 

# 

import speech_recognition as sr 

import sys 

 

def main(args): 

    recognizer = sr.Recognizer() 

    with sr.AudioFile(args[1]) as source: 

        wav = recognizer.record(source) 

 

    result = recognizer.recognize_google(wav, language='ja_JP') 

 

    print(result) 

 

if __name__ == '__main__': 

    args = sys.argv 

    if(len(args) != 2): 

        print('Usage',args[0],'wavefile')  

        sys.exit() 

    main(args) 

 