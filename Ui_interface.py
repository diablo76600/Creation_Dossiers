# -*- Coding: utf-8 -*-
# Created by G@rk@m76 on 03/05/2024 -- 22:23:20.

import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from create_folders import create_folder  # Import de la fonction create_folder


class MainWindow(QtWidgets.QMainWindow):
    """Classe MainWindow pour l'interface utilisateur de création de dossiers.
    La classe MainWindow gère l'interface graphique pour la création de dossiers avec des fonctionnalités telles que la sélection de dates, de dossiers, et la création de sous-dossiers."""
    def __init__(self):
        super().__init__()
        self.resize(530, 332)  # Définition de la taille de la fenêtre principale
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(10, 10, 510, 316)
        )  # Définition de la géométrie du widget de la grille
        self.gridLayout = QtWidgets.QGridLayout(
            self.gridLayoutWidget
        )  # Création d'une grille pour organiser les éléments de l'interface
        self.gridLayout.setContentsMargins(
            0, 0, 0, 0
        )  # Définition des marges de la grille

        today = QtCore.QDate.currentDate()  # Récupération de la date du jour

        # Création des labels et des éditeurs de date pour la date de début et la date de fin
        self.label_date_start = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_date_start, 0, 0, 1, 1)
        self.date_edit_start = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.date_edit_start.setCalendarPopup(True)
        self.date_edit_start.setDate(today)
        self.date_edit_start.dateChanged.connect(self.update_date)
        self.gridLayout.addWidget(self.date_edit_start, 0, 1, 1, 1)
        #
        self.label_date_end = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_date_end, 1, 0, 1, 1)
        self.date_edit_end = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.date_edit_end.setCalendarPopup(True)
        self.date_edit_end.setDate(today)
        self.gridLayout.addWidget(self.date_edit_end, 1, 1, 1, 1)

        # Créarion du checkbox fusion
        self.checkbox = QtWidgets.QCheckBox(self)
        self.checkbox.setText("Fusion")
        self.gridLayout.addWidget(self.checkbox, 1, 2, 1, 1)

        # Création de l'étiquette, de l'éditeur de ligne et du bouton pour choisir le dossier de destination
        self.label_choice_folder = QtWidgets.QLabel(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label_choice_folder, 2, 0, 1, 1)
        self.line_choice_folder = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.line_choice_folder, 2, 1, 1, 1)
        self.push_button_choice_folder = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_choice_folder.clicked.connect(self.set_current_path)
        self.gridLayout.addWidget(self.push_button_choice_folder, 2, 2, 1, 1)

        # Création d'une ligne de séparation
        self.separator_1 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.separator_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator_1.setLineWidth(4)
        self.gridLayout.addWidget(self.separator_1, 3, 0, 2, 3)

        # Création de l'étiquette pour les sous-dossiers
        self.label_subfolder = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_subfolder.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(
            self.label_subfolder, 4, 1, 1, 1)

        # Création des étiquettes et des éditeurs de ligne pour les sous-dossiers
        for i in range(1, 4):
            label_subfolder = QtWidgets.QLabel(self.gridLayoutWidget)
            label_subfolder.setText(f"Sous-dossier {i} :")
            self.gridLayout.addWidget(label_subfolder, i + 4, 0, 1, 1)
            #
            line_edit_subfolder = QtWidgets.QLineEdit(self.gridLayoutWidget)
            setattr(self, f"line_edit_subfolder_{i}", line_edit_subfolder)
            self.gridLayout.addWidget(line_edit_subfolder, i + 4, 1, 1, 1)

        # Création d'une autre ligne de séparation
        self.separator_2 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.separator_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator_2.setLineWidth(4)
        self.gridLayout.addWidget(self.separator_2, 8, 0, 2, 3)

        # Création du bouton OK
        self.push_button_ok = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.push_button_ok.setMaximumSize(QtCore.QSize(64, 32))
        self.push_button_ok.clicked.connect(self.get_values)
        self.gridLayout.addWidget(
            self.push_button_ok, 9, 0, 2, 0, QtCore.Qt.AlignHCenter
        )

        # Définition du widget de la grille comme widget central
        self.setCentralWidget(self.gridLayoutWidget)

        # Appel de la fonction retranslateUi pour traduire les textes de l'interface
        self.retranslateUi()

    def retranslateUi(self):
        """ Traduction des textes de l'interface."""
        self.setWindowTitle("Création Dossiers")
        self.push_button_choice_folder.setText("Choisir")
        self.label_date_end.setText(" Date de fin :")
        self.label_date_start.setText(" Date de début : ")
        self.label_subfolder.setText("Création des sous-dossiers (optionnel) :")
        self.label_choice_folder.setText(" Dossier de destination :")
        self.push_button_ok.setText("Ok")

    def update_date(self):
        self.date_edit_end.setDate(self.date_edit_start.date())

    def set_current_path(self):
        """Définit le chemin actuel en fonction du dossier sélectionné 
            par l'utilisateur à l'aide d'une boîte de dialogue de sélection de dossier."""
        current_path = QFileDialog.getExistingDirectory(
            self, "Selectionnez ou créez un dossier", str(Path.home())
        )
        self.line_choice_folder.setText(current_path)

    def get_values(self):
        """Récupère les valeurs de la date de début, de fin, 
            du dossier courant et des sous-dossiers saisis dans l'interface utilisateur."""
        try:
            start_date = self.date_edit_start.date().toPyDate()
            end_date = self.date_edit_end.date().toPyDate()
            current_folder = self.line_choice_folder.text()
            if not current_folder:
                raise ValueError("Veuillez saisir un Dossier de destination !!")

            subfolders = []
            for i in range(1, 4):
                line_edit = getattr(self, f"line_edit_subfolder_{i}")
                subfolder = line_edit.text() or None
                subfolders.append(subfolder)

            if create_folder(start_date, end_date, current_folder, subfolders, self.checkbox):
                message = "Création des dossiers réussis."
            else:
                raise ValueError("Problème de date !!")

        except ValueError as error:
            self.display_message(
                QMessageBox.Icon.Warning,
                str(error),
            )
        else:
            self.display_message(
                QMessageBox.Icon.Information,
                message,
            )

    @staticmethod
    def display_message(icon, message):
        """Affiche un message à l'utilisateur 
            avec une icône spécifiée et un message donné."""
        QMessageBox(icon, "", message).exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Translate
    translators = []
    translator = QtCore.QTranslator()
    traduction = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("qtbase_fr.qm", traduction)
    app.installTranslator(translator)
    #
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
