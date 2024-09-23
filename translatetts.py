import sys

import googletrans
import pyttsx3
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QPlainTextEdit, QPushButton, QComboBox,
                             QErrorMessage, QSizePolicy, QLabel)
from httpcore import ConnectError
from pyttsx3.voice import Voice


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)

        self.setWindowTitle("Translate and Speak")
        self.setGeometry(500, 100, 900, 400)

        self.translateLR = QPushButton("")
        self.translateLR.setIcon(QIcon("icons/translatelr.png"))
        self.translateLR.setToolTip("Translate (from left to right)")
        self.translateLR.setIconSize(QSize(32, 32))

        # self.swap = QPushButton("")
        # self.swap.setIcon(QIcon("icons/swap.png"))
        # self.swap.setToolTip("Swap")
        # self.swap.setIconSize(QSize(32,32))

        self.translateRL = QPushButton("")
        self.translateRL.setIcon(QIcon("icons/translaterl.png"))
        self.translateRL.setToolTip("Translate (from right to left)")
        self.translateRL.setIconSize(QSize(32, 32))

        self.srcText = QPlainTextEdit("Let us translate and speak.")
        self.destText = QPlainTextEdit("Lassen Sie uns übersetzen und sprechen.")

        self.srcSpeak = QPushButton("")
        self.srcSpeak.setIcon(QIcon("icons/speakl.png"))
        self.srcSpeak.setIconSize(QSize(32, 32))
        self.srcSpeak.setToolTip("Speak")

        # self.speakAfterTranslate = QCheckBox("")
        # self.translateRL.setToolTip("Speak after translation")
        # self.speakAfterTranslate.setChecked(True)
        # self.speakAfterTranslate.setIcon(QIcon("icons/speakaftertranslate.png"))
        # self.speakAfterTranslate.setIconSize(QSize(64, 32))

        self.destSpeak = QPushButton("")
        self.destSpeak.setIcon(QIcon("icons/speakr.png"))
        self.destSpeak.setToolTip("Speak")
        self.destSpeak.setIconSize(QSize(32, 32))

        self.srcLanguages = QComboBox()
        self.destLanguages = QComboBox()

        self.srcVoices = QComboBox()
        self.destVoices = QComboBox()

        self.translator = googletrans.Translator()

        self.initUI()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        centralWidgetGridLayout = QGridLayout()

        srcLanguageLabel = QLabel("From:")
        srcLanguageLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(srcLanguageLabel, 0, 0)
        self.srcLanguages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.srcLanguages, 0, 1, 1, 3)

        destLanguagesLabel = QLabel("To:")
        destLanguagesLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(destLanguagesLabel, 0, 4)
        self.destLanguages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.destLanguages, 0, 5, 1, 3)

        centralWidgetGridLayout.addWidget(self.srcText, 1, 0, 1, 4)
        centralWidgetGridLayout.addWidget(self.destText, 1, 4, 1, 4)

        # self.translateLR.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.translateLR, 2, 0, 1, 4)

        # self.translateRL.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.translateRL, 2, 4, 1, 4)

        # noinspection PyTypeChecker
        voices = tuple(self.engine.getProperty('voices'))
        for voice in voices:
            self.srcVoices.addItem(voice.name, voice)
            self.destVoices.addItem(voice.name, voice)
        self.srcVoices.setCurrentText("English (America)")
        self.destVoices.setCurrentText("German")

        self.srcSpeak.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.srcSpeak, 3, 0)
        srcInLabel = QLabel("in")
        srcInLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(srcInLabel, 3, 1)
        self.srcVoices.setStyleSheet("height: 32px;")
        self.srcVoices.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.srcVoices, 3, 2)
        srcVoiceLabel = QLabel("voice.")
        srcVoiceLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(srcVoiceLabel, 3, 3)

        self.destSpeak.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.destSpeak, 3, 4)
        destInLabel = QLabel("in")
        destInLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(destInLabel, 3, 5)
        self.destVoices.setStyleSheet("height: 32px;")
        self.destVoices.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(self.destVoices, 3, 6)
        destVoiceLabel = QLabel("voice.")
        destVoiceLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        centralWidgetGridLayout.addWidget(destVoiceLabel, 3, 7)

        centralWidget.setLayout(centralWidgetGridLayout)

        languages = googletrans.LANGUAGES

        for language in languages:
            self.srcLanguages.addItem(languages[language].capitalize(), language)
            self.destLanguages.addItem(languages[language].capitalize(), language)

        self.srcLanguages.setCurrentText("English")
        self.destLanguages.setCurrentText("German")

        # noinspection PyUnresolvedReferences
        # self.swap.clicked.connect(self.swapSrcDest

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

    def speak(self, text: str, lang: str, voice: Voice, afterTranslate=False):
        self.engine.setProperty("voice", voice.id)
        self.engine.say(text)
        self.engine.runAndWait()

    # def swapSrcDest(self):
    #     srcPlainText = self.srcText.toPlainText()
    #     self.srcText.setPlainText(self.destText.toPlainText())
    #     self.destText.setPlainText(srcPlainText)
    #
    #     srcCurrentText = self.srcLanguages.currentText()
    #     self.srcLanguages.setCurrentText(self.destLanguages.currentText())
    #     self.destLanguages.setCurrentText(srcCurrentText)
    #
    #     srcCurrentVoice = self.srcVoices.currentText()
    #     self.srcVoices.setCurrentText(self.destVoices.currentText())
    #     self.destVoices.setCurrentText(srcCurrentVoice)

    def translateNow(self, srcText, srcLanguages, srcVoices, destText, destLanguages, destVoices):
        try:
            textToTranslate = srcText.toPlainText()
            translatedText = self.translator.translate(textToTranslate,
                                                       src=srcLanguages.itemData(srcLanguages.currentIndex()),
                                                       dest=destLanguages.itemData(destLanguages.currentIndex()))
            destText.setPlainText(translatedText.text)
            # if self.speakAfterTranslate.isChecked():
            self.speak(destText.toPlainText(),
                       destLanguages.itemData(destLanguages.currentIndex()),
                       destVoices.itemData(destVoices.currentIndex()))
        except ConnectError as ce:
            errorMessage = QErrorMessage()
            errorMessage.showMessage(
                "No internet connection! Internet connection is needed for translation.<br/><br/>Try again later once you are online.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
