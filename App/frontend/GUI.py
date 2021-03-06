from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from engine import *
from frontend.Spiral_Painter import Spiral_Painter
from frontend.Camera_Widget import Camera_Widget
from frontend.Calibration_Widget import Calibration_Widget

PAGE_COUNT = STATE_COUNT

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")

        self.fullscreen_dimensions = MainWindow.geometry()
        print(self.fullscreen_dimensions)

        VERTICAL_BORDERSIZE = self.fullscreen_dimensions.height() // 100
        HORIZONTAL_BORDERSIZE = self.fullscreen_dimensions.width() // 100

        font_db = QFontDatabase()
        font_db.addApplicationFont("./assets/fonts/Montserrat-SemiBold.ttf")
        font_db.addApplicationFont("./assets/fonts/Montserrat-Regular.ttf")
        #font_db.addApplicationFont("./assets/fonts/Montserrat-Medium.ttf")
        #font_db.addApplicationFont("./assets/fonts/Montserrat-Black.ttf")
        #font_db.addApplicationFont("./assets/fonts/Montserrat-Bold.ttf")


        self.bg = QWidget(self.MainWindow)
        self.bg.setGeometry(self.MainWindow.geometry())
        self.bg.setObjectName("bg")

        self.frame = QFrame(self.MainWindow)
        self.frame.setGeometry(QRect(HORIZONTAL_BORDERSIZE, VERTICAL_BORDERSIZE,
                                     self.fullscreen_dimensions.width() - 2 * HORIZONTAL_BORDERSIZE,
                                     self.fullscreen_dimensions.height() - 2 * VERTICAL_BORDERSIZE))
        self.frame.setObjectName("frame")

        self.version = QLineEdit(self.frame)
        self.version.move(self.frame.geometry().left(), self.frame.geometry().height() - self.version.height())
        self.version.setObjectName("version")
        self.version.setText("Water Moccassin v1.0b")
        self.version.setReadOnly(True)

        self.stacked_widget = QStackedWidget(self.frame)
        self.stacked_widget.setObjectName("stacked_widget")
        self.stacked_widget.resize(self.frame.size())
        
        self.calibration_screen = QWidget()
        self.calibration_screen.resize(self.frame.size())
        self.setup_calibration_screen()

        self.title_screen = QWidget()
        self.title_screen.resize(self.frame.size())
        self.setup_title_screen()

        self.spiral_pairing_screen = QWidget()
        self.spiral_pairing_screen.resize(self.frame.size())
        self.setup_spiral_pairing_screen()

        self.spiral_test_screen = QWidget()
        self.spiral_test_screen.resize(self.frame.size())
        self.setup_spiral_test_screen()

        self.spiral_complete_test_screen = QWidget()
        self.spiral_complete_test_screen.setGeometry(self.frame.geometry())
        self.setup_spiral_test_complete_screen(self.spiral_complete_test_screen)

        self.tremor_pairing_screen = QWidget()
        self.tremor_pairing_screen.setGeometry(self.frame.geometry())
        self.setup_tremor_pairing_screen()

        self.tremor_test_start_screen = QWidget()
        self.tremor_test_start_screen.setGeometry(self.frame.geometry())
        self.setup_tremor_test_start_screen()

        self.tremor_test_screen = QWidget()
        self.tremor_test_screen.setGeometry(self.frame.geometry())
        self.setup_tremor_test_screen()

        self.tremor_complete_test_screen = QWidget()
        self.tremor_complete_test_screen.setGeometry(self.frame.geometry())
        self.setup_tremor_test_complete_screen(self.tremor_complete_test_screen)

        self.questionnaire_screen = QWidget()
        self.questionnaire_screen.setGeometry(self.frame.geometry())
        self.setup_questionnaire_screen()

        self.result_screen = QWidget()
        self.result_screen.setGeometry(self.frame.geometry())
        self.setup_result_screen()

        self.complete_screen = QWidget()
        self.complete_screen.setGeometry(self.frame.geometry())
        self.setup_complete_screen()

        self.stacked_widget.addWidget(self.title_screen)
        self.stacked_widget.addWidget(self.spiral_pairing_screen)
        self.stacked_widget.addWidget(self.calibration_screen)
        self.stacked_widget.addWidget(self.spiral_test_screen)
        self.stacked_widget.addWidget(self.spiral_complete_test_screen)
        self.stacked_widget.addWidget(self.tremor_pairing_screen)
        self.stacked_widget.addWidget(self.tremor_test_start_screen)
        self.stacked_widget.addWidget(self.tremor_test_screen)
        self.stacked_widget.addWidget(self.tremor_complete_test_screen)
        self.stacked_widget.addWidget(self.questionnaire_screen)
        self.stacked_widget.addWidget(self.result_screen)
        self.stacked_widget.addWidget(self.complete_screen)

        self.debug_next_button = QPushButton(self.frame)
        self.debug_next_button.move(self.fullscreen_dimensions.width() - self.debug_next_button.width() - HORIZONTAL_BORDERSIZE,
                        VERTICAL_BORDERSIZE)
        self.debug_next_button.setText("Next")

        self.exit_button = QPushButton(self.frame)
        self.exit_button.setGeometry(QRect(self.frame.geometry().right() - self.exit_button.geometry().width(),
                                           self.frame.geometry().bottom() - self.exit_button.geometry().height(),
                                           self.exit_button.geometry().width(), self.exit_button.geometry().height()))
        print(self.exit_button.geometry())
        self.exit_button.setText("Exit")

        print(self.stacked_widget.currentIndex())
        
    def setup_calibration_screen(self):
        calibration_widget = QWidget(self.calibration_screen)
        calibration_widget.resize(self.calibration_screen.size())
        calibration_widget.setObjectName("calibration_widget")
        
        calibration_layout = QVBoxLayout(calibration_widget)
        
        calibration_title_text = QLabel(calibration_widget)
        calibration_title_text.setText("Calibration")
        calibration_title_text.setObjectName("calibration_title_text")
        calibration_layout.addWidget(calibration_title_text)
        
        calibration_subtitle_text = QLabel(calibration_widget)
        calibration_subtitle_text.setText("Position the projector's projection in the middle of the camera.")
        calibration_subtitle_text.setObjectName("calibration_subtitle_text")
        calibration_layout.addWidget(calibration_subtitle_text)

        self.calibration_canvas = QWidget(calibration_widget)
        self.calibration_canvas.setObjectName("calibration_canvas")
        calibration_layout.addWidget(self.calibration_canvas)
        
        calibration_canvas_layout = QGridLayout()
        calibration_canvas_layout.setColumnMinimumWidth(0, 10)
        calibration_canvas_layout.setColumnMinimumWidth(2, 10)
        self.calibration_canvas.setLayout(calibration_canvas_layout)
        
        self.camera_widget = Camera_Widget(calibration_widget)
        self.camera_widget.setObjectName("camera_widget")

        self.calibration_aid_widget = Calibration_Widget(calibration_widget)
        self.calibration_aid_widget.setObjectName("calibration_aid_widget")

        self.calibration_reset_button = QPushButton(calibration_widget)
        self.calibration_reset_button.setObjectName("calibration_reset_button")
        self.calibration_reset_button.setText("Reset Calibration")
        calibration_canvas_layout.addWidget(self.calibration_reset_button, 2, 1, 1, 3)

        self.calibration_confirm_button = QPushButton(calibration_widget)
        self.calibration_confirm_button.setObjectName("calibration_confirm_button")
        self.calibration_confirm_button.setText("Confirm Calibration")
        calibration_canvas_layout.addWidget(self.calibration_confirm_button, 3, 1, 1, 3)
        
        '''
        self.camera_widget.setMinimumSize(min(self.camera_widget.geometry().width(), self.calibration_aid_widget.geometry().width()),
                                        min(self.camera_widget.geometry().height(), self.calibration_aid_widget.geometry().height()))
        self.calibration_aid_widget.setMinimumSize(min(self.camera_widget.geometry().width(), self.calibration_aid_widget.geometry().width()),
                                           min(self.camera_widget.geometry().height(), self.calibration_aid_widget.geometry().height()))
        '''
        
        # calibration_layout.addWidget(self.camera_widget)
        calibration_canvas_layout.addWidget(self.camera_widget, 1, 1)
        calibration_canvas_layout.addWidget(self.calibration_aid_widget, 1, 3)

    def setup_title_screen(self):
        title_widget = QWidget(self.title_screen)
        # title_widget.setGeometry(QRect(self.frame.geometry().width() // 3, self.frame.geometry().height() * 0.1, self.frame.geometry().width() // 3, self.frame.geometry().height() * 0.8))
        title_widget.setObjectName("title_layout_widget")
        title_widget.resize(self.frame.size())

        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("./assets/images/logo.png")
        logo = QLabel(title_widget)
        logo.setObjectName("logo")
        logo.setPixmap(pixmap)
        title_layout.addWidget(logo)

        self.start_button = QPushButton(title_widget)
        self.start_button.setObjectName("start_button")
        self.start_button.setText("Begin")
        title_layout.addWidget(self.start_button)


    def setup_spiral_pairing_screen(self):
        spiral_pairing_layout_widget = QWidget(self.spiral_pairing_screen)
        spiral_pairing_layout_widget.setGeometry(QRect(self.frame.geometry().width() // 3, self.frame.geometry().height() // 4,
                                        self.frame.geometry().width() // 3, self.frame.geometry().height() // 2))

        spiral_pairing_layout = QVBoxLayout(spiral_pairing_layout_widget)

        pixmap = QPixmap("./assets/images/pair1.png")
        spiral_pairing_image = QLabel(spiral_pairing_layout_widget)
        spiral_pairing_image.setObjectName("pairing_image")
        spiral_pairing_image.setGeometry(spiral_pairing_layout_widget.geometry())
        spiral_pairing_image.setPixmap(pixmap.scaled(spiral_pairing_image.width(), spiral_pairing_image.height(), Qt.KeepAspectRatio))
        spiral_pairing_layout.addWidget(spiral_pairing_image)

        spiral_pairing_text = QLineEdit(spiral_pairing_layout_widget)
        spiral_pairing_text.setObjectName("pairing_text")
        spiral_pairing_text.setText("Pairing with Device")
        spiral_pairing_text.setReadOnly(True)
        spiral_pairing_layout.addWidget(spiral_pairing_text)

        self.spiral_pairing_start_button = QPushButton(spiral_pairing_layout_widget)
        self.spiral_pairing_start_button.setObjectName("pairing_start_button")
        self.spiral_pairing_start_button.setText("START PAIRING")
        spiral_pairing_layout.addWidget(self.spiral_pairing_start_button)

        self.spiral_pairing_failed_button = QPushButton(spiral_pairing_layout_widget)
        self.spiral_pairing_failed_button.setObjectName("pairing_failed_button")
        self.spiral_pairing_failed_button.setText("FAILED, PRESS TO TRY AGAIN")
        spiral_pairing_layout.addWidget(self.spiral_pairing_failed_button)

        self.spiral_pairing_continue_button = QPushButton(spiral_pairing_layout_widget)
        self.spiral_pairing_continue_button.setObjectName("pairing_continue_button")
        self.spiral_pairing_continue_button.setText("CONTINUE")
        spiral_pairing_layout.addWidget(self.spiral_pairing_continue_button)


    def setup_spiral_test_screen(self):
        spiral_test_layout_widget = QWidget(self.spiral_test_screen)
        spiral_test_layout_widget.resize(self.spiral_test_screen.size())
    
        spiral_test_title = QLineEdit()
        spiral_test_title.setObjectName("spiral_test_title")
        spiral_test_title.setText("Spiral Drawing Test")
        spiral_test_title.setReadOnly(True)

        spiral_test_text = QLineEdit()
        spiral_test_text.setObjectName("spiral_test_text")
        spiral_test_text.setText("Use the IR Pen to trace the spiral in the white area. Press \"Next\" when finished.")
        spiral_test_text.setReadOnly(True)
        
        spiral_test_text_layout = QVBoxLayout()
        spiral_test_text_layout.addWidget(spiral_test_title)
        spiral_test_text_layout.addWidget(spiral_test_text)
        
        self.spiral_test_reset_button = QPushButton()
        self.spiral_test_reset_button.setText("Reset Drawing")
        
        self.spiral_test_next_button = QPushButton()
        self.spiral_test_next_button.setText("Next")
        
        spiral_test_button_layout = QVBoxLayout()
        spiral_test_button_layout.addWidget(self.spiral_test_reset_button)
        spiral_test_button_layout.addWidget(self.spiral_test_next_button)
        
        spiral_test_header_layout = QHBoxLayout()
        spiral_test_header_layout.addLayout(spiral_test_text_layout)
        spiral_test_header_layout.addLayout(spiral_test_button_layout)

        self.spiral_painter = Spiral_Painter()
        self.spiral_painter.setObjectName("spiral_painter")
        
        spiral_test_layout = QVBoxLayout()
        spiral_test_layout.addLayout(spiral_test_header_layout)
        spiral_test_layout.addWidget(self.spiral_painter)
        
        spiral_test_layout_widget.setLayout(spiral_test_layout)

    def setup_tremor_pairing_screen(self):
        tremor_pairing_layout_widget = QWidget(self.tremor_pairing_screen)
        tremor_pairing_layout_widget.setGeometry(
            QRect(self.frame.geometry().width() // 3, self.frame.geometry().height() // 4,
                  self.frame.geometry().width() // 3, self.frame.geometry().height() // 2))

        tremor_pairing_layout = QVBoxLayout(tremor_pairing_layout_widget)

        pixmap = QPixmap("./assets/images/pair1.png")
        tremor_pairing_image = QLabel(tremor_pairing_layout_widget)
        tremor_pairing_image.setObjectName("pairing_image")
        tremor_pairing_image.setGeometry(tremor_pairing_layout_widget.geometry())
        tremor_pairing_image.setPixmap(
            pixmap.scaled(tremor_pairing_image.width(), tremor_pairing_image.height(), Qt.KeepAspectRatio))
        tremor_pairing_layout.addWidget(tremor_pairing_image)

        tremor_pairing_text = QLineEdit(tremor_pairing_layout_widget)
        tremor_pairing_text.setObjectName("pairing_text")
        tremor_pairing_text.setText("Pairing with Device")
        tremor_pairing_text.setReadOnly(True)
        tremor_pairing_layout.addWidget(tremor_pairing_text)

        self.tremor_pairing_start_button = QPushButton(tremor_pairing_layout_widget)
        self.tremor_pairing_start_button.setObjectName("pairing_start_button")
        self.tremor_pairing_start_button.setText("START PAIRING")
        tremor_pairing_layout.addWidget(self.tremor_pairing_start_button)

        self.tremor_pairing_failed_button = QPushButton(tremor_pairing_layout_widget)
        self.tremor_pairing_failed_button.setObjectName("pairing_failed_button")
        self.tremor_pairing_failed_button.setText("FAILED, PRESS TO TRY AGAIN")
        tremor_pairing_layout.addWidget(self.tremor_pairing_failed_button)

        self.tremor_pairing_continue_button = QPushButton(tremor_pairing_layout_widget)
        self.tremor_pairing_continue_button.setObjectName("pairing_continue_button")
        self.tremor_pairing_continue_button.setText("CONTINUE")
        tremor_pairing_layout.addWidget(self.tremor_pairing_continue_button)


    def setup_tremor_test_start_screen(self):
        tremor_test_start_layout_widget = QWidget(self.tremor_test_start_screen)
        tremor_test_start_layout_widget.setGeometry(self.frame.geometry())

        tremor_test_start_layout = QVBoxLayout(tremor_test_start_layout_widget)

        tremor_test_start_title = QLineEdit(tremor_test_start_layout_widget)
        tremor_test_start_title.setObjectName("tremor_test_start_title")
        tremor_test_start_title.setText("Tremor Test")
        tremor_test_start_title.setReadOnly(True)
        tremor_test_start_layout.addWidget(tremor_test_start_title)

        tremor_test_start_text = QLineEdit(tremor_test_start_layout_widget)
        tremor_test_start_text.setObjectName("tremor_test_start_text")
        tremor_test_start_text.setText("Wear the glove and press start to begin the tremor test.")
        tremor_test_start_text.setReadOnly(True)
        tremor_test_start_layout.addWidget(tremor_test_start_text)

        self.tremor_test_start_button = QPushButton(tremor_test_start_layout_widget)
        self.tremor_test_start_button.setObjectName("tremor_test_start_button")
        self.tremor_test_start_button.setText("Start")
        tremor_test_start_layout.addWidget(self.tremor_test_start_button)

    def setup_tremor_test_screen(self):
        tremor_test_layout_widget = QWidget(self.tremor_test_screen)
        tremor_test_layout_widget.setGeometry(self.frame.geometry())

        tremor_test_layout = QVBoxLayout(tremor_test_layout_widget)

        self.tremor_time_text = QLineEdit(tremor_test_layout_widget)
        self.tremor_time_text.setObjectName("tremor_time_text")
        self.tremor_time_text.setReadOnly(True)
        tremor_test_layout.addWidget(self.tremor_time_text)


    def setup_spiral_test_complete_screen(self, screen_widget):
        complete_test_layout_widget = QWidget(screen_widget)
        complete_test_layout_widget.setGeometry(self.frame.geometry())

        complete_test_layout = QVBoxLayout(complete_test_layout_widget)

        complete_test_title = QLineEdit(complete_test_layout_widget)
        complete_test_title.setObjectName("complete_test_title")
        complete_test_title.setText("Test Complete")
        complete_test_title.setReadOnly(True)
        complete_test_layout.addWidget(complete_test_title)

        complete_test_text = QLineEdit(complete_test_layout_widget)
        complete_test_text.setObjectName("complete_test_text")
        complete_test_text.setText("Please click \"Continue\" to proceed or \"Save and Exit\" to save your progress and quit this session.")
        complete_test_text.setReadOnly(True)
        complete_test_layout.addWidget(complete_test_text)

        complete_test_button_layout_widget = QWidget()
        complete_test_button_layout = QHBoxLayout(complete_test_button_layout_widget)

        self.spiral_next_button = QPushButton(complete_test_button_layout_widget)
        self.spiral_next_button.setObjectName("spiral_next_button")
        self.spiral_next_button.setText("CONTINUE")
        complete_test_button_layout.addWidget(self.spiral_next_button)

        self.spiral_save_exit_button = QPushButton(complete_test_button_layout_widget)
        self.spiral_save_exit_button.setObjectName("save_exit_button")
        self.spiral_save_exit_button.setText("SAVE AND EXIT")
        complete_test_button_layout.addWidget(self.spiral_save_exit_button)

        complete_test_layout.addWidget(complete_test_button_layout_widget)

    def setup_tremor_test_complete_screen(self, screen_widget):
        complete_test_layout_widget = QWidget(screen_widget)
        complete_test_layout_widget.setGeometry(self.frame.geometry())

        complete_test_layout = QVBoxLayout(complete_test_layout_widget)

        complete_test_title = QLineEdit(complete_test_layout_widget)
        complete_test_title.setObjectName("complete_test_title")
        complete_test_title.setText("Test Complete")
        complete_test_title.setReadOnly(True)
        complete_test_layout.addWidget(complete_test_title)

        complete_test_text = QLineEdit(complete_test_layout_widget)
        complete_test_text.setObjectName("complete_test_text")
        complete_test_text.setText("Please click \"Continue\" to proceed or \"Save and Exit\" to save your progress and quit this session.")
        complete_test_text.setReadOnly(True)
        complete_test_layout.addWidget(complete_test_text)

        complete_test_button_layout_widget = QWidget()
        complete_test_button_layout = QHBoxLayout(complete_test_button_layout_widget)

        self.tremor_next_button = QPushButton(complete_test_button_layout_widget)
        self.tremor_next_button.setObjectName("next_button")
        self.tremor_next_button.setText("CONTINUE")
        complete_test_button_layout.addWidget(self.tremor_next_button)

        self.tremor_save_exit_button = QPushButton(complete_test_button_layout_widget)
        self.tremor_save_exit_button.setObjectName("save_exit_button")
        self.tremor_save_exit_button.setText("SAVE AND EXIT")
        complete_test_button_layout.addWidget(self.tremor_save_exit_button)

        complete_test_layout.addWidget(complete_test_button_layout_widget)


    def setup_questionnaire_screen(self):
        questionnaire_layout_widget = QWidget(self.questionnaire_screen)
        questionnaire_layout_widget.setGeometry(self.frame.geometry())

        questionnaire_layout = QVBoxLayout(questionnaire_layout_widget)

        questionnaire_title = QLineEdit(questionnaire_layout_widget)
        questionnaire_title.setObjectName("questionnaire_title")
        questionnaire_title.setText("Questionnaire")
        questionnaire_title.setReadOnly(True)
        questionnaire_layout.addWidget(questionnaire_title)


        question1_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question1_layout)

        question1_text = QLineEdit(questionnaire_layout_widget)
        question1_text.setObjectName("question1")
        question1_text.setText("1. Do you think you have a tremor?")
        question1_text.setReadOnly(True)
        question1_layout.addWidget(question1_text)

        question1_buttonlayout = QHBoxLayout()
        question1_layout.addLayout(question1_buttonlayout)

        question1_button0 = QRadioButton()
        question1_button0.setObjectName("q1b0")
        question1_button0.setText("Yes")
        question1_button0.setChecked(False)

        question1_button1 = QRadioButton()
        question1_button1.setObjectName("q1b1")
        question1_button1.setText("Unsure")
        question1_button1.setChecked(False)

        question1_button2 = QRadioButton()
        question1_button2.setObjectName("q1b2")
        question1_button2.setText("No")
        question1_button2.setChecked(True)
        
        question1_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question1_buttongroup.setExclusive(True)
        question1_buttongroup.addButton(question1_button0, 0)
        question1_buttongroup.addButton(question1_button1, 1)
        question1_buttongroup.addButton(question1_button2, 2)

        question1_buttonlayout.addWidget(question1_button0)
        question1_buttonlayout.addWidget(question1_button1)
        question1_buttonlayout.addWidget(question1_button2)

        question2_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question2_layout)

        question2_text = QLineEdit(questionnaire_layout_widget)
        question2_text.setObjectName("question2")
        question2_text.setText("2. If you have a tremor, is it worse when writing or using utensils?")
        question2_text.setReadOnly(True)
        question2_layout.addWidget(question2_text)

        question2_buttonlayout = QHBoxLayout(questionnaire_layout_widget)
        question2_layout.addLayout(question2_buttonlayout)

        question2_button0 = QRadioButton()
        question2_button0.setText("Yes")
        question2_button0.setChecked(False)

        question2_button1 = QRadioButton()
        question2_button1.setText("Unsure")
        question2_button1.setChecked(False)

        question2_button2 = QRadioButton()
        question2_button2.setText("No")
        question2_button2.setChecked(True)
        
        question2_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question2_buttongroup.setExclusive(True)
        question2_buttongroup.addButton(question2_button0, 0)
        question2_buttongroup.addButton(question2_button1, 1)
        question2_buttongroup.addButton(question2_button2, 2)

        question2_buttonlayout.addWidget(question2_button0)
        question2_buttonlayout.addWidget(question2_button1)
        question2_buttonlayout.addWidget(question2_button2)


        question3_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question3_layout)

        question3_text = QLineEdit(questionnaire_layout_widget)
        question3_text.setObjectName("question3")
        question3_text.setText("3. Is tremor worse when resting arm?")
        question3_text.setReadOnly(True)
        question3_layout.addWidget(question3_text)

        question3_buttonlayout = QHBoxLayout(questionnaire_layout_widget)
        question3_layout.addLayout(question3_buttonlayout)

        question3_button0 = QRadioButton()
        question3_button0.setText("Yes")
        question3_button0.setChecked(False)

        question3_button1 = QRadioButton()
        question3_button1.setText("Unsure")
        question3_button1.setChecked(False)

        question3_button2 = QRadioButton()
        question3_button2.setText("No")
        question3_button2.setChecked(True)
        
        question3_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question3_buttongroup.setExclusive(True)
        question3_buttongroup.addButton(question3_button0, 0)
        question3_buttongroup.addButton(question3_button1, 1)
        question3_buttongroup.addButton(question3_button2, 2)

        question3_buttonlayout.addWidget(question3_button0)
        question3_buttonlayout.addWidget(question3_button1)
        question3_buttonlayout.addWidget(question3_button2)


        question4_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question4_layout)

        question4_text = QLineEdit(questionnaire_layout_widget)
        question4_text.setObjectName("question4")
        question4_text.setText("4. Have you/anyone noticed slowness of movement or walking?")
        question4_text.setReadOnly(True)
        question4_layout.addWidget(question4_text)

        question4_buttonlayout = QHBoxLayout(questionnaire_layout_widget)
        question4_layout.addLayout(question4_buttonlayout)

        question4_button0 = QRadioButton()
        question4_button0.setText("Yes")
        question4_button0.setChecked(False)

        question4_button1 = QRadioButton()
        question4_button1.setText("No")
        question4_button1.setChecked(True)
        
        question4_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question4_buttongroup.setExclusive(True)
        question4_buttongroup.addButton(question4_button0, 0)
        question4_buttongroup.addButton(question4_button1, 1)

        question4_buttonlayout.addWidget(question4_button0)
        question4_buttonlayout.addWidget(question4_button1)


        question5_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question5_layout)

        question5_text = QLineEdit(questionnaire_layout_widget)
        question5_text.setObjectName("question5")
        question5_text.setText("5. Has anyone noticed you acting out your dreams in sleep?")
        question5_text.setReadOnly(True)
        question5_layout.addWidget(question5_text)

        question5_buttonlayout = QHBoxLayout(questionnaire_layout_widget)
        question5_layout.addLayout(question5_buttonlayout)

        question5_button0 = QRadioButton()
        question5_button0.setText("Yes")
        question5_button0.setChecked(False)

        question5_button1 = QRadioButton()
        question5_button1.setText("No")
        question5_button1.setChecked(True)

        question5_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question5_buttongroup.setExclusive(True)
        question5_buttongroup.addButton(question5_button0, 0)
        question5_buttongroup.addButton(question5_button1, 1)

        question5_buttonlayout.addWidget(question5_button0)
        question5_buttonlayout.addWidget(question5_button1)

        question6_layout = QVBoxLayout()
        questionnaire_layout.addLayout(question6_layout)

        question6_text = QLineEdit(questionnaire_layout_widget)
        question6_text.setObjectName("question6")
        question6_text.setText("6. Do you have constipation?")
        question6_text.setReadOnly(True)
        question6_layout.addWidget(question6_text)

        question6_buttonlayout = QHBoxLayout(questionnaire_layout_widget)
        question6_layout.addLayout(question6_buttonlayout)

        question6_button0 = QRadioButton()
        question6_button0.setText("Yes")
        question6_button0.setChecked(False)

        question6_button1 = QRadioButton()
        question6_button1.setText("No")
        question6_button1.setChecked(True)
        
        question6_buttongroup = QButtonGroup(questionnaire_layout_widget)
        question6_buttongroup.setExclusive(True)
        question6_buttongroup.addButton(question6_button0, 0)
        question6_buttongroup.addButton(question6_button1, 1)

        question6_buttonlayout.addWidget(question6_button0)
        question6_buttonlayout.addWidget(question6_button1)

        self.questionnaire_complete_button = QPushButton(questionnaire_layout_widget)
        self.questionnaire_complete_button.setObjectName("questionnaire_complete_button")
        self.questionnaire_complete_button.setText("Submit")
        questionnaire_layout.addWidget(self.questionnaire_complete_button)
        
        self.questionnaire_grouped_buttons = [question1_buttongroup, question2_buttongroup,
                                              question3_buttongroup, question4_buttongroup,
                                              question5_buttongroup, question6_buttongroup]

    def setup_result_screen(self):
        result_layout_widget = QWidget(self.result_screen)
        result_layout_widget.setGeometry(self.frame.geometry())

        result_layout = QVBoxLayout(result_layout_widget)

        result_title_text = QLineEdit(result_layout_widget)
        result_title_text.setObjectName("result_title_text")
        result_title_text.setText("Results")
        result_title_text.setReadOnly(True)
        result_layout.addWidget(result_title_text)
        
        result_spiral_image_text = QLineEdit(result_layout_widget)
        result_spiral_image_text.setObjectName("result_spiral_image_text")
        result_spiral_image_text.setText("Spiral Image: ")
        result_layout.addWidget(result_spiral_image_text)
        
        # result_spiral_image = QLabel(result_layout_widget)
        
        result_tremor_text = QLineEdit(result_layout_widget)
        result_tremor_text.setObjectName("result_tremor_text")
        result_tremor_text.setText("Tremor frequency: ")
        result_layout.addWidget(result_tremor_text)
        
        self.result_tremor_frequency_text = QLineEdit(result_layout_widget)
        self.result_tremor_frequency_text.setObjectName("result_tremor_frequency_text")
        result_layout.addWidget(self.result_tremor_frequency_text)
        
        result_questionnaire_title = QLineEdit(result_layout_widget)
        result_questionnaire_title.setObjectName("result_questionnaire_title")
        result_questionnaire_title.setText("Questionnaire Results: ")
        result_layout.addWidget(result_questionnaire_title)
        
        self.result_questionnaire_q1 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q1.setObjectName("result_questionnaire_q1")
        self.result_questionnaire_q1.setText("1. ")
        result_layout.addWidget(self.result_questionnaire_q1)
        
        self.result_questionnaire_q2 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q2.setObjectName("result_questionnaire_q2")
        self.result_questionnaire_q2.setText("2. ")
        result_layout.addWidget(self.result_questionnaire_q2)
        
        self.result_questionnaire_q3 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q3.setObjectName("result_questionnaire_q3")
        self.result_questionnaire_q3.setText("3. ")
        result_layout.addWidget(self.result_questionnaire_q3)
        
        self.result_questionnaire_q4 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q4.setObjectName("result_questionnaire_q4")
        self.result_questionnaire_q4.setText("4. ")
        result_layout.addWidget(self.result_questionnaire_q4)
        
        self.result_questionnaire_q5 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q5.setObjectName("result_questionnaire_q5")
        self.result_questionnaire_q5.setText("5. ")
        result_layout.addWidget(self.result_questionnaire_q5)
        
        self.result_questionnaire_q6 = QLineEdit(result_layout_widget)
        self.result_questionnaire_q6.setObjectName("result_questionnaire_q6")
        self.result_questionnaire_q6.setText("6. ")
        result_layout.addWidget(self.result_questionnaire_q6)

        self.result_next_button = QPushButton(result_layout_widget)
        self.result_next_button.setObjectName("result_next_button")
        self.result_next_button.setText("Finish")
        result_layout.addWidget(self.result_next_button)
    
    def setup_complete_screen(self):
        complete_layout_widget = QWidget(self.complete_screen)
        complete_layout_widget.setGeometry(self.frame.geometry())

        complete_layout = QVBoxLayout(complete_layout_widget)

        complete_text = QLineEdit(complete_layout_widget)
        complete_text.setObjectName("complete_text")
        complete_text.setText("Thank you for using Spiria!")
        complete_text.setReadOnly(True)

        self.complete_button = QPushButton(complete_layout_widget)
        self.complete_button.setObjectName("complete_button")
        self.complete_button.setText("Finish")
        complete_layout.addWidget(self.complete_button)


    def set_screen(self, screen):
        self.stacked_widget.setCurrentIndex(screen)
        self.reset_screen(True)
        
    def reset_screen(self, status):
        if status == True:
            curr_index = self.stacked_widget.currentIndex()
            print(curr_index)

            if curr_index == SPIRAL_PAIRING_STATE:
                self.spiral_pairing_start_button.setVisible(True)
                self.spiral_pairing_continue_button.setVisible(False)
                self.spiral_pairing_failed_button.setVisible(False)

            elif curr_index == TREMOR_PAIRING_STATE:
                self.tremor_pairing_start_button.setVisible(True)
                self.tremor_pairing_continue_button.setVisible(False)
                self.tremor_pairing_failed_button.setVisible(False)
                
    def reset(self):
        self.setup_calibration_screen()
        self.setup_title_screen()
        self.setup_spiral_pairing_screen()
        self.setup_spiral_test_screen()
        self.setup_spiral_test_complete_screen(self.spiral_complete_test_screen)
        self.setup_tremor_pairing_screen()
        self.tremor_test_start_screen.setGeometry(self.frame.geometry())
        self.setup_tremor_test_start_screen()
        self.setup_tremor_test_screen()
        self.setup_tremor_test_complete_screen(self.tremor_complete_test_screen)
        self.setup_questionnaire_screen()
        self.setup_result_screen()
        self.setup_complete_screen()

    def debug_flip_page(self):
        self.set_screen((self.stacked_widget.currentIndex() + 1) % PAGE_COUNT)

"""
def run():
    import sys
    app = QApplication(sys.argv)
    file = QFile("./styles/title_screen.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    MainWindow = QWidget()
    Ui = Ui_MainWindow()
    Ui.setup_ui(MainWindow)
    MainWindow.showMaximized()
    # MainWindow.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
"""

