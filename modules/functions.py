from PyQt5.QtWidgets import *


def save(sender, path):
    """
    :param sender: QTabWidget
    :param path: str, file path
    """
    try:
        text_edit = sender.currentWidget()
        text = text_edit.toPlainText()
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(text)
    except Exception as e:
        create_error_msg(f'Save error: {e}')


def save_as(sender):
    """
    :param sender:  QTabWidget
    :return: tuple (None, None) or tuple (str, str)
    """
    try:
        fpath = QFileDialog.getSaveFileName()[0]
        if fpath != '':
            text_edit = sender.currentWidget()
            text = text_edit.toPlainText()

            with open(fpath, 'w', encoding='UTF-8') as f:
                f.write(text)
        else:
            return None, None

    except Exception as e:
        create_error_msg(f"Save as error: {e}")
    else:
        # если файл открылся удачно, записываем название файла и если файл расширения .py
        # то сразу ставим подсветку синтакса питона
        name = fpath.split('/')[-1]
        sender.setTabText(sender.currentIndex(), name)
        if name.endswith('.py'):
            sender.currentWidget().set_lang('python')
        return fpath, name


def create_save_file_msg():
    """
    Creates save file QMessageBox
    """
    msg = QMessageBox()
    msg.setWindowTitle('Save changes')
    msg.setIcon(QMessageBox.Question)
    msg.setText('Save file')
    msg.setInformativeText('Do you want to save changes before closing the file?')
    msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Save)
    return msg.exec()


def create_error_msg(e):
    """
    Creates error QMessageBox
    :param e: Exception
    """
    er = QMessageBox()
    er.setWindowTitle('Error')
    er.setIcon(QMessageBox.Critical)
    er.setText(str(e))
    er.exec()