# System imports
import glob
import os
import os.path as osp
import sys

# Third party imports
import numpy as np

# import PyQt5
from PyQt5 import uic

# local imports
from .dna_cryptography import *

# Load and preconfigure GUI from UI file
self_wd = osp.abspath(osp.dirname(__file__))
(Ui_MainWindow, QMainWindow) = uic.loadUiType(osp.join(self_wd, 'gui', 'mainwindow.ui'))

class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup paths
        self.wd = osp.abspath(osp.dirname(__file__))

        # Connect signals to SLOTs
        self.ui.encryption_button.clicked.connect(self._encrypt_button_clicked)
        self.ui.decrypt_button.clicked.connect(self._decrypt_button_clicked)

    def _encrypt_button_clicked(self):
        # Convert message to binary
        self.m_enc = self.ui.enc_M_text.toPlainText()
        self.M_enc = text_to_bits(self.m_enc)

        # Generate key
        self.K_enc = generate_K(len(self.M_enc)*7*10) # 7 бит в каждой букве
        self.ui.enc_K_text.setText(str(self.K_enc))

        # Encrypt M to C using K
        self.C_enc = encrypt(self.K_enc, self.M_enc)
        self.ui.enc_C_text.setText('\n'.join(self.C_enc))

    def _decrypt_button_clicked(self):
        # Get encrypted message and key
        self.C_dec = [i for i in self.ui.dec_C_text.toPlainText().split('\n')]
        self.K_dec = self.ui.dec_K_text.toPlainText()

        # Decrypt message C to M using K
        self.M_dec = decrypt(self.K_dec, self.C_dec)

        # Convert binary to text again
        self.m_dec = text_from_bits(self.M_dec)
        self.ui.dec_M_text.setText(str(self.m_dec))

    def __del__(self):
        self.ui = None

#-----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Linux visual style
    app.setApplicationName('DNACipher')

    # create widget
    w = MainWindow()
    w.setWindowTitle('DNA Cipher')
    w.show()

    app.installEventFilter(w)

    # execute application
    sys.exit(app.exec_())