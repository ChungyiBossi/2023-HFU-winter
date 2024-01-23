from pydub import AudioSegment


if __name__ == '__main__':
    audio_path = './maplestory.mp4'
    song = AudioSegment.from_file(audio_path)    # 讀取 audio 檔案
    song.export(audio_path.replace('.mp4', '.wav'), format='wav')
