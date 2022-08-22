from pyaudio import PyAudio
import wave, sys

class Music:
    musics = {
        '1': './audios/clear.wav',
        '2': './audios/start.wav',
        '3': './audios/tetris-clear.wav',
        '4': './audios/1.wav',
        '5': './audios/2.wav',
        '6': './audios/3.wav',
        '7': './audios/4.wav',
        '8': './audios/5.wav',
        '9': './audios/6.wav',
        '10': './audios/7.wav',
        '11': './audios/8.wav',
        '12': './audios/9.wav',
        '13': './audios/10.wav',
        '14': './audios/11.wav',
        '15': './audios/12.wav',
        '16': './audios/13.wav',
    }

    def __init__(self):
        self.__chunk = 1024 # length of data to read.
        self.__audio = PyAudio() # create audio object.

    def play(self, music_path: str):
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

def main(argv: str):
    music = Music()
    music.play(Music.musics.get(argv, '1'))

if __name__ == '__main__':
    main(sys.argv[1])