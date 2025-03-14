# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SQLite_2.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import rec_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(615, 317)
        Dialog.setStyleSheet(u"QWidget {\n"
"    background-color: rgb(244,226,226);\n"
"	font-size: 15px;\n"
"	font-weight: 300;\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 5, 5, 5)
        self.WindowHeaderLabel = QLabel(Dialog)
        self.WindowHeaderLabel.setObjectName(u"WindowHeaderLabel")
        self.WindowHeaderLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WindowHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.WindowHeaderLabel.setMargin(0)

        self.verticalLayout_2.addWidget(self.WindowHeaderLabel)

        self.TableName = QLineEdit(Dialog)
        self.TableName.setObjectName(u"TableName")
        self.TableName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.TableName)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 599, 249))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.TypeDataComboBox_0 = QComboBox(self.scrollAreaWidgetContents)
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.addItem("")
        self.TypeDataComboBox_0.setObjectName(u"TypeDataComboBox_0")

        self.gridLayout.addWidget(self.TypeDataComboBox_0, 1, 1, 1, 1)

        self.UNLabel = QLabel(self.scrollAreaWidgetContents)
        self.UNLabel.setObjectName(u"UNLabel")
        self.UNLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.UNLabel.setMargin(4)

        self.gridLayout.addWidget(self.UNLabel, 0, 6, 1, 1)

        self.AttributeLabel = QLabel(self.scrollAreaWidgetContents)
        self.AttributeLabel.setObjectName(u"AttributeLabel")

        self.gridLayout.addWidget(self.AttributeLabel, 0, 0, 1, 1)

        self.UQLabel = QLabel(self.scrollAreaWidgetContents)
        self.UQLabel.setObjectName(u"UQLabel")
        self.UQLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.UQLabel.setMargin(4)

        self.gridLayout.addWidget(self.UQLabel, 0, 4, 1, 1)

        self.PKLabel = QLabel(self.scrollAreaWidgetContents)
        self.PKLabel.setObjectName(u"PKLabel")
        self.PKLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PKLabel.setMargin(4)

        self.gridLayout.addWidget(self.PKLabel, 0, 2, 1, 1)

        self.AddRowButton_0 = QPushButton(self.scrollAreaWidgetContents)
        self.AddRowButton_0.setObjectName(u"AddRowButton_0")
        icon = QIcon()
        icon.addFile(u":/icons/icons/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AddRowButton_0.setIcon(icon)

        self.gridLayout.addWidget(self.AddRowButton_0, 1, 7, 1, 1)

        self.DelRowButton_0 = QPushButton(self.scrollAreaWidgetContents)
        self.DelRowButton_0.setObjectName(u"DelRowButton_0")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.DelRowButton_0.setIcon(icon1)

        self.gridLayout.addWidget(self.DelRowButton_0, 1, 8, 1, 1)

        self.TypeDataLabel = QLabel(self.scrollAreaWidgetContents)
        self.TypeDataLabel.setObjectName(u"TypeDataLabel")

        self.gridLayout.addWidget(self.TypeDataLabel, 0, 1, 1, 1)

        self.BLabel = QLabel(self.scrollAreaWidgetContents)
        self.BLabel.setObjectName(u"BLabel")
        self.BLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.BLabel.setMargin(4)

        self.gridLayout.addWidget(self.BLabel, 0, 5, 1, 1)

        self.NNLabel = QLabel(self.scrollAreaWidgetContents)
        self.NNLabel.setObjectName(u"NNLabel")
        self.NNLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.NNLabel.setMargin(4)

        self.gridLayout.addWidget(self.NNLabel, 0, 3, 1, 1)

        self.lineEdit_0 = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_0.setObjectName(u"lineEdit_0")

        self.gridLayout.addWidget(self.lineEdit_0, 1, 0, 1, 1)

        self.widget_1_0 = QWidget(self.scrollAreaWidgetContents)
        self.widget_1_0.setObjectName(u"widget_1_0")
        self.verticalLayout = QVBoxLayout(self.widget_1_0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.PKcheckBox_0 = QCheckBox(self.widget_1_0)
        self.PKcheckBox_0.setObjectName(u"PKcheckBox_0")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PKcheckBox_0.sizePolicy().hasHeightForWidth())
        self.PKcheckBox_0.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.PKcheckBox_0)


        self.gridLayout.addWidget(self.widget_1_0, 1, 2, 1, 1)

        self.widget_2_0 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2_0.setObjectName(u"widget_2_0")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2_0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.NNcheckBox_0 = QCheckBox(self.widget_2_0)
        self.NNcheckBox_0.setObjectName(u"NNcheckBox_0")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.NNcheckBox_0.sizePolicy().hasHeightForWidth())
        self.NNcheckBox_0.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.NNcheckBox_0)


        self.gridLayout.addWidget(self.widget_2_0, 1, 3, 1, 1)

        self.widget_3_0 = QWidget(self.scrollAreaWidgetContents)
        self.widget_3_0.setObjectName(u"widget_3_0")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3_0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.UQcheckBox_0 = QCheckBox(self.widget_3_0)
        self.UQcheckBox_0.setObjectName(u"UQcheckBox_0")
        sizePolicy.setHeightForWidth(self.UQcheckBox_0.sizePolicy().hasHeightForWidth())
        self.UQcheckBox_0.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.UQcheckBox_0)


        self.gridLayout.addWidget(self.widget_3_0, 1, 4, 1, 1)

        self.widget_4_0 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4_0.setObjectName(u"widget_4_0")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4_0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.BcheckBox_0 = QCheckBox(self.widget_4_0)
        self.BcheckBox_0.setObjectName(u"BcheckBox_0")
        sizePolicy.setHeightForWidth(self.BcheckBox_0.sizePolicy().hasHeightForWidth())
        self.BcheckBox_0.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.BcheckBox_0)


        self.gridLayout.addWidget(self.widget_4_0, 1, 5, 1, 1)

        self.widget_5_0 = QWidget(self.scrollAreaWidgetContents)
        self.widget_5_0.setObjectName(u"widget_5_0")
        self.verticalLayout_6 = QVBoxLayout(self.widget_5_0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.UNcheckBox_0 = QCheckBox(self.widget_5_0)
        self.UNcheckBox_0.setObjectName(u"UNcheckBox_0")
        sizePolicy.setHeightForWidth(self.UNcheckBox_0.sizePolicy().hasHeightForWidth())
        self.UNcheckBox_0.setSizePolicy(sizePolicy)

        self.verticalLayout_6.addWidget(self.UNcheckBox_0)


        self.gridLayout.addWidget(self.widget_5_0, 1, 6, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.SaveButton = QPushButton(self.scrollAreaWidgetContents)
        self.SaveButton.setObjectName(u"SaveButton")
        self.SaveButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SaveButton.setIcon(icon2)

        self.verticalLayout_7.addWidget(self.SaveButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u0435\u0439", None))
        self.WindowHeaderLabel.setText(QCoreApplication.translate("Dialog", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0432 \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445:", None))
        self.TableName.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
        self.TypeDataComboBox_0.setItemText(0, QCoreApplication.translate("Dialog", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435...", None))
        self.TypeDataComboBox_0.setItemText(1, QCoreApplication.translate("Dialog", u"TEXT", None))
        self.TypeDataComboBox_0.setItemText(2, QCoreApplication.translate("Dialog", u"INTEGER", None))
        self.TypeDataComboBox_0.setItemText(3, QCoreApplication.translate("Dialog", u"REAL", None))
        self.TypeDataComboBox_0.setItemText(4, QCoreApplication.translate("Dialog", u"DATE", None))
        self.TypeDataComboBox_0.setItemText(5, QCoreApplication.translate("Dialog", u"DATETIME", None))
        self.TypeDataComboBox_0.setItemText(6, QCoreApplication.translate("Dialog", u"BOOLEAN", None))

#if QT_CONFIG(tooltip)
        self.UNLabel.setToolTip(QCoreApplication.translate("Dialog", u"Unsigned data type", None))
#endif // QT_CONFIG(tooltip)
        self.UNLabel.setText(QCoreApplication.translate("Dialog", u"UN", None))
        self.AttributeLabel.setText(QCoreApplication.translate("Dialog", u"\u041f\u043e\u043b\u0435", None))
#if QT_CONFIG(tooltip)
        self.UQLabel.setToolTip(QCoreApplication.translate("Dialog", u"Unique Constraint", None))
#endif // QT_CONFIG(tooltip)
        self.UQLabel.setText(QCoreApplication.translate("Dialog", u"UQ", None))
#if QT_CONFIG(tooltip)
        self.PKLabel.setToolTip(QCoreApplication.translate("Dialog", u"Primary Key", None))
#endif // QT_CONFIG(tooltip)
        self.PKLabel.setText(QCoreApplication.translate("Dialog", u"PK", None))
        self.AddRowButton_0.setText("")
        self.DelRowButton_0.setText("")
        self.TypeDataLabel.setText(QCoreApplication.translate("Dialog", u"\u0422\u0438\u043f \u0434\u0430\u043d\u043d\u044b\u0445", None))
#if QT_CONFIG(tooltip)
        self.BLabel.setToolTip(QCoreApplication.translate("Dialog", u"BLOB", None))
#endif // QT_CONFIG(tooltip)
        self.BLabel.setText(QCoreApplication.translate("Dialog", u"B", None))
#if QT_CONFIG(tooltip)
        self.NNLabel.setToolTip(QCoreApplication.translate("Dialog", u"Not Null", None))
#endif // QT_CONFIG(tooltip)
        self.NNLabel.setText(QCoreApplication.translate("Dialog", u"NN", None))
        self.PKcheckBox_0.setText("")
        self.NNcheckBox_0.setText("")
        self.UQcheckBox_0.setText("")
        self.BcheckBox_0.setText("")
        self.UNcheckBox_0.setText("")
        self.SaveButton.setText(QCoreApplication.translate("Dialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
    # retranslateUi

