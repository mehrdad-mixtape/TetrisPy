import sys, os
try:
    from pyaudio import PyAudio
    import wave
except ImportError:
    sys.exit()

musics = {
        '1': './audios/Opening1.wav',
        '2': './audios/Opening2.wav',
        '3': './audios/Row-Clear1.wav',
        '4': './audios/Row-Clear2.wav',
        '5': './audios/Row-Clear3.wav',
        '6': './audios/Tetris-Clear.wav',
        '7': './audios/Ending.wav',
        '8': './audios/Game-Over.wav',
        '9': './audios/Mapping.wav',
        '10': './audios/Move-Down.wav',
        '11': './audios/Move-RL.wav',
        '12': './audios/Rotate-Shape.wav',
        '13': './audios/Pause.wav',
        '14': './audios/Stage-Clear1.wav',
        '15': './audios/Stage-Clear2.wav',
        '15': './audios/TypeA.wav',
        '16': './audios/TypeB.wav',
        '17': './audios/TypeC.wav',
        '18': './audios/TypeD.wav',
        '19': './audios/TypeE.wav',
        '20': './audios/TypeF.wav',
}

def find_audios(path: str='./') -> bool:
    files = os.listdir(path)
    if 'audios' in files:
        wav_files = os.listdir(path + 'audios/')
        for key in musics:
            if musics[key].split('/')[2] not in wav_files:
                break
        else:
            return True
    else:
        return False

class Music:
    def __init__(self):
        self.__chunk = 1024 # length of data to read.
        self.__audio = PyAudio() # create audio object.

    def play(self, music_path: str) -> None:
        with wave.open(music_path, mode='rb') as wf:
            # open stream based on the wave object which has been input.
            stream = self.__audio.open(
                format=self.__audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output = True
            )

            # read data (based on the chunk size)
            data = wf.readframes(self.__chunk)

            # play stream (looping from beginning of file to the end)
            while data != b'':
                # writing to the stream is what *actually* plays the sound.
                stream.write(data)
                data = wf.readframes(self.__chunk)

            # cleanup stuff.
            stream.close()
    
def duration_music(music_number: int) -> int:
    if find_audios():
        with wave.open(musics.get(f"{music_number}", '1')) as wf:
            return int(wf.getnframes() // float(wf.getframerate()))

def main(argv: str):
    music = Music()
    music.play(musics.get(argv, '1'))

if __name__ == '__main__':
    main(sys.argv[1])