# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProgInfo.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QFrame,
    QLabel, QLayout, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)
import rec_rc

class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(866, 725)
        self.background = QLabel(dialog)
        self.background.setObjectName(u"background")
        self.background.setGeometry(QRect(30, 10, 311, 101))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.background.sizePolicy().hasHeightForWidth())
        self.background.setSizePolicy(sizePolicy)
        self.background.setPixmap(QPixmap(u":/images/images/dev-background-light.jpg"))
        self.background.setScaledContents(True)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info = QFrame(dialog)
        self.info.setObjectName(u"info")
        self.info.setGeometry(QRect(120, 120, 621, 421))
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

        self.label_4 = QLabel(self.info)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setPointSize(10)
        self.label_4.setFont(font1)

        self.verticalLayout.addWidget(self.label_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_6 = QLabel(self.info)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_6)

        self.textEdit_2 = QTextEdit(self.info)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)
        self.textEdit_2.setFrameShape(QFrame.Shape.WinPanel)
        self.textEdit_2.setFrameShadow(QFrame.Shadow.Plain)
        self.textEdit_2.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.textEdit_2.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.textEdit_2)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_5 = QLabel(self.info)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_5)

        self.textEdit = QTextEdit(self.info)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy2)
        self.textEdit.setFrameShape(QFrame.Shape.WinPanel)
        self.textEdit.setFrameShadow(QFrame.Shadow.Plain)
        self.textEdit.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textEdit)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"\u041e \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0438", None))
        self.background.setText("")
        self.label_2.setText(QCoreApplication.translate("dialog", u"\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441 \u0434\u043b\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u0441 \u0431\u0430\u0437\u043e\u0439 \u0434\u0430\u043d\u043d\u044b\u0445 SQLite", None))
        self.label_4.setText(QCoreApplication.translate("dialog", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f: SQLite", None))
        self.label_6.setText(QCoreApplication.translate("dialog", u"\u041e\u0441\u043d\u043e\u0432\u043d\u044b\u0435 \u0444\u0443\u043d\u043a\u0446\u0438\u0438:", None))
        self.textEdit_2.setHtml(QCoreApplication.translate("dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Not"
                        "o Sans','sans-serif'; font-size:14px; font-weight:700; color:#222222; background-color:#ffffff;\">\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0431\u0430\u0437 \u0434\u0430\u043d\u043d\u044b\u0445:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; color:#222222; background-color:#ffffff;\">    - \u043b\u0435\u0433\u043a\u043e \u0441\u043e\u0437\u0434\u0430\u0432\u0430\u0439\u0442\u0435 \u043d\u043e"
                        "\u0432\u044b\u0435 \u0431\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445 \u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u0443\u0439\u0442\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u044e\u0449\u0438\u0435 \u043f\u0440\u0438 \u043f\u043e\u043c\u043e\u0449\u0438 \u043f\u0440\u043e\u0441\u0442\u043e\u0433\u043e \u0432 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0438 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','N"
                        "oto Sans','sans-serif'; font-size:14px; font-weight:700; color:#222222; background-color:#ffffff;\">\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u0430\u043c\u0438:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; color:#222222; background-color:#ffffff;\">    - \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0439\u0442\u0435, \u0443\u0434\u0430\u043b\u044f\u0439\u0442\u0435 \u0438 \u0438\u0437\u043c\u0435\u043d\u044f\u0439\u0442\u0435 \u0442\u0430"
                        "\u0431\u043b\u0438\u0446\u044b, \u0430 \u0442\u0430\u043a\u0436\u0435 \u043d\u0430\u0441\u0442\u0440\u0430\u0438\u0432\u0430\u0439\u0442\u0435 \u0438\u0445 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0443, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u0442\u0438\u043f\u044b \u0434\u0430\u043d\u043d\u044b\u0445 \u0438 \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u0438\u044f.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; font-weight:700; color:#222222; background-color:#fffff"
                        "f;\">\u0418\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; color:#222222; background-color:#ffffff;\">    - \u043d\u0430\u0431\u043b\u044e\u0434\u0430\u0439\u0442\u0435 \u0437\u0430 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f\u043c\u0438 \u0432 \u0431\u0430\u0437\u0435 \u0434\u0430\u043d\u043d\u044b\u0445 \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u0432\u0440\u0435\u043c\u0435\u043d"
                        "\u0438. \u0421\u043e\u0434\u0435\u0440\u0436\u0438\u043c\u043e\u0435 \u0434\u0438\u043d\u0430\u043c\u0438\u0447\u0435\u0441\u043a\u0438 \u043e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u0432\u043e \u0438\u0437\u0431\u0435\u0436\u0430\u043d\u0438\u0435 \u043e\u0448\u0438\u0431\u043e\u043a.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; font-weight:700; color:#222222; background-color:#ffffff;\">\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 SQL-\u0437\u0430\u043f"
                        "\u0440\u043e\u0441\u043e\u0432:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; background-color:#ffffff;\"><span style=\" font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; color:#222222; background-color:#ffffff;\">    - \u0438\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440 SQL \u0441 \u043f\u043e\u0434\u0441\u0432\u0435\u0442\u043a\u043e\u0439 \u0441\u0438\u043d\u0442\u0430\u043a\u0441\u0438\u0441\u0430 \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u0435\u0442 \u043f\u0438\u0441\u0430\u0442\u044c \u0438 \u0432"
                        "\u044b\u043f\u043e\u043b\u043d\u044f\u0442\u044c \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u0432 \u0440\u0435\u0430\u043b\u044c\u043d\u043e\u043c \u0432\u0440\u0435\u043c\u0435\u043d\u0438, \u0447\u0442\u043e \u0443\u043f\u0440\u043e\u0449\u0430\u0435\u0442 \u0440\u0430\u0431\u043e\u0442\u0443 \u0441 \u0434\u0430\u043d\u043d\u044b\u043c\u0438.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:150%; font-family:'DDG_ProximaNova','DDG_ProximaNova_UI_0','DDG_ProximaNova_UI_1','DDG_ProximaNova_UI_2','DDG_ProximaNova_UI_3','DDG_ProximaNova_UI_4','DDG_ProximaNova_UI_5','DDG_ProximaNova_UI_6','Proxima Nova','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Oxygen-Sans','Ubuntu','Cantarell','Helvetica Neue','Arial','Noto Sans','sans-serif'; font-size:14px; color:#222222; background-color:#ffffff;\"><br /></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("dialog", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:", None))
        self.textEdit.setHtml(QCoreApplication.translate("dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    SQLite \u2014 \u044d\u0442\u043e \u043c\u043e\u0449\u043d\u044b\u0439 \u0438 \u0438\u043d\u0442\u0443\u0438\u0442\u0438\u0432\u043d\u043e \u043f\u043e\u043d\u044f\u0442\u043d\u044b\u0439 \u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441 \u0434\u043b\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u0441 \u0431\u0430\u0437\u0430\u043c"
                        "\u0438 \u0434\u0430\u043d\u043d\u044b\u0445 SQLite. \u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043f\u0440\u0435\u0434\u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u043e \u043a\u0430\u043a \u0434\u043b\u044f \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432, \u0442\u0430\u043a \u0438 \u0434\u043b\u044f \u043e\u043f\u044b\u0442\u043d\u044b\u0445 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439, \u043f\u0440\u0435\u0434\u043e\u0441\u0442\u0430\u0432\u043b\u044f\u044f \u0432\u0441\u0435 \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u0435 \u0438\u043d\u0441\u0442\u0440\u0443\u043c\u0435\u043d\u0442\u044b \u0434\u043b\u044f \u044d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u043e\u0433\u043e \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f \u0434\u0430\u043d\u043d\u044b\u043c\u0438.</p></body></html>", None))
    # retranslateUi

