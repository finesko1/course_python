# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SQLite.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)
import rec_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(843, 496)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: rgb(244,226,226);\n"
"	font-size: 15px;\n"
"	font-weight: 300;\n"
"}\n"
"\n"
"/*\u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e*/\n"
"QMenuBar {\n"
"    background-color: rgb(244,220,240);\n"
"    color: #2c2c2c; \n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background-color: transparent; \n"
"    color: #000000; \n"
"    padding: 5px 20px;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    padding: 1px;\n"
"	border: 1px solid rgba(0,128,255, 1); /* \u041f\u0440\u0438\u043c\u0435\u0440 \u0442\u0435\u043d\u0438 \u0441 \u043f\u043e\u043c\u043e\u0449\u044c\u044e \u0433\u0440\u0430\u043d\u0438\u0446\u044b */\n"
"	border-radius: 5px;\n"
"    background-color: rgb(244,220,240);\n"
"    color: rgb(0,128,255); \n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background-color: rgb(244,220,240);\n"
"    color: #2c2c2c; \n"
"}\n"
"\n"
"/*\u0412\u044b\u043f\u0430\u0434\u0430\u044e\u0449\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043c\u0435\u043d\u044e*/\n"
""
                        "QMenu {\n"
"    background-color: rgb(244,220,240);\n"
"    color: #2c2c2c; \n"
"}\n"
"\n"
"QMenu::item {\n"
"    background-color: transparent; \n"
"    color: #000000;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"	padding: 1px;\n"
"	border: 1px solid rgba(0,128,255, 1); /* \u041f\u0440\u0438\u043c\u0435\u0440 \u0442\u0435\u043d\u0438 \u0441 \u043f\u043e\u043c\u043e\u0449\u044c\u044e \u0433\u0440\u0430\u043d\u0438\u0446\u044b */\n"
"	border-radius: 5px;\n"
"    background-color: rgb(244,220,240);\n"
"    color: rgb(0,128,255); \n"
"}")
        self.DeveloperInfoAction = QAction(MainWindow)
        self.DeveloperInfoAction.setObjectName(u"DeveloperInfoAction")
        icon = QIcon()
        icon.addFile(u":/icons/icons/developer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.DeveloperInfoAction.setIcon(icon)
        self.ProgrammInfoAction = QAction(MainWindow)
        self.ProgrammInfoAction.setObjectName(u"ProgrammInfoAction")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/info.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ProgrammInfoAction.setIcon(icon1)
        self.SettingsAction = QAction(MainWindow)
        self.SettingsAction.setObjectName(u"SettingsAction")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SettingsAction.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.WorkDirectoryLabel = QLabel(self.frame)
        self.WorkDirectoryLabel.setObjectName(u"WorkDirectoryLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.WorkDirectoryLabel.sizePolicy().hasHeightForWidth())
        self.WorkDirectoryLabel.setSizePolicy(sizePolicy1)
        self.WorkDirectoryLabel.setMinimumSize(QSize(116, 0))
        self.WorkDirectoryLabel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.WorkDirectoryLabel.setAutoFillBackground(False)

        self.horizontalLayout.addWidget(self.WorkDirectoryLabel)

        self.SelectWorkDirectoryLabel = QLabel(self.frame)
        self.SelectWorkDirectoryLabel.setObjectName(u"SelectWorkDirectoryLabel")
        sizePolicy1.setHeightForWidth(self.SelectWorkDirectoryLabel.sizePolicy().hasHeightForWidth())
        self.SelectWorkDirectoryLabel.setSizePolicy(sizePolicy1)
        self.SelectWorkDirectoryLabel.setMinimumSize(QSize(180, 0))

        self.horizontalLayout.addWidget(self.SelectWorkDirectoryLabel)

        self.SelectFolderButton = QPushButton(self.frame)
        self.SelectFolderButton.setObjectName(u"SelectFolderButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.SelectFolderButton.sizePolicy().hasHeightForWidth())
        self.SelectFolderButton.setSizePolicy(sizePolicy2)
        self.SelectFolderButton.setMinimumSize(QSize(75, 0))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SelectFolderButton.setIcon(icon3)

        self.horizontalLayout.addWidget(self.SelectFolderButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.LabelQuery = QLabel(self.frame)
        self.LabelQuery.setObjectName(u"LabelQuery")

        self.horizontalLayout.addWidget(self.LabelQuery)

        self.AddQueryButton = QPushButton(self.frame)
        self.AddQueryButton.setObjectName(u"AddQueryButton")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/add.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AddQueryButton.setIcon(icon4)

        self.horizontalLayout.addWidget(self.AddQueryButton)

        self.DelQueryButton = QPushButton(self.frame)
        self.DelQueryButton.setObjectName(u"DelQueryButton")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.DelQueryButton.setIcon(icon5)

        self.horizontalLayout.addWidget(self.DelQueryButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.DatabasesScrollArea = QScrollArea(self.frame)
        self.DatabasesScrollArea.setObjectName(u"DatabasesScrollArea")
        self.DatabasesScrollArea.setMaximumSize(QSize(400, 16777215))
        self.DatabasesScrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.DatabasesScrollArea.setLineWidth(0)
        self.DatabasesScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.DatabasesScrollArea.setWidgetResizable(True)
        self.DatabasesScrollArea.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 411))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.DatabasesWidget = QWidget(self.scrollAreaWidgetContents)
        self.DatabasesWidget.setObjectName(u"DatabasesWidget")
        sizePolicy.setHeightForWidth(self.DatabasesWidget.sizePolicy().hasHeightForWidth())
        self.DatabasesWidget.setSizePolicy(sizePolicy)
        self.DatabasesWidget.setAutoFillBackground(False)
        self.verticalLayout_5 = QVBoxLayout(self.DatabasesWidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.DatabasesVBoxLayoutForWidget = QVBoxLayout()
        self.DatabasesVBoxLayoutForWidget.setObjectName(u"DatabasesVBoxLayoutForWidget")

        self.verticalLayout_5.addLayout(self.DatabasesVBoxLayoutForWidget)


        self.verticalLayout_6.addWidget(self.DatabasesWidget, 0, Qt.AlignmentFlag.AlignTop)

        self.DatabasesScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.DatabasesScrollArea)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TabWidget = QTabWidget(self.frame)
        self.TabWidget.setObjectName(u"TabWidget")
        sizePolicy.setHeightForWidth(self.TabWidget.sizePolicy().hasHeightForWidth())
        self.TabWidget.setSizePolicy(sizePolicy)
        self.TabWidget.setMinimumSize(QSize(0, 150))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setMouseTracking(False)
        self.tab.setTabletTracking(False)
        self.TabWidget.addTab(self.tab, "")

        self.verticalLayout.addWidget(self.TabWidget)

        self.ExecuteQueryButton = QPushButton(self.frame)
        self.ExecuteQueryButton.setObjectName(u"ExecuteQueryButton")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.ExecuteQueryButton.setIcon(icon6)

        self.verticalLayout.addWidget(self.ExecuteQueryButton)

        self.tableWidget = QTableWidget(self.frame)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.tableWidget)

        self.SaveChangesButton = QPushButton(self.frame)
        self.SaveChangesButton.setObjectName(u"SaveChangesButton")

        self.verticalLayout.addWidget(self.SaveChangesButton)

        self.ResutlText = QTextEdit(self.frame)
        self.ResutlText.setObjectName(u"ResutlText")
        self.ResutlText.setEnabled(True)
        self.ResutlText.setMinimumSize(QSize(0, 50))
        self.ResutlText.setMaximumSize(QSize(16777215, 100))
        self.ResutlText.setReadOnly(True)

        self.verticalLayout.addWidget(self.ResutlText)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 843, 31))
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menuBar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menu.addAction(self.DeveloperInfoAction)
        self.menu.addAction(self.ProgrammInfoAction)
        self.menu_2.addAction(self.SettingsAction)

        self.retranslateUi(MainWindow)

        self.TabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SQLite", None))
        self.DeveloperInfoAction.setText(QCoreApplication.translate("MainWindow", u"\u041e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0435", None))
#if QT_CONFIG(shortcut)
        self.DeveloperInfoAction.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+D", None))
#endif // QT_CONFIG(shortcut)
        self.ProgrammInfoAction.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
#if QT_CONFIG(shortcut)
        self.ProgrammInfoAction.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+I", None))
#endif // QT_CONFIG(shortcut)
        self.SettingsAction.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
#if QT_CONFIG(shortcut)
        self.SettingsAction.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+G", None))
#endif // QT_CONFIG(shortcut)
        self.WorkDirectoryLabel.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0431\u043e\u0447\u0430\u044f \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u044f:", None))
        self.SelectWorkDirectoryLabel.setText(QCoreApplication.translate("MainWindow", u"\u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0430\u0431\u043e\u0447\u0443\u044e \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u044e:", None))
#if QT_CONFIG(tooltip)
        self.SelectFolderButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0440\u0430\u0431\u043e\u0447\u0438\u044e \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u044e", None))
#endif // QT_CONFIG(tooltip)
        self.SelectFolderButton.setText("")
        self.LabelQuery.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0440\u043e\u0441:", None))
#if QT_CONFIG(tooltip)
        self.AddQueryButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443 \u0441 \u0437\u0430\u043f\u0440\u043e\u0441\u043e\u043c", None))
#endif // QT_CONFIG(tooltip)
        self.AddQueryButton.setText("")
#if QT_CONFIG(tooltip)
        self.DelQueryButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443 \u0441 \u0437\u0430\u043f\u0440\u043e\u0441\u043e\u043c", None))
#endif // QT_CONFIG(tooltip)
        self.DelQueryButton.setText("")
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0440\u043e\u0441 1", None))
#if QT_CONFIG(tooltip)
        self.ExecuteQueryButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u0437\u0430\u043f\u0440\u043e\u0441", None))
#endif // QT_CONFIG(tooltip)
        self.ExecuteQueryButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u043f\u0440\u043e\u0441", None))
#if QT_CONFIG(tooltip)
        self.SaveChangesButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.SaveChangesButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.ResutlText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:15px; font-weight:300; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:12px; font-weight:704;\"><br /></p></body></html>", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430", None))
    # retranslateUi

