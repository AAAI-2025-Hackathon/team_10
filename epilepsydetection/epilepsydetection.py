# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'epilepsydetection.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QListView, QMainWindow, QPushButton,
    QSizePolicy, QSlider, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from pyvistaqt.plotting import QtInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1559, 942)
        MainWindow.setMinimumSize(QSize(1300, 700))
        MainWindow.setStyleSheet(u"/* Global Styles */\n"
"QWidget {\n"
"    background-color: #FFFFFF; /* white background */\n"
"    font-family: \"Segoe UI\", sans-serif;\n"
"    font-size: 12pt;\n"
"    color: #333333; /* Dark gray text */\n"
"}\n"
"\n"
"/* QMainWindow styling */\n"
"QMainWindow {\n"
"    background-color: #FFFFFF; /* White background for the main window */\n"
"    border: none;\n"
"}\n"
"\n"
"/* TabWidget Styling */\n"
"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"    border-top: 1px solid #E0E0E0; /* Light gray border for the tab pane */\n"
"    background-color: #FFFFFF; /* White background for tabs area */\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #FFFFFF; /* White background for each tab */\n"
"    border: none;\n"
"    padding: 22px 40px; /* Padding for tab text */\n"
"    color: #555555; /* Dark gray text */\n"
"    font-size: 13pt;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #F8F9FA; /* Ligh"
                        "t gray background for the selected tab */\n"
"    color: #164194; /* Blue text for the active tab */\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #E8EAF6; /* Subtle blue hover effect */\n"
"    color: #164194;\n"
"}\n"
"\n"
"/* General Button Styling */\n"
"QPushButton {\n"
"    background-color: #FFFFFF; /* White button background */\n"
"    border: 1px solid #E0E0E0; /* Light gray border */\n"
"    border-radius: 6px; /* Rounded corners */\n"
"    padding: 6px 12px;\n"
"    color: #333333; /* Dark gray text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #E8EAF6; /* Subtle blue hover effect */\n"
"    border-color: #B0B0B0; /* Slightly darker border */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #DDE2F1; /* Slightly darker blue for pressed state */\n"
"}\n"
"\n"
"/* Header Styling */\n"
"QLabel#headerLabel {\n"
"    font-size: 14pt; /* Larger font size for headers */\n"
"    font-weight: bold;\n"
"    color: #333333; /* Dark gray "
                        "*/\n"
"}\n"
"\n"
"/* General Frame Styling */\n"
"QFrame {\n"
"    background-color: #FFFFFF; /* White background for cards or sections */\n"
"    border: 1px solid #E0E0E0; /* Light gray border */\n"
"    border-radius: 6px; /* Rounded corners */\n"
"    padding: 12px;\n"
"}\n"
"\n"
"\n"
"\n"
"/* Text Fields */\n"
"QLineEdit, QTextEdit {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QLineEdit:focus, QTextEdit:focus {\n"
"    border-color: #164194; /* Blue border when focused */\n"
"}\n"
"\n"
"/* Footer Styling */\n"
"QStatusBar {\n"
"    background-color: #FFFFFF;\n"
"    border-top: 1px solid #E0E0E0; /* Light gray top border */\n"
"    font-size: 10pt;\n"
"    color: #555555; /* Slightly lighter gray text */\n"
"}\n"
"\n"
"QGroupBox {\n"
"    background-color: #F9F9F9;\n"
"	padding: 5px;\n"
"    border-radius: 6px;\n"
"    font-size: 13pt;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
""
                        "	padding: 20px;\n"
"}\n"
"\n"
"QWebEngineView {\n"
"   border-radius: 6px;\n"
"}\n"
"\n"
"#tabWidget > QFrame {\n"
"	border: none;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1561, 921))
        self.tab_01_view = QWidget()
        self.tab_01_view.setObjectName(u"tab_01_view")
        self.horizontalLayout_1 = QHBoxLayout(self.tab_01_view)
        self.horizontalLayout_1.setSpacing(6)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.horizontalLayout_1.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.tab_01_view)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_5 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.uploadButton = QPushButton(self.widget_2)
        self.uploadButton.setObjectName(u"uploadButton")
        self.uploadButton.setCheckable(False)
        self.uploadButton.setFlat(False)

        self.horizontalLayout_4.addWidget(self.uploadButton)

        self.uploadMaskButton = QPushButton(self.widget_2)
        self.uploadMaskButton.setObjectName(u"uploadMaskButton")

        self.horizontalLayout_4.addWidget(self.uploadMaskButton)

        self.inferMaskButton = QPushButton(self.widget_2)
        self.inferMaskButton.setObjectName(u"inferMaskButton")

        self.horizontalLayout_4.addWidget(self.inferMaskButton)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget = QWidget(self.tab_01_view)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image_label = QLabel(self.widget)
        self.image_label.setObjectName(u"image_label")

        self.horizontalLayout.addWidget(self.image_label)

        self.three_D_plotter = QtInteractor(self.widget)
        self.three_D_plotter.setObjectName(u"three_D_plotter")
        self.three_D_plotter.setMinimumSize(QSize(25, 0))

        self.horizontalLayout.addWidget(self.three_D_plotter)

        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(320, 0))
        self.groupBox_3.setMaximumSize(QSize(320, 16777215))
        self.verticalLayoutWidget = QWidget(self.groupBox_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(19, 69, 281, 611))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.volumeListView = QListView(self.verticalLayoutWidget)
        self.volumeListView.setObjectName(u"volumeListView")
        self.volumeListView.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_2.addWidget(self.volumeListView)


        self.horizontalLayout.addWidget(self.groupBox_3)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)

        self.slice_slider = QSlider(self.tab_01_view)
        self.slice_slider.setObjectName(u"slice_slider")
        self.slice_slider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.slice_slider)


        self.horizontalLayout_1.addLayout(self.verticalLayout)

        self.tabWidget.addTab(self.tab_01_view, "")
        self.logoMN = QLabel(self.centralwidget)
        self.logoMN.setObjectName(u"logoMN")
        self.logoMN.setGeometry(QRect(10, 2, 181, 61))
        self.logoMN.setStyleSheet(u"QLabel {\n"
"margin: 0px;\n"
"padding: 0px;\n"
"padding-top: 4px;\n"
"border: none;\n"
"border-right: 1px solid #858585;\n"
"border-radius: 0px;\n"
"}")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(200, 0, 211, 61))
        self.label_9.setStyleSheet(u"QLabel {\n"
"margin: 0px;\n"
"padding: 0px;\n"
"padding-top: 6px;\n"
"padding-left: 6px;\n"
"border: none;\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.uploadButton.setText(QCoreApplication.translate("MainWindow", u"Load brain MRI", None))
        self.uploadMaskButton.setText(QCoreApplication.translate("MainWindow", u"Load mask", None))
        self.inferMaskButton.setText(QCoreApplication.translate("MainWindow", u"AI generate mask", None))
        self.image_label.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Volumes to show", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_01_view), QCoreApplication.translate("MainWindow", u"View", None))
        self.logoMN.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><img src=\"gui/resources/MN_logo.png\" height=\"44\"/></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt;\">Epilepsy detection</span></p></body></html>", None))
    # retranslateUi

