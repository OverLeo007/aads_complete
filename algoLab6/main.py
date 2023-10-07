from ui_src import SettingsWindow, QApplication, sys


def main():
    """

    """
    app = QApplication([])
    application = SettingsWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
