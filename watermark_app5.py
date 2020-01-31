# импортируем модули, необходимые для работы программы
from PyQt5 import QtWidgets, QtCore    # интерфейс
from PyQt5.QtWidgets import QMessageBox

from wm_app_logic import AppLogic
from watermark_gui5 import Ui_MainWindow    # то, что было создано при помощи qt designer
import sys     # работа с командной строкой
import os      # работа с файлами и папками
import threading       # работа с потоками
import subprocess      # запуск сторонних процессов


class _FilterConstructor(QtCore.QObject):      # в данном классе создаём так называемый фильтр событий для menu bar
    def __init__(self, parent):
        super().__init__(parent)

    def eventFilter(self, obj, _event):    # фильтр перехватывает событие StatusTip и не позволяет
        if _event.type() == QtCore.QEvent.StatusTip:       # перезаписывать статус в status bar
            return True
        else:
            return QtCore.QObject.eventFilter(self, obj, _event)


class WatermarkApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()     # инициализируем конструктор родительского класса

        self.setupUi(self)     # вызываем метод настройки интерфейса из файла watermark_gui5.py
        self.connectFramesButtons()

        self.setFixedSize(425, 286)    # устанавливаем фиксированный размер окна приложения
        self.statusBar.showMessage("Ожидание")     # в статус бар отображаем сообщение
        self.progressBar.setValue(0)       # устанавливаем значеие прогресс бара в 0

        self.changeSettings.triggered.connect(self.toggleSettingsFrame)       # связываем пункты меню с нужными методами
        self.about.triggered.connect(self.toggleInfoFrame)
        
        event_filter = _FilterConstructor(self.menuBar)
        self.menuBar.installEventFilter(event_filter)
        
        self.path_to_chosen_folder = ""
        self.watermark_image = ""
        self.output_folder_path = ""
        self.position_index = 0

        self.openOutputFolderButton.setEnabled(False)
        self.MainFrame.raise_()

    # связываем кнопки MainFrame с соответствующим функционалом
    def connectFramesButtons(self):
        self.folderButton.clicked.connect(self.chooseFolder)
        self.watermarkButton.clicked.connect(self.chooseWatermark)
        self.processingButton.clicked.connect(self.updateImages)
        self.openOutputFolderButton.clicked.connect(self.openFolder)
        self.watermarkPosition.currentIndexChanged.connect(self.changeMarkPosition)

        self.settOkButton.clicked.connect(self.toggleMainFrame)

        self.infoBackButton.clicked.connect(self.toggleMainFrame)

    def toggleMainFrame(self):
        self.MainFrame.raise_()

    def toggleSettingsFrame(self):
        self.SettingsFrame.raise_()

    def toggleInfoFrame(self):
        self.InfoFrame.raise_()

    def setToZero(self):       # метод меняет сообщение в статус бар и устанавливает значение прогресс бар в 0
        self.statusBar.showMessage("Ожидание")
        self.progressBar.setValue(0)

    def popUp(self):
        pop_up_message = QMessageBox()
        pop_up_message.setWindowTitle("Предупреждение!")
        pop_up_message.setText("Убедитесь, что все поля заполнены, и выбрана позиция для водяного знака.     ")
        show_pop_up = pop_up_message.exec_()

    def chooseFolder(self):    # метод выбора папки с изображениями
        self.setToZero()
        self.path_to_chosen_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if self.path_to_chosen_folder:
            self.folderPath.setText(self.path_to_chosen_folder)
            images_number = len(os.listdir(self.path_to_chosen_folder))
            self.progressBar.setMaximum(images_number)

    def chooseWatermark(self):     # метод выбора файла с водяным знаком
        self.setToZero()
        self.watermark_image = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл с водяным знаком",
                                                                           "", "Image Files (*bmp *.jpg *.png)")[0]
        self.watermarkPath.setText(self.watermark_image)

    def changeMarkPosition(self):      # записываем в переменную значение индекса combobox
        self.position_index = self.watermarkPosition.currentIndex()

    def updateImages(self):    # вызываем основной метод, обрабатывающий изображения
        if not self.path_to_chosen_folder or not self.watermark_image or self.position_index == 0:
            self.popUp()
            return
        processing_method = AppLogic(self)
        second_thread = threading.Thread(target = processing_method.addWatermark()).start()       # создаём отдельный поток

    def openFolder(self):      # открываем папку с выходными изображениями
        explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        subprocess.run([explorer_path, self.output_folder_path])


def main():
    App = QtWidgets.QApplication(sys.argv)
    MainWindow = WatermarkApp()
    MainWindow.show()
    App.exec_()


if __name__ == '__main__':
    main()