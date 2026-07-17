# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1746, 872)
        self.actionLoad_data = QAction(MainWindow)
        self.actionLoad_data.setObjectName(u"actionLoad_data")
        self.actionSave_data = QAction(MainWindow)
        self.actionSave_data.setObjectName(u"actionSave_data")
        self.actionL_BFGS_B = QAction(MainWindow)
        self.actionL_BFGS_B.setObjectName(u"actionL_BFGS_B")
        self.actionL_BFGS_B.setCheckable(True)
        self.actionL_BFGS_B.setChecked(True)
        self.actionPowell = QAction(MainWindow)
        self.actionPowell.setObjectName(u"actionPowell")
        self.actionPowell.setCheckable(True)
        self.actionNelder_Mead = QAction(MainWindow)
        self.actionNelder_Mead.setObjectName(u"actionNelder_Mead")
        self.actionNelder_Mead.setCheckable(True)
        self.actionSLSQP = QAction(MainWindow)
        self.actionSLSQP.setObjectName(u"actionSLSQP")
        self.actionSLSQP.setCheckable(True)
        self.actionTNC = QAction(MainWindow)
        self.actionTNC.setObjectName(u"actionTNC")
        self.actionTNC.setCheckable(True)
        self.actionMAX_ITER = QAction(MainWindow)
        self.actionMAX_ITER.setObjectName(u"actionMAX_ITER")
        self.actionLoad_data_2 = QAction(MainWindow)
        self.actionLoad_data_2.setObjectName(u"actionLoad_data_2")
        self.actionSave_data_2 = QAction(MainWindow)
        self.actionSave_data_2.setObjectName(u"actionSave_data_2")
        self.actionExport_to_ZondTEM1D = QAction(MainWindow)
        self.actionExport_to_ZondTEM1D.setObjectName(u"actionExport_to_ZondTEM1D")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.action_hankel_key_81_2009 = QAction(MainWindow)
        self.action_hankel_key_81_2009.setObjectName(u"action_hankel_key_81_2009")
        self.action_hankel_key_81_2009.setCheckable(True)
        self.action_hankel_key_101_2012 = QAction(MainWindow)
        self.action_hankel_key_101_2012.setObjectName(u"action_hankel_key_101_2012")
        self.action_hankel_key_101_2012.setCheckable(True)
        self.action_hankel_key_201_2012 = QAction(MainWindow)
        self.action_hankel_key_201_2012.setObjectName(u"action_hankel_key_201_2012")
        self.action_hankel_key_201_2012.setCheckable(True)
        self.action_hankel_key_241_2009 = QAction(MainWindow)
        self.action_hankel_key_241_2009.setObjectName(u"action_hankel_key_241_2009")
        self.action_hankel_key_241_2009.setCheckable(True)
        self.action_hankel_key_601_2009 = QAction(MainWindow)
        self.action_hankel_key_601_2009.setObjectName(u"action_hankel_key_601_2009")
        self.action_hankel_key_601_2009.setCheckable(True)
        self.action_hankel_grayver_50_2021 = QAction(MainWindow)
        self.action_hankel_grayver_50_2021.setObjectName(u"action_hankel_grayver_50_2021")
        self.action_hankel_grayver_50_2021.setCheckable(True)
        self.action_hankel_wer_101_2020a = QAction(MainWindow)
        self.action_hankel_wer_101_2020a.setObjectName(u"action_hankel_wer_101_2020a")
        self.action_hankel_wer_101_2020a.setCheckable(True)
        self.action_hankel_wer_101_2020b = QAction(MainWindow)
        self.action_hankel_wer_101_2020b.setObjectName(u"action_hankel_wer_101_2020b")
        self.action_hankel_wer_101_2020b.setCheckable(True)
        self.actionkey_81_2009 = QAction(MainWindow)
        self.actionkey_81_2009.setObjectName(u"actionkey_81_2009")
        self.actionkey_101_2012 = QAction(MainWindow)
        self.actionkey_101_2012.setObjectName(u"actionkey_101_2012")
        self.actionkey_201_2012 = QAction(MainWindow)
        self.actionkey_201_2012.setObjectName(u"actionkey_201_2012")
        self.action_hankel_wer_201_2018 = QAction(MainWindow)
        self.action_hankel_wer_201_2018.setObjectName(u"action_hankel_wer_201_2018")
        self.action_hankel_wer_201_2018.setCheckable(True)
        self.action_hankel_key_101_2009 = QAction(MainWindow)
        self.action_hankel_key_101_2009.setObjectName(u"action_hankel_key_101_2009")
        self.action_hankel_key_101_2009.setCheckable(True)
        self.action_hankel_key_201_2009 = QAction(MainWindow)
        self.action_hankel_key_201_2009.setObjectName(u"action_hankel_key_201_2009")
        self.action_hankel_key_201_2009.setCheckable(True)
        self.action_hankel_key_401_2009 = QAction(MainWindow)
        self.action_hankel_key_401_2009.setObjectName(u"action_hankel_key_401_2009")
        self.action_hankel_key_401_2009.setCheckable(True)
        self.action_hankel_key_51_2012 = QAction(MainWindow)
        self.action_hankel_key_51_2012.setObjectName(u"action_hankel_key_51_2012")
        self.action_hankel_key_51_2012.setCheckable(True)
        self.action_hankel_key_101_2013 = QAction(MainWindow)
        self.action_hankel_key_101_2013.setObjectName(u"action_hankel_key_101_2013")
        self.action_hankel_key_101_2013.setCheckable(True)
        self.action_hankel_key_201_2013 = QAction(MainWindow)
        self.action_hankel_key_201_2013.setObjectName(u"action_hankel_key_201_2013")
        self.action_hankel_key_201_2013.setCheckable(True)
        self.actionVCI_alpha = QAction(MainWindow)
        self.actionVCI_alpha.setObjectName(u"actionVCI_alpha")
        self.actionSrcpts = QAction(MainWindow)
        self.actionSrcpts.setObjectName(u"actionSrcpts")
        self.actionAuto_fitting_srcpts = QAction(MainWindow)
        self.actionAuto_fitting_srcpts.setObjectName(u"actionAuto_fitting_srcpts")
        self.actionTurn_off_0_01_ms = QAction(MainWindow)
        self.actionTurn_off_0_01_ms.setObjectName(u"actionTurn_off_0_01_ms")
        self.actionExport_results_to_text_dat = QAction(MainWindow)
        self.actionExport_results_to_text_dat.setObjectName(u"actionExport_results_to_text_dat")
        self.actionExport_results_by_horizontal_slice_to_text_dat = QAction(MainWindow)
        self.actionExport_results_by_horizontal_slice_to_text_dat.setObjectName(u"actionExport_results_by_horizontal_slice_to_text_dat")
        self.actionColorMap = QAction(MainWindow)
        self.actionColorMap.setObjectName(u"actionColorMap")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.btnLoad = QPushButton(self.centralwidget)
        self.btnLoad.setObjectName(u"btnLoad")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLoad.sizePolicy().hasHeightForWidth())
        self.btnLoad.setSizePolicy(sizePolicy)
        self.btnLoad.setMinimumSize(QSize(116, 0))
        self.btnLoad.setMaximumSize(QSize(116, 16777215))
        self.btnLoad.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon = QIcon(QIcon.fromTheme(u"document-open"))
        self.btnLoad.setIcon(icon)

        self.gridLayout_6.addWidget(self.btnLoad, 0, 1, 1, 1)

        self.btnSaveData = QPushButton(self.centralwidget)
        self.btnSaveData.setObjectName(u"btnSaveData")
        self.btnSaveData.setMinimumSize(QSize(116, 0))
        self.btnSaveData.setMaximumSize(QSize(116, 16777215))
        icon1 = QIcon(QIcon.fromTheme(u"document-save"))
        self.btnSaveData.setIcon(icon1)

        self.gridLayout_6.addWidget(self.btnSaveData, 1, 1, 1, 1)

        self.lblPath = QLabel(self.centralwidget)
        self.lblPath.setObjectName(u"lblPath")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lblPath.sizePolicy().hasHeightForWidth())
        self.lblPath.setSizePolicy(sizePolicy1)
        self.lblPath.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.lblPath.setFont(font)

        self.gridLayout_6.addWidget(self.lblPath, 0, 0, 2, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMaximumSize(QSize(150, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.label.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label)

        self.comboBoxSelectProfile = QComboBox(self.centralwidget)
        self.comboBoxSelectProfile.setObjectName(u"comboBoxSelectProfile")
        self.comboBoxSelectProfile.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_5.addWidget(self.comboBoxSelectProfile)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.checkBoxTablePicketsAdvanceColumnView = QCheckBox(self.centralwidget)
        self.checkBoxTablePicketsAdvanceColumnView.setObjectName(u"checkBoxTablePicketsAdvanceColumnView")

        self.verticalLayout_2.addWidget(self.checkBoxTablePicketsAdvanceColumnView)

        self.tablePickets = QTableWidget(self.centralwidget)
        self.tablePickets.setObjectName(u"tablePickets")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tablePickets.sizePolicy().hasHeightForWidth())
        self.tablePickets.setSizePolicy(sizePolicy3)
        self.tablePickets.setMinimumSize(QSize(100, 0))
        self.tablePickets.setMaximumSize(QSize(320, 16777215))
        self.tablePickets.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablePickets.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablePickets.setTextElideMode(Qt.TextElideMode.ElideRight)

        self.verticalLayout_2.addWidget(self.tablePickets)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBoxSelectInverseMethods = QComboBox(self.centralwidget)
        self.comboBoxSelectInverseMethods.addItem("")
        self.comboBoxSelectInverseMethods.addItem("")
        self.comboBoxSelectInverseMethods.addItem("")
        self.comboBoxSelectInverseMethods.addItem("")
        self.comboBoxSelectInverseMethods.addItem("")
        self.comboBoxSelectInverseMethods.setObjectName(u"comboBoxSelectInverseMethods")
        self.comboBoxSelectInverseMethods.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.comboBoxSelectInverseMethods, 11, 1, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.label_9, 5, 0, 1, 1)

        self.checkBoxIgnoreInvertedValue = QCheckBox(self.centralwidget)
        self.checkBoxIgnoreInvertedValue.setObjectName(u"checkBoxIgnoreInvertedValue")
        self.checkBoxIgnoreInvertedValue.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.checkBoxIgnoreInvertedValue, 7, 1, 1, 1)

        self.checkBoxUseRobustError = QCheckBox(self.centralwidget)
        self.checkBoxUseRobustError.setObjectName(u"checkBoxUseRobustError")
        self.checkBoxUseRobustError.setMaximumSize(QSize(85, 16777215))

        self.gridLayout_2.addWidget(self.checkBoxUseRobustError, 7, 0, 1, 1)

        self.btnDirectProblem = QPushButton(self.centralwidget)
        self.btnDirectProblem.setObjectName(u"btnDirectProblem")
        self.btnDirectProblem.setEnabled(True)
        self.btnDirectProblem.setMinimumSize(QSize(120, 0))
        self.btnDirectProblem.setMaximumSize(QSize(80, 16777215))
        self.btnDirectProblem.setBaseSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.btnDirectProblem, 8, 0, 1, 1)

        self.spinBoxMaxIteration = QSpinBox(self.centralwidget)
        self.spinBoxMaxIteration.setObjectName(u"spinBoxMaxIteration")
        self.spinBoxMaxIteration.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.spinBoxMaxIteration, 11, 2, 1, 1)

        self.btnPlotCrossSection = QPushButton(self.centralwidget)
        self.btnPlotCrossSection.setObjectName(u"btnPlotCrossSection")
        self.btnPlotCrossSection.setMinimumSize(QSize(120, 0))
        self.btnPlotCrossSection.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.btnPlotCrossSection, 13, 2, 1, 1)

        self.btnLoopHeightApply = QPushButton(self.centralwidget)
        self.btnLoopHeightApply.setObjectName(u"btnLoopHeightApply")

        self.gridLayout_2.addWidget(self.btnLoopHeightApply, 3, 2, 1, 1)

        self.btnDirectProblemMulti = QPushButton(self.centralwidget)
        self.btnDirectProblemMulti.setObjectName(u"btnDirectProblemMulti")
        self.btnDirectProblemMulti.setMinimumSize(QSize(120, 0))
        self.btnDirectProblemMulti.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.btnDirectProblemMulti, 8, 1, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setMaximumSize(QSize(80, 16777215))
        self.label_7.setFont(font1)

        self.gridLayout_2.addWidget(self.label_7, 11, 0, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.label_8, 4, 0, 1, 1)

        self.btnDirectProblemAll = QPushButton(self.centralwidget)
        self.btnDirectProblemAll.setObjectName(u"btnDirectProblemAll")
        self.btnDirectProblemAll.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.btnDirectProblemAll, 8, 2, 1, 1)

        self.checkBoxVCI = QCheckBox(self.centralwidget)
        self.checkBoxVCI.setObjectName(u"checkBoxVCI")
        self.checkBoxVCI.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.checkBoxVCI, 7, 2, 1, 1)

        self.btnInverseProblemAll = QPushButton(self.centralwidget)
        self.btnInverseProblemAll.setObjectName(u"btnInverseProblemAll")
        self.btnInverseProblemAll.setMinimumSize(QSize(120, 0))
        self.btnInverseProblemAll.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.btnInverseProblemAll, 12, 2, 1, 1)

        self.btnInverseProblem = QPushButton(self.centralwidget)
        self.btnInverseProblem.setObjectName(u"btnInverseProblem")
        self.btnInverseProblem.setMinimumSize(QSize(120, 0))
        self.btnInverseProblem.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.btnInverseProblem, 12, 0, 1, 1)

        self.brnSelectFilters = QPushButton(self.centralwidget)
        self.brnSelectFilters.setObjectName(u"brnSelectFilters")
        self.brnSelectFilters.setMinimumSize(QSize(120, 0))
        self.brnSelectFilters.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_2.addWidget(self.brnSelectFilters, 9, 0, 1, 1)

        self.spinBoxBeginTime = QSpinBox(self.centralwidget)
        self.spinBoxBeginTime.setObjectName(u"spinBoxBeginTime")
        self.spinBoxBeginTime.setMaximumSize(QSize(66, 16777215))

        self.gridLayout_2.addWidget(self.spinBoxBeginTime, 4, 1, 1, 1)

        self.btnInverseProblemMulti = QPushButton(self.centralwidget)
        self.btnInverseProblemMulti.setObjectName(u"btnInverseProblemMulti")
        self.btnInverseProblemMulti.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_2.addWidget(self.btnInverseProblemMulti, 12, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 35))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setBold(True)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 6, 0, 1, 3)

        self.lblFtArg = QLabel(self.centralwidget)
        self.lblFtArg.setObjectName(u"lblFtArg")

        self.gridLayout_2.addWidget(self.lblFtArg, 9, 2, 1, 1)

        self.spinBoxEndTime = QSpinBox(self.centralwidget)
        self.spinBoxEndTime.setObjectName(u"spinBoxEndTime")
        self.spinBoxEndTime.setMaximumSize(QSize(66, 16777215))

        self.gridLayout_2.addWidget(self.spinBoxEndTime, 5, 1, 1, 1)

        self.edLoopHeight = QLineEdit(self.centralwidget)
        self.edLoopHeight.setObjectName(u"edLoopHeight")
        self.edLoopHeight.setMaximumSize(QSize(66, 16777215))

        self.gridLayout_2.addWidget(self.edLoopHeight, 3, 1, 1, 1)

        self.lblHtArg = QLabel(self.centralwidget)
        self.lblHtArg.setObjectName(u"lblHtArg")

        self.gridLayout_2.addWidget(self.lblHtArg, 9, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)

        self.edLoopArea = QLineEdit(self.centralwidget)
        self.edLoopArea.setObjectName(u"edLoopArea")
        self.edLoopArea.setMaximumSize(QSize(66, 16777215))

        self.gridLayout_2.addWidget(self.edLoopArea, 2, 1, 1, 1)

        self.btnLoopAreaApply = QPushButton(self.centralwidget)
        self.btnLoopAreaApply.setObjectName(u"btnLoopAreaApply")

        self.gridLayout_2.addWidget(self.btnLoopAreaApply, 2, 2, 1, 1)

        self.btnBeginTimeApply = QPushButton(self.centralwidget)
        self.btnBeginTimeApply.setObjectName(u"btnBeginTimeApply")

        self.gridLayout_2.addWidget(self.btnBeginTimeApply, 4, 2, 1, 1)

        self.btnEndTimeApply = QPushButton(self.centralwidget)
        self.btnEndTimeApply.setObjectName(u"btnEndTimeApply")

        self.gridLayout_2.addWidget(self.btnEndTimeApply, 5, 2, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 1)
        self.gridLayout_2.setColumnMinimumWidth(2, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(320, 16777215))
        self.progressBar.setValue(0)

        self.verticalLayout_2.addWidget(self.progressBar)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tabProfile = QWidget()
        self.tabProfile.setObjectName(u"tabProfile")
        self.verticalLayout = QVBoxLayout(self.tabProfile)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutProfileButtons = QHBoxLayout()
        self.layoutProfileButtons.setObjectName(u"layoutProfileButtons")
        self.layoutProfileButtons.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.btnSmoothModelThickness = QPushButton(self.tabProfile)
        self.btnSmoothModelThickness.setObjectName(u"btnSmoothModelThickness")
        self.btnSmoothModelThickness.setMinimumSize(QSize(116, 0))
        self.btnSmoothModelThickness.setMaximumSize(QSize(116, 16777215))

        self.layoutProfileButtons.addWidget(self.btnSmoothModelThickness)

        self.btnSmoothModelRho = QPushButton(self.tabProfile)
        self.btnSmoothModelRho.setObjectName(u"btnSmoothModelRho")
        self.btnSmoothModelRho.setMinimumSize(QSize(116, 0))
        self.btnSmoothModelRho.setMaximumSize(QSize(116, 16777215))

        self.layoutProfileButtons.addWidget(self.btnSmoothModelRho)

        self.btnSmoothModelBoth = QPushButton(self.tabProfile)
        self.btnSmoothModelBoth.setObjectName(u"btnSmoothModelBoth")
        self.btnSmoothModelBoth.setMinimumSize(QSize(116, 0))
        self.btnSmoothModelBoth.setMaximumSize(QSize(116, 16777215))

        self.layoutProfileButtons.addWidget(self.btnSmoothModelBoth)

        self.btnCrossSectionSettings = QPushButton(self.tabProfile)
        self.btnCrossSectionSettings.setObjectName(u"btnCrossSectionSettings")

        self.layoutProfileButtons.addWidget(self.btnCrossSectionSettings)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutProfileButtons.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.layoutProfileButtons)

        self.layoutGraphics = QVBoxLayout()
        self.layoutGraphics.setObjectName(u"layoutGraphics")

        self.verticalLayout.addLayout(self.layoutGraphics)

        self.verticalLayout.setStretch(1, 1)
        self.tab_widget.addTab(self.tabProfile, "")
        self.tabMap = QWidget()
        self.tabMap.setObjectName(u"tabMap")
        self.verticalLayout_5 = QVBoxLayout(self.tabMap)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.layoutMapButtons = QHBoxLayout()
        self.layoutMapButtons.setObjectName(u"layoutMapButtons")
        self.btnExcludingProfiles = QPushButton(self.tabMap)
        self.btnExcludingProfiles.setObjectName(u"btnExcludingProfiles")

        self.layoutMapButtons.addWidget(self.btnExcludingProfiles)

        self.btnMapSectionSettings = QPushButton(self.tabMap)
        self.btnMapSectionSettings.setObjectName(u"btnMapSectionSettings")

        self.layoutMapButtons.addWidget(self.btnMapSectionSettings)

        self.btnPrepareData = QPushButton(self.tabMap)
        self.btnPrepareData.setObjectName(u"btnPrepareData")

        self.layoutMapButtons.addWidget(self.btnPrepareData)

        self.btnDrawMap = QPushButton(self.tabMap)
        self.btnDrawMap.setObjectName(u"btnDrawMap")

        self.layoutMapButtons.addWidget(self.btnDrawMap)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutMapButtons.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.layoutMapButtons)

        self.layoutMapMain = QHBoxLayout()
        self.layoutMapMain.setObjectName(u"layoutMapMain")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalSliderMap = QSlider(self.tabMap)
        self.verticalSliderMap.setObjectName(u"verticalSliderMap")
        self.verticalSliderMap.setOrientation(Qt.Orientation.Vertical)

        self.verticalLayout_4.addWidget(self.verticalSliderMap)

        self.lblCurrentDepth = QLabel(self.tabMap)
        self.lblCurrentDepth.setObjectName(u"lblCurrentDepth")

        self.verticalLayout_4.addWidget(self.lblCurrentDepth)


        self.layoutMapMain.addLayout(self.verticalLayout_4)

        self.layoutMapGraphics = QVBoxLayout()
        self.layoutMapGraphics.setObjectName(u"layoutMapGraphics")
        self.layoutMapGraphics.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.layoutMapMain.addLayout(self.layoutMapGraphics)

        self.layoutMapMain.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.layoutMapMain)

        self.tab_widget.addTab(self.tabMap, "")
        self.tabPseudoSection = QWidget()
        self.tabPseudoSection.setObjectName(u"tabPseudoSection")
        self.verticalLayout_6 = QVBoxLayout(self.tabPseudoSection)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.pushButton_2 = QPushButton(self.tabPseudoSection)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.tabPseudoSection)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.layoutPseudoSection = QVBoxLayout()
        self.layoutPseudoSection.setObjectName(u"layoutPseudoSection")

        self.verticalLayout_6.addLayout(self.layoutPseudoSection)

        self.verticalLayout_6.setStretch(1, 1)
        self.tab_widget.addTab(self.tabPseudoSection, "")

        self.horizontalLayout_4.addWidget(self.tab_widget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMaximumSize(QSize(16777215, 14))
        font3 = QFont()
        font3.setPointSize(9)
        self.label_3.setFont(font3)
        self.label_3.setScaledContents(False)

        self.verticalLayout_3.addWidget(self.label_3)

        self.btnCreateVCILayers = QPushButton(self.centralwidget)
        self.btnCreateVCILayers.setObjectName(u"btnCreateVCILayers")

        self.verticalLayout_3.addWidget(self.btnCreateVCILayers)

        self.tableModel = QTableWidget(self.centralwidget)
        self.tableModel.setObjectName(u"tableModel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tableModel.sizePolicy().hasHeightForWidth())
        self.tableModel.setSizePolicy(sizePolicy4)
        self.tableModel.setMinimumSize(QSize(0, 100))

        self.verticalLayout_3.addWidget(self.tableModel)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.btnAddLayer = QPushButton(self.frame_2)
        self.btnAddLayer.setObjectName(u"btnAddLayer")
        self.btnAddLayer.setMinimumSize(QSize(116, 0))
        self.btnAddLayer.setMaximumSize(QSize(116, 16777215))
        icon2 = QIcon(QIcon.fromTheme(u"list-add"))
        self.btnAddLayer.setIcon(icon2)

        self.gridLayout.addWidget(self.btnAddLayer, 0, 0, 1, 1)

        self.btnDeleteLayer = QPushButton(self.frame_2)
        self.btnDeleteLayer.setObjectName(u"btnDeleteLayer")
        self.btnDeleteLayer.setMinimumSize(QSize(116, 0))
        self.btnDeleteLayer.setMaximumSize(QSize(116, 16777215))
        icon3 = QIcon(QIcon.fromTheme(u"list-remove"))
        self.btnDeleteLayer.setIcon(icon3)

        self.gridLayout.addWidget(self.btnDeleteLayer, 0, 1, 1, 1)

        self.btnCopyModel = QPushButton(self.frame_2)
        self.btnCopyModel.setObjectName(u"btnCopyModel")
        self.btnCopyModel.setMinimumSize(QSize(116, 0))
        self.btnCopyModel.setMaximumSize(QSize(116, 16777215))
        icon4 = QIcon(QIcon.fromTheme(u"edit-copy"))
        self.btnCopyModel.setIcon(icon4)

        self.gridLayout.addWidget(self.btnCopyModel, 1, 0, 1, 1)

        self.btnCopyModelBorders = QPushButton(self.frame_2)
        self.btnCopyModelBorders.setObjectName(u"btnCopyModelBorders")
        self.btnCopyModelBorders.setMinimumSize(QSize(116, 0))
        self.btnCopyModelBorders.setMaximumSize(QSize(116, 16777215))

        self.gridLayout.addWidget(self.btnCopyModelBorders, 2, 0, 1, 1)

        self.btnPasteModel = QPushButton(self.frame_2)
        self.btnPasteModel.setObjectName(u"btnPasteModel")
        self.btnPasteModel.setMinimumSize(QSize(116, 0))
        self.btnPasteModel.setMaximumSize(QSize(116, 16777215))
        icon5 = QIcon(QIcon.fromTheme(u"edit-paste"))
        self.btnPasteModel.setIcon(icon5)

        self.gridLayout.addWidget(self.btnPasteModel, 1, 1, 1, 1)

        self.btnPasteModelForAll = QPushButton(self.frame_2)
        self.btnPasteModelForAll.setObjectName(u"btnPasteModelForAll")
        self.btnPasteModelForAll.setMinimumSize(QSize(116, 0))
        self.btnPasteModelForAll.setMaximumSize(QSize(116, 16777215))

        self.gridLayout.addWidget(self.btnPasteModelForAll, 2, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMaximumSize(QSize(16777215, 14))
        self.label_4.setFont(font3)
        self.label_4.setScaledContents(False)

        self.verticalLayout_3.addWidget(self.label_4)

        self.tableModelBorders = QTableWidget(self.centralwidget)
        self.tableModelBorders.setObjectName(u"tableModelBorders")
        self.tableModelBorders.setMinimumSize(QSize(0, 100))

        self.verticalLayout_3.addWidget(self.tableModelBorders)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 4)
        self.horizontalLayout_4.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1746, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuFile.addAction(self.actionLoad_data_2)
        self.menuFile.addAction(self.actionSave_data_2)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_to_ZondTEM1D)
        self.menuFile.addAction(self.actionExport_results_to_text_dat)
        self.menuFile.addAction(self.actionExport_results_by_horizontal_slice_to_text_dat)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionVCI_alpha)
        self.menuOptions.addAction(self.actionSrcpts)
        self.menuOptions.addAction(self.actionAuto_fitting_srcpts)
        self.menuOptions.addAction(self.actionTurn_off_0_01_ms)
        self.menuOptions.addAction(self.actionColorMap)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionLoad_data.setText(QCoreApplication.translate("MainWindow", u"Load data", None))
        self.actionSave_data.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
        self.actionL_BFGS_B.setText(QCoreApplication.translate("MainWindow", u"L-BFGS-B", None))
        self.actionPowell.setText(QCoreApplication.translate("MainWindow", u"Powell", None))
        self.actionNelder_Mead.setText(QCoreApplication.translate("MainWindow", u"Nelder Mead", None))
        self.actionSLSQP.setText(QCoreApplication.translate("MainWindow", u"SLSQP", None))
        self.actionTNC.setText(QCoreApplication.translate("MainWindow", u"TNC", None))
        self.actionMAX_ITER.setText(QCoreApplication.translate("MainWindow", u"MAX_ITER: ", None))
        self.actionLoad_data_2.setText(QCoreApplication.translate("MainWindow", u"Load data", None))
        self.actionSave_data_2.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
        self.actionExport_to_ZondTEM1D.setText(QCoreApplication.translate("MainWindow", u"Export to ZondTEM1D", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.action_hankel_key_81_2009.setText(QCoreApplication.translate("MainWindow", u"key_81_2009", None))
        self.action_hankel_key_101_2012.setText(QCoreApplication.translate("MainWindow", u"key_101_2012", None))
        self.action_hankel_key_201_2012.setText(QCoreApplication.translate("MainWindow", u"key_201_2012", None))
        self.action_hankel_key_241_2009.setText(QCoreApplication.translate("MainWindow", u"key_241_2009", None))
        self.action_hankel_key_601_2009.setText(QCoreApplication.translate("MainWindow", u"key_601_2009", None))
        self.action_hankel_grayver_50_2021.setText(QCoreApplication.translate("MainWindow", u"grayver_50_2021", None))
        self.action_hankel_wer_101_2020a.setText(QCoreApplication.translate("MainWindow", u"wer_101_2020a", None))
        self.action_hankel_wer_101_2020b.setText(QCoreApplication.translate("MainWindow", u"wer_101_2020b", None))
        self.actionkey_81_2009.setText(QCoreApplication.translate("MainWindow", u"key_81_2009", None))
        self.actionkey_101_2012.setText(QCoreApplication.translate("MainWindow", u"key_101_2012", None))
        self.actionkey_201_2012.setText(QCoreApplication.translate("MainWindow", u"key_201_2012", None))
        self.action_hankel_wer_201_2018.setText(QCoreApplication.translate("MainWindow", u"wer_201_2018", None))
        self.action_hankel_key_101_2009.setText(QCoreApplication.translate("MainWindow", u"key_101_2009", None))
        self.action_hankel_key_201_2009.setText(QCoreApplication.translate("MainWindow", u"key_201_2009", None))
        self.action_hankel_key_401_2009.setText(QCoreApplication.translate("MainWindow", u"key_401_2009", None))
        self.action_hankel_key_51_2012.setText(QCoreApplication.translate("MainWindow", u"key_51_2012", None))
        self.action_hankel_key_101_2013.setText(QCoreApplication.translate("MainWindow", u"key_101_2012", None))
        self.action_hankel_key_201_2013.setText(QCoreApplication.translate("MainWindow", u"key_201_2012", None))
        self.actionVCI_alpha.setText(QCoreApplication.translate("MainWindow", u"VCI alpha: 0.1", None))
        self.actionSrcpts.setText(QCoreApplication.translate("MainWindow", u"srcpts: 7", None))
        self.actionAuto_fitting_srcpts.setText(QCoreApplication.translate("MainWindow", u"auto fitting srcpts", None))
        self.actionTurn_off_0_01_ms.setText(QCoreApplication.translate("MainWindow", u"turn_off: 0.01 ms", None))
        self.actionExport_results_to_text_dat.setText(QCoreApplication.translate("MainWindow", u"Export results by PR to text (*.dat)", None))
        self.actionExport_results_by_horizontal_slice_to_text_dat.setText(QCoreApplication.translate("MainWindow", u"Export results by horizontal slice to text (*.dat)", None))
        self.actionColorMap.setText(QCoreApplication.translate("MainWindow", u"colormap", None))
        self.btnLoad.setText(QCoreApplication.translate("MainWindow", u"Load data", None))
        self.btnSaveData.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
        self.lblPath.setText(QCoreApplication.translate("MainWindow", u"path", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select profile", None))
        self.checkBoxTablePicketsAdvanceColumnView.setText(QCoreApplication.translate("MainWindow", u"Advance column view", None))
        self.comboBoxSelectInverseMethods.setItemText(0, QCoreApplication.translate("MainWindow", u"L-BFGS-B", None))
        self.comboBoxSelectInverseMethods.setItemText(1, QCoreApplication.translate("MainWindow", u"Powell", None))
        self.comboBoxSelectInverseMethods.setItemText(2, QCoreApplication.translate("MainWindow", u"Nelder-Mead", None))
        self.comboBoxSelectInverseMethods.setItemText(3, QCoreApplication.translate("MainWindow", u"TNC", None))
        self.comboBoxSelectInverseMethods.setItemText(4, QCoreApplication.translate("MainWindow", u"SLSQP", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"End time index for proccess", None))
        self.checkBoxIgnoreInvertedValue.setText(QCoreApplication.translate("MainWindow", u"Ignore Neg Value", None))
        self.checkBoxUseRobustError.setText(QCoreApplication.translate("MainWindow", u"Robust err", None))
        self.btnDirectProblem.setText(QCoreApplication.translate("MainWindow", u"Direct", None))
        self.btnPlotCrossSection.setText(QCoreApplication.translate("MainWindow", u"Plot Cross-Section", None))
        self.btnLoopHeightApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.btnDirectProblemMulti.setText(QCoreApplication.translate("MainWindow", u"Multi Direct", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Inverse method:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Loop height, m", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Begin time index for proccess", None))
        self.btnDirectProblemAll.setText(QCoreApplication.translate("MainWindow", u"All Direct problem", None))
        self.checkBoxVCI.setText(QCoreApplication.translate("MainWindow", u"VCI", None))
        self.btnInverseProblemAll.setText(QCoreApplication.translate("MainWindow", u"All Inverse problem", None))
        self.btnInverseProblem.setText(QCoreApplication.translate("MainWindow", u"Inverse", None))
        self.brnSelectFilters.setText(QCoreApplication.translate("MainWindow", u"Filters", None))
        self.btnInverseProblemMulti.setText(QCoreApplication.translate("MainWindow", u"Multi Inverse", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Proccess", None))
        self.lblFtArg.setText(QCoreApplication.translate("MainWindow", u"Fourier:", None))
        self.edLoopHeight.setText(QCoreApplication.translate("MainWindow", u"40", None))
        self.lblHtArg.setText(QCoreApplication.translate("MainWindow", u"Hankel:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Loop area, m2", None))
        self.edLoopArea.setText(QCoreApplication.translate("MainWindow", u"2500", None))
        self.btnLoopAreaApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.btnBeginTimeApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.btnEndTimeApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.btnSmoothModelThickness.setText(QCoreApplication.translate("MainWindow", u"Smooth h", None))
        self.btnSmoothModelRho.setText(QCoreApplication.translate("MainWindow", u"Smooth rho", None))
        self.btnSmoothModelBoth.setText(QCoreApplication.translate("MainWindow", u"Smooth both", None))
        self.btnCrossSectionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tabProfile), QCoreApplication.translate("MainWindow", u"Cross-section", None))
        self.btnExcludingProfiles.setText(QCoreApplication.translate("MainWindow", u"Excluding PR", None))
        self.btnMapSectionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btnPrepareData.setText(QCoreApplication.translate("MainWindow", u"Prepare data", None))
        self.btnDrawMap.setText(QCoreApplication.translate("MainWindow", u"Draw", None))
        self.lblCurrentDepth.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tabMap), QCoreApplication.translate("MainWindow", u"Map", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tabPseudoSection), QCoreApplication.translate("MainWindow", u"Pseudo-section", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.btnCreateVCILayers.setText(QCoreApplication.translate("MainWindow", u"Create VCI layers", None))
        self.btnAddLayer.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btnDeleteLayer.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.btnCopyModel.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.btnCopyModelBorders.setText(QCoreApplication.translate("MainWindow", u"Copy Borders", None))
        self.btnPasteModel.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        self.btnPasteModelForAll.setText(QCoreApplication.translate("MainWindow", u"Paste to All", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Model Borders", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

