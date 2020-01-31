from PIL import Image      # обработка изображений
import os      # работа с файлами и папками
import shutil      # удаление папок, в которых содержатся файлы

class AppLogic():
    def __init__(self, GUI):
        self.GUI = GUI

    def addWatermark(self):  # метод, в котором добавляются водяные знаки
        input_image_path = self.GUI.path_to_chosen_folder
        watermark_image_path = self.GUI.watermark_image

        new_folder_name = input_image_path + "_watermarked"
        self.GUI.output_folder_path = os.path.normpath(new_folder_name)
        self.GUI.statusBar.showMessage("Обработка")
        self.GUI.folderButton.setEnabled(False)
        self.GUI.watermarkButton.setEnabled(False)
        self.GUI.processingButton.setEnabled(False)
        self.GUI.watermarkPosition.setEnabled(False)

        if os.path.exists(new_folder_name):
            shutil.rmtree(new_folder_name)

        os.mkdir(new_folder_name)

        images_number = len(os.listdir(input_image_path))
        current_image = 0
        for input_image in os.listdir(input_image_path):  # обрабатываются все изображения, находящиеся в папке
            left_part, right_part = os.path.splitext(input_image)
            if right_part.lower() not in ['.png', '.bmp', '.jpg', '.gif']:
                continue
            wm_left_part, wm_right_part = os.path.splitext(watermark_image_path)
            output_image = left_part + "_watermarked.jpg"  # получаем новое имя для файла
            base_image = Image.open(input_image_path + "\\" + input_image)  # открываем исходное изображение
            watermark = Image.open(watermark_image_path)  # открываем изображение водяного знака
            width, height = base_image.size  # получаем высоту и ширину исходного изображения
            wm_width, wm_height = watermark.size
            if self.GUI.position_index == 1:
                position = (0, 0)
            elif self.GUI.position_index == 2:
                position = (0, height - wm_height)
            elif self.GUI.position_index == 3:
                position = (width - wm_width, 0)
            elif self.GUI.position_index == 4:
                position = (width - wm_width, height - wm_height)
            transparent = Image.new('RGB', (width, height),
                                    (0, 0, 0, 0))  # создаем новое изображение с высотой и шириной исходного
            transparent.paste(base_image, (0, 0))  # вставляем исходное изображение в новое
            if wm_right_part.lower() == '.png':
                transparent.paste(watermark, position, mask=watermark)
            elif wm_right_part.lower() == '.jpg' or right_part.lower() == '.bmp' or right_part.lower() == '.gif':
                transparent.paste(watermark, position)
            transparent.save(
                new_folder_name + "\\" + output_image)  # сохраняем полученное изображение во вновь созданной папке под новым именем
            current_image += 1
            # self.progressBar.setValue(round((current_image/images_number) * 100))
            self.GUI.progressBar.setValue(current_image)

        self.GUI.folderButton.setEnabled(True)
        self.GUI.watermarkButton.setEnabled(True)
        self.GUI.processingButton.setEnabled(True)
        self.GUI.watermarkPosition.setEnabled(True)
        self.GUI.openOutputFolderButton.setEnabled(True)