####### 语音转文字
import whisper
import threading


class Translator:
    def __init__(self):
        self.model = whisper.load_model("turbo")
    
    def translate(self, audio_path):
        print("translate===")
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio, n_mels=self.model.dims.n_mels).to(self.model.device)

        # detect the spoken language
        _, probs = self.model.detect_language(mel)
        # decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        print("result.text: ", result.text)
        return result.text

    def translate_thread(self, audio_path):
        """在新线程中运行 `translate()`，并返回队列中的结果"""
        t = threading.Thread(target=self.translate, args=(audio_path,), daemon=True)
        t.start()
        return t

# Function to translate audio to text by a given audio path
# # def translate(audio_path):
#     model = whisper.load_model("turbo")
#     # result = model.transcribe("audio.mp3", fp16=False)
#     # print(result["text"])

#     # load audio and pad/trim it to fit 30 seconds
#     audio = whisper.load_audio(audio_path)
#     audio = whisper.pad_or_trim(audio)

#     # make log-Mel spectrogram and move to the same device as the model
#     mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

#     # detect the spoken language
#     _, probs = model.detect_language(mel)
#     # decode the audio
#     options = whisper.DecodingOptions()
#     result = whisper.decode(model, mel, options)

#     # print the recognized text
#     print(result.text)
#     return result.text