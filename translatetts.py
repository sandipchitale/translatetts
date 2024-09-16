import sys

import googletrans
import pyttsx3
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QPlainTextEdit, QPushButton, QComboBox,
                             QCheckBox, QVBoxLayout)
from pyttsx3.voice import Voice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)

        self.setWindowTitle("Translate and Speak")
        self.setGeometry(500, 100, 900, 400)

        self.srcText = QPlainTextEdit()
        self.srcText.setPlainText("Let us translate and speak.")
        self.srcSpeak = QPushButton("")
        self.srcSpeak.setIcon(QIcon("icons/speak.png"))
        self.srcSpeak.setToolTip("Speak")
        self.srcLanguages = QComboBox()

        self.translateLR = QPushButton("")
        self.translateLR.setIcon(QIcon("icons/translatelr.png"))
        self.translateLR.setToolTip("Translate (from left to right)")

        self.translateRL = QPushButton("")
        self.translateRL.setIcon(QIcon("icons/translaterl.png"))
        self.translateRL.setToolTip("Translate (from right to left)")

        self.speakAfterTranslate = QCheckBox("Speak After Translate")
        self.speakAfterTranslate.setChecked(False)
        self.swap = QPushButton("")
        self.swap.setIcon(QIcon("icons/swap.png"))
        self.swap.setToolTip("Swap")

        self.destText = QPlainTextEdit("Lassen Sie uns übersetzen und sprechen.")
        self.destSpeak = QPushButton("")
        self.destSpeak.setIcon(QIcon("icons/speak.png"))
        self.destSpeak.setToolTip("Speak")
        self.destLanguages = QComboBox()

        self.srcVoices = QComboBox()
        self.destVoices = QComboBox()

        self.translator = googletrans.Translator()

        self.initUI()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        centralWidgetGridLayout = QGridLayout()

        centralWidgetGridLayout.addWidget(self.srcText, 0, 0)
        centralWidgetGridLayout.addWidget(self.srcSpeak, 1, 0)
        centralWidgetGridLayout.addWidget(self.srcLanguages, 2, 0)

        middle = QWidget()
        middleLayout = QVBoxLayout()
        middle.setLayout(middleLayout)

        middleLayout.addStretch()
        middleLayout.addWidget(self.translateLR)
        middleLayout.addWidget(self.translateRL)
        middleLayout.addStretch()

        centralWidgetGridLayout.addWidget(middle, 0, 1)

        centralWidgetGridLayout.addWidget(self.destText, 0, 2)
        centralWidgetGridLayout.addWidget(self.destSpeak, 1, 2)
        centralWidgetGridLayout.addWidget(self.destLanguages, 2, 2)

        centralWidgetGridLayout.addWidget(self.speakAfterTranslate, 1, 1)
        centralWidgetGridLayout.addWidget(self.swap, 2, 1)

        # noinspection PyTypeChecker
        voices = tuple(self.engine.getProperty('voices'))
        for voice in voices:
            self.srcVoices.addItem(voice.name, voice)
            self.destVoices.addItem(voice.name, voice)
        self.srcVoices.setCurrentText("English (America)")
        self.destVoices.setCurrentText("German")
        centralWidgetGridLayout.addWidget(self.srcVoices, 3, 0)
        centralWidgetGridLayout.addWidget(self.destVoices, 3, 2)

        centralWidget.setLayout(centralWidgetGridLayout)

        languages = googletrans.LANGUAGES

        for language in languages:
            self.srcLanguages.addItem(languages[language], language)
            self.destLanguages.addItem(languages[language], language)

        self.srcLanguages.setCurrentText("english")
        self.destLanguages.setCurrentText("german")

        # noinspection PyUnresolvedReferences
        self.swap.clicked.connect(self.swapSrcDest)
        # noinspection PyUnresolvedReferences
        self.translateLR.clicked.connect(lambda: self.translateNow(self.srcText,
                                                                   self.srcLanguages,
                                                                   self.srcVoices,
                                                                   self.destText,
                                                                   self.destLanguages,
                                                                   self.destVoices))
        # noinspection PyUnresolvedReferences
        self.translateRL.clicked.connect(lambda: self.translateNow(self.destText,
                                                                   self.destLanguages,
                                                                   self.destVoices,
                                                                   self.srcText,
                                                                   self.srcLanguages,
                                                                   self.srcVoices))

        # noinspection PyUnresolvedReferences
        self.srcSpeak.clicked.connect(lambda: self.speak(self.srcText.toPlainText(),
                                                         self.srcLanguages.itemData(
                                                             self.srcLanguages.currentIndex()),
                                                         self.srcVoices.itemData(self.srcVoices.currentIndex())))
        # noinspection PyUnresolvedReferences
        self.destSpeak.clicked.connect(lambda: self.speak(self.destText.toPlainText(),
                                                          self.destLanguages.itemData(
                                                              self.destLanguages.currentIndex()),
                                                          self.destVoices.itemData(self.destVoices.currentIndex())))

    def speak(self, text: str, lang: str, voice: Voice, afterTranslate = False):
        self.engine.setProperty("voice", voice.id)
        self.engine.say(text)
        self.engine.runAndWait()

    def swapSrcDest(self):
        srcPlainText = self.srcText.toPlainText()
        self.srcText.setPlainText(self.destText.toPlainText())
        self.destText.setPlainText(srcPlainText)

        srcCurrentText = self.srcLanguages.currentText()
        self.srcLanguages.setCurrentText(self.destLanguages.currentText())
        self.destLanguages.setCurrentText(srcCurrentText)

        srcCurrentVoice = self.srcVoices.currentText()
        self.srcVoices.setCurrentText(self.destVoices.currentText())
        self.destVoices.setCurrentText(srcCurrentVoice)

    def translateNow(self, srcText, srcLanguages, srcVoices, destText, destLanguages, destVoices):
        textToTranslate = srcText.toPlainText()
        translatedText = self.translator.translate(textToTranslate,
                                                   src=srcLanguages.itemData(srcLanguages.currentIndex()),
                                                   dest=destLanguages.itemData(destLanguages.currentIndex()))
        destText.setPlainText(translatedText.text)
        if self.speakAfterTranslate.isChecked():
            self.speak(destText.toPlainText(),
                       destLanguages.itemData(destLanguages.currentIndex()),
                       destVoices.itemData(destVoices.currentIndex()))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
