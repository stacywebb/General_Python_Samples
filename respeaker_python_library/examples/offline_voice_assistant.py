# Offline Voice Assistant
# offline_voice_assistant.py

import time
from threading import Thread, Event

import pyaudio

try:
    from respeaker import *
except ImportError:
    import fix_import
    from respeaker import *


mic = None


def task(quit_event):
    global mic

    pixels = PixelRing()
    pixels.set_color(rgb=0x400000)

    pa = pyaudio.PyAudio()
    mic = Microphone(pa)

    pixels.set_color(rgb=0x004000)
    time.sleep(2)
    pixels.off()

    while not quit_event.is_set():
        if mic.wakeup(keyword='alexa'):
            print('Wake up')
            pixels.listen()

            data = mic.listen()
            text = mic.recognize(data)

            pixels.wait()
            if text.find('play music') >= 0:
                print('Play music')

        pixels.off()

    pixels.off()
    mic.close()


def main():
    quit_event = Event()
    thread = Thread(target=task, args=(quit_event,))
    thread.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nquit')
            quit_event.set()
            mic.quit()
            break

    thread.join()


if __name__ == '__main__':
    main()
