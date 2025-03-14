# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DevInfo.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)
import rec_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(917, 362)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"")
        self.background = QLabel(Dialog)
        self.background.setObjectName(u"background")
        self.background.setGeometry(QRect(0, 0, 691, 441))
        sizePolicy.setHeightForWidth(self.background.sizePolicy().hasHeightForWidth())
        self.background.setSizePolicy(sizePolicy)
        self.background.setPixmap(QPixmap(u":/images/images/dev-background-light.jpg"))
        self.background.setScaledContents(True)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info = QFrame(Dialog)
        self.info.setObjectName(u"info")
        self.info.setGeometry(QRect(0, 0, 481, 181))
        self.info.setFrameShape(QFrame.Shape.StyledPanel)
        self.info.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.info)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.info)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(True)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.info)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)

        self.label_6 = QLabel(self.info)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.verticalLayout.addWidget(self.label_6)

        self.label_4 = QLabel(self.info)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(self.info)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout.addWidget(self.label_5)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u041e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0435", None))
        self.background.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441 \u0434\u043b\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u0441 \u0431\u0430\u0437\u043e\u0439 \u0434\u0430\u043d\u043d\u044b\u0445 SQLite", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u0420\u0430\u0431\u043e\u0442\u0443 \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u043b: \u0441\u0442\u0443\u0434\u0435\u043d\u0442", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u0424\u043e\u0440\u043c\u0430 \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u044f: \u043e\u0447\u043d\u0430\u044f", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u0424\u0418\u041e: \u0424\u0435\u0434\u043e\u0440\u043e\u0432 \u041c\u0438\u0445\u0430\u0438\u043b \u0415\u0432\u0433\u0435\u043d\u044c\u0435\u0432\u0438\u0447", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u0413\u0440\u0443\u043f\u043f\u0430: \u0431\u041f\u041e-221", None))
    # retranslateUi

