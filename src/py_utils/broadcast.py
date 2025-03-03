import pyttsx3
import argparse
import sys

def speak(text):
    """使用 `pyttsx3` 朗读文本"""
    engine = pyttsx3.init(driverName="nsss")  # 适用于 macOS
    engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # 释放资源，避免 Python 进程卡住

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文本转语音（TTS）")
    parser.add_argument("text", nargs="?", type=str, help="需要朗读的文本")
    
    args = parser.parse_args()

    if args.text:
        # ✅ 如果提供了文本作为参数，直接朗读
        speak(args.text)
