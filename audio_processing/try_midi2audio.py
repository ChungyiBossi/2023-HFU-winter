from midi2audio import FluidSynth
from pydub import AudioSegment


if __name__ == '__main__':

    sound_font_path = './sound_font/MuseScore_General_Full.sf2'
    # midi_file_path = './maplestory.mid'
    # midi_file_path = './maplestory_sound2midi.mid'
    midi_file_path = '/Users/chungilin/2023_hfu_winter/audio-to-midi/maplestory.wav.mid'

    # 使用FluidSynth将MIDI文件转换为WAV格式
    fs = FluidSynth(sound_font=sound_font_path)
    fs.midi_to_audio(midi_file_path, midi_file_path.replace('.mid', '.wav'))

    # # 加载并播放WAV文件
    # audio = AudioSegment.from_wav('output.wav')
