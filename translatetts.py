import sys

import googletrans
import pyttsx3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QPlainTextEdit, QPushButton, QComboBox,
                             QCheckBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translate and Speak")
        self.setGeometry(500, 100, 900, 400)

        self.srcText = QPlainTextEdit()
        self.srcText.setPlainText("My name is Translator.")
        self.srcSpeak = QPushButton("Speak")
        self.srcLanguages = QComboBox()

        self.translate = QPushButton("Translate")
        self.speakAfterTranslate = QCheckBox("Speak After Translate")
        self.speakAfterTranslate.setChecked(True)
        self.swap = QPushButton("Swap")

        self.destText = QPlainTextEdit("")
        self.destSpeak = QPushButton("Speak")
        self.destLanguages = QComboBox()

        self.translator = googletrans.Translator()

        self.initUI()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        centralWidgetGridLayout = QGridLayout()

        centralWidgetGridLayout.addWidget(self.srcText, 0, 0)
        centralWidgetGridLayout.addWidget(self.srcSpeak, 1, 0)
        centralWidgetGridLayout.addWidget(self.srcLanguages, 2, 0)

        centralWidgetGridLayout.addWidget(self.translate, 0, 1)

        centralWidgetGridLayout.addWidget(self.destText, 0, 2)
        centralWidgetGridLayout.addWidget(self.destSpeak, 1, 2)
        centralWidgetGridLayout.addWidget(self.destLanguages, 2, 2)

        centralWidgetGridLayout.addWidget(self.speakAfterTranslate, 1, 1)
        centralWidgetGridLayout.addWidget(self.swap, 2, 1)

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
        self.translate.clicked.connect(self.translateNow)

        # noinspection PyUnresolvedReferences
        self.srcSpeak.clicked.connect(lambda: self.speak(self.srcText.toPlainText(),
                                                         self.srcLanguages.itemData(self.srcLanguages.currentIndex())))
        # noinspection PyUnresolvedReferences
        self.destSpeak.clicked.connect(lambda: self.speak(self.destText.toPlainText(), self.destLanguages.itemData(
            self.destLanguages.currentIndex())))

    def speak(self, text: str, lang: str):
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        engine.say(text)
        engine.runAndWait()

    def swapSrcDest(self):
        srcPlainText = self.srcText.toPlainText()
        self.srcText.setPlainText(self.destText.toPlainText())
        self.destText.setPlainText(srcPlainText)

        srcCurrentText = self.srcLanguages.currentText()
        self.srcLanguages.setCurrentText(self.destLanguages.currentText())
        self.destLanguages.setCurrentText(srcCurrentText)

    def translateNow(self):
        srcText = self.srcText.toPlainText()
        destText = self.translator.translate(srcText,
                                             src=self.srcLanguages.itemData(self.srcLanguages.currentIndex()),
                                             dest=self.destLanguages.itemData(self.destLanguages.currentIndex()))
        self.destText.setPlainText(destText.text)
        if self.speakAfterTranslate.isChecked():
            self.speak(self.destText.toPlainText(), self.destLanguages.itemData(self.destLanguages.currentIndex()))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
