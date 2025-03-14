# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 179)
        Dialog.setStyleSheet(u"QWidget {\n"
"    background-color: rgb(244,226,226);\n"
"	font-size: 15px;\n"
"	font-weight: 300;\n"
"}")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)

        self.AllTablesCheckBox = QCheckBox(Dialog)
        self.AllTablesCheckBox.setObjectName(u"AllTablesCheckBox")
        sizePolicy.setHeightForWidth(self.AllTablesCheckBox.sizePolicy().hasHeightForWidth())
        self.AllTablesCheckBox.setSizePolicy(sizePolicy)
        self.AllTablesCheckBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.AllTablesCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.AllTablesCheckBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.SaveChangesButton = QPushButton(Dialog)
        self.SaveChangesButton.setObjectName(u"SaveChangesButton")

        self.verticalLayout.addWidget(self.SaveChangesButton)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
#if QT_CONFIG(tooltip)
        self.AllTablesCheckBox.setToolTip(QCoreApplication.translate("Dialog", u"\u041f\u0440\u0438 \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u0438 \u0441\u043f\u0438\u0441\u043a\u0430 \u0442\u0430\u0431\u043b\u0438\u0446 \u0431\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445 \u0432\u0441\u0435 \u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435 \u0441\u043a\u0440\u044b\u0432\u0430\u044e\u0442\u0441\u044f", None))
#endif // QT_CONFIG(tooltip)
        self.AllTablesCheckBox.setText(QCoreApplication.translate("Dialog", u"\u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u043e\u0434\u043d\u043e\u0439 \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
        self.SaveChangesButton.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
    # retranslateUi

