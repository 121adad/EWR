import tkinter as tk
from threading import Thread, Event
from pygame import mixer
from requests import get
from os import walk
from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import sleep


class Settings:
    waitingTime = 10
    time_to_start = [20, 28]
    download_link = 'https://ssl.gstatic.com/dictionary/static/sounds/oxford/'


class Listener:
    def __init__(self):
        self.observers = []

    def update(self):
        while True:
            if datetime.now().minute == settings.time_to_start[1]:
                self.alert()
                break
            sleep(1)
            print(f'{settings.time_to_start[1] - datetime.now().minute}分钟后开始听写')

    def alert(self):
        for observer in self.observers:
            observer.update()

    def append(self, observers):
        self.observers.append(observers)


class Observer(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Observer1(Observer):
    def __init__(self):
        super().__init__()

    def update(self):
        app = App()


class App_Frame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.font = ('华文行楷', 20)


class PromptAudios:
    mixer.init()
    prompt_one_minute_audio = mixer.Sound("./audios/prompt_one_minute.mp3")
    prompt_interval_audio = mixer.Sound("./audios/interval.mp3")
    prompt_ready_to_3500_audio = mixer.Sound("./audios/ready_to_3500.mp3")
    prompt_ready_to_xk_audio = mixer.Sound("./audios/ready_to_xk.mp3")
    prompt_end_audio = mixer.Sound("./audios/end_audio.mp3")

    mixer.music.load("audios/background.mp3")

    mixer.music.set_volume(0)

    mixer.music.play()


class Frame_EL(App_Frame):
    class _Word:
        def __init__(self, name, path, sound):
            self.name = name
            self.path = path
            self.sound = sound

    def __init__(self):
        super().__init__()
        self.prompt_audios = PromptAudios()
        self.node_3500, self.node_xk = self.nodes()
        self.nodes = self.node_3500 + self.node_xk

        self.label_position_text = tk.StringVar()
        self.label_position_text.set("第 1 个")
        self.position = 1
        self.position_max = len(self.nodes)

        self.label_position = tk.Label(self, font=self.font, textvariable=self.label_position_text)
        self.label_position.pack()
        tk.Button(self, font=self.font, text='下一个', command=self.next_word).pack()
        tk.Button(self, font=self.font, text='上一个', command=self.last_word).pack()
        tk.Button(self, font=self.font, text='播放', command=self.read_word).pack()
        tk.Button(self, font=self.font, text='开始听力', command=self.automatic).pack()

    # 优化结构
    def nodes(self):
        word_3500 = []
        word_xk = []
        for root, dirs, files in walk(r"audios"):
            if root[-1] == "0":
                for word in files:
                    path = root + '\\' + word
                    sound = mixer.Sound(path)
                    word_3500.append(self._Word(word, path, sound))
            elif root[-1] == 'k':
                for word in files:
                    path = root + '\\' + word
                    sound = mixer.Sound(path)
                    word_xk.append(self._Word(word, path, sound))
        return word_3500, word_xk

    def update_position(self):
        self.label_position_text.set(f"第 {self.position} 个")

    def set_position(self, value):
        self.position = value
        self.update_position()

    def read_word(self):
        self.nodes[self.position - 1].sound.play()

    def next_word(self):
        if self.position < self.position_max:
            self.set_position(self.position + 1)

    def last_word(self):
        if 1 < self.position:
            self.set_position(self.position - 1)

    def automatic(self):
        def _round():
            self.prompt_audios.prompt_one_minute_audio.play()
            sleep(60)  # 60s waiting
            self.prompt_audios.prompt_ready_to_3500_audio.play()
            sleep(5)  # 5s waiting
            for word in self.node_3500:
                word.sound.play()
                sleep(settings.waitingTime // 2)
                word.sound.play()
                sleep(settings.waitingTime // 2)
                self.prompt_audios.prompt_interval_audio.play()
                sleep(1.5)

            self.prompt_audios.prompt_ready_to_xk_audio.play()
            sleep(10)
            for word in self.node_xk:
                word.sound.play()
                sleep(settings.waitingTime // 2)
                word.sound.play()
                sleep(settings.waitingTime // 2)
                self.prompt_audios.prompt_interval_audio.play()
                sleep(1.5)
            self.prompt_audios.prompt_end_audio.play()
            sleep(5)

        t = Thread(target=_round)
        t.start()


class Frame_DL(App_Frame):
    def __init__(self):
        super().__init__()
        self.downed_word_path = 'audios'
        self.British_accent = '--_gb_1.mp3'
        self.American_accent = '--_us_1.mp3'
        self.input_box = tk.Text(self, font=self.font, height=15, width=40)
        self.input_box.pack()
        self.btn_download = tk.Button(self, text='download', font=self.font, command=self.download)
        self.btn_download.pack()

    def download(self):
        def _filter(text: str):
            text = text[:-1]
            return text.split(',')

        def _request(word: str):
            response = get(settings.download_link + word + self.American_accent)
            return response

        words = _filter(self.input_box.get('1.0', 'end'))
        for word in words:
            with open(f"audios/{word}.mp3", 'wb') as f:
                resp = _request(word)
                f.write(resp.content)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('听写管理')
        self.geometry("800x600")
        self.font = ('华文行楷', 20)
        tk.Button(self, text='听写', command=self.show_page1, font=self.font).pack()
        tk.Button(self, text='单词音频下载', command=self.show_page2, font=self.font).pack()

        self.page1 = Frame_EL()
        self.page2 = Frame_DL()

        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.mainloop()

    def close_window(self):
        print('window is closed')
        self.destroy()

    def show_page1(self):
        self.page2.pack_forget()
        self.page1.pack()

    def show_page2(self):
        self.page1.pack_forget()
        self.page2.pack()


if __name__ == '__main__':
    settings = Settings()

    listener = Listener()
    listener.append(Observer1())
    # listener.update()
    App()
