import os
import threading
import webview

from time import time
import sys
import asyncio

sys.path.append(os.path.join(os.getcwd() + '/src/py_utils/'))

from translator import Translator
import chat
import broadcast

# from record import record_conference_audio
import sounddevice as sd
import soundfile as sf

import time
import signal
from datetime import datetime
import subprocess

translator = Translator()

# 结束录音的事件
stop_recording = threading.Event()

def read_text(text):
    """启动一个新线程朗读文本"""
    subprocess.run(["python", '{first}/src/py_utils/broadcast.py'.format(first=os.getcwd()), text]) 


def process_audio(filename):
    """处理录音：翻译 -> 生成对话 -> 语音播放"""
    try:
        # 翻译文本
        translate_script = translator.translate(filename)
        print(translate_script)

        # # 生成对话文本
        responsed_text = chat.chat(translate_script)
        print("responsed_text: ", responsed_text)

        # 朗读文本
        read_text(responsed_text)

        # 删除录音文件
        os.remove(filename)
        print(f"🗑️ 已删除录音文件: {filename}")

    except Exception as e:
        print(f"❌ 处理音频时发生错误: {e}")

def record_conference_audio():
    """在新线程中运行录音"""
    def recording_thread():
        try:
            sample_rate = 16000  # 16kHz 采样率
            channels = 1         # 单声道
            device = None        # 使用默认输入设备

            # 生成带时间戳的文件名
            filename = datetime.now().strftime("record%Y%m%d_%H%M%S.wav")

            # 打开音频文件
            with sf.SoundFile(filename, mode='x', samplerate=sample_rate, channels=channels) as audio_file:
                
                def callback(indata, frames, time_info, status):
                    """实时音频数据回调函数"""
                    if status:
                        print(status, file=sys.stderr)
                    audio_file.write(indata.copy())

                # 创建输入流
                with sd.InputStream(samplerate=sample_rate, device=device, channels=channels, callback=callback):
                    print(f"🎤 录音中... 文件将保存为：{filename}")
                    while not stop_recording.is_set():
                        time.sleep(1)  # 维持主线程运行
            
            print("\n✅ 录音已停止")
            print(f"💾 文件已保存到：{filename}")

            # 在新线程中处理音频（翻译 -> 生成文本 -> 朗读）
            threading.Thread(target=process_audio, args=(filename,), daemon=True).start()

        except Exception as e:
            print(f"❌ 录音时发生错误: {e}")
    threading.Thread(target=recording_thread, daemon=False).start()




class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()

    def stop_record(self, content):
        """从 GUI 触发停止录音"""
        stop_recording.set()

    def record(self, content):
        """从 GUI 触发录音"""
        stop_recording.clear()
        record_conference_audio()


def get_entrypoint():
    def exists(path):
        return os.path.exists(os.path.join(os.path.dirname(__file__), path))

    if exists('../gui/index.html'): # unfrozen development
        return '../gui/index.html'

    if exists('../Resources/gui/index.html'): # frozen py2app
        return '../Resources/gui/index.html'

    if exists('./gui/index.html'):
        return './gui/index.html'

    raise Exception('No index.html found')


entry = get_entrypoint()

if __name__ == '__main__':
    window = webview.create_window('Knight的私人助理', entry, js_api=Api())
    webview.start()
