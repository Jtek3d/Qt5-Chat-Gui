# Code starts
import requests
import openai
import sys
#import torch
#import black
#import transformers
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#import tensorflow as tf


class MyTextEdit(QTextEdit):
    enterPressed = pyqtSignal()  # Add the enterPressed signal here

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)
        self.setViewportMargins(0, 0, 0, 0)
	
	#preset prompts quick buttons for topic changes
	self.preset1 = "You are the are a story writer. tell me a story of a hero running jobs in acyberpunkworld."

	self.preset2 = "you are the head code develoveloper gone freelance, and i'm the paying customer"

	self.preset3 = "you are the dungeon master of dungeons and dragons dice roll game."

	self.preset4 = "you will emulate the complete game of the classic bbs game of legend of the red dragon."
	self.preset4 += "you will control and keep track of all my character inventory stats."
	self.preset4 += "you will generate the battle sequences based om dice rolls"
	
    def setPreset(self, preset):
	#personality button defaults
        if preset == "fantasy_story": 
            #self.engine = "fantasy_story_model"
            self.max_tokens = 1024
            self.temperature = 2.0
            self.top_p = 0.1
            self.n = 10
        elif preset == "science_story":
            #self.engine = "science_story_model"
            self.max_tokens = 1024
            self.temperature = 0.03
            self.top_p = 1.0
            self.n = 2
        elif preset == "code":
            #self.engine = "code_model"
            self.max_tokens = 1024
            self.temperature = 0.01
            self.top_p = 1
            self.n = 1
        elif preset == "conversation":
            #self.engine = "conversation_model"
            self.max_tokens = 1512
            self.temperature = 2.0
            self.top_p = 0.33
            self.n = 1
        elif preset == "custom":
            #self.engine = "custom_model"
            self.max_tokens = 2048
            self.temperature = 0.8
            self.top_p = 0.50
            self.n = 1
        else:
            #self.engine = "davinci"
            self.max_tokens = 1512
            self.temperature = 0.6
            self.top_p = 1.0
            self.n = 1

    def aiPreset0(self, preset):
        self.topic_field.setText(self.preset1)
    def aiPreset1(self, preset):
        self.topic_field.setText(self.preset2))
    def aiPreset2(self, preset):
        self.topic_field.setText(self.preset3)
    def aiPreset3(self, preset):
        self.topic_field.setText(self.preset4))

    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, event):
#        if event.key() == Qt.Key_Return and not Qt.Key_Shift and not event.modifiers():
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self.enterPressed.emit()  # Emit the signal here
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            curr_pos = self.viewport().mapFromGlobal(event.globalPos())
            diff = curr_pos - self.viewport().mapFromGlobal(self.__mouseMovePos)
            self.__mouseMovePos = event.globalPos()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())

class OpenAIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    #has to be after the __init__ or api erases

    @pyqtSlot()

    def clear_history(self):
        """Clears the text in the response field widget."""
        self.response_field.clear()
    def readFile(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()


   #fileattach function     
    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            # Set the text of the text box to the selected file name
            self.attachName.setText(file_name)
   #post highlighting
    def highlightPost(self):
        # Make sure the response_field widget is initialized
        if not self.response_field:
            return

        # Initialize the cursor for the response_field widget
        cursor = self.response_field.textCursor()

        # Find the first occurrence of the "Me:" tag
        cursor = self.response_field.document().find(self.convTag_me)

        # Find the first occurrence of the "Bot:" tag after the "Me:" tag
        cursor = self.response_field.document().find(self.convTag_bot, cursor)

        # Select the text between the two occurrences of the conversation tags
        cursor.setPosition(cursor.selectionStart())
        cursor.setPosition(cursor.selectionEnd(), QTextCursor.KeepAnchor)
        self.response_field.setTextCursor(cursor)
    def highlightPostOnClick(self, event):
        self.highlightPost()
    def remove_clicked(self):
        # Replace .hasSelectedText() with .textCursor().hasSelection()
        if self.response_field.textCursor().hasSelection():
            # Replace .selectedText() with .textCursor().selectedText()
            self.response_field.textCursor().removeSelectedText()

    def remove_clicked(self):
        cursor = self.response_field.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
    #---------------------
    # this is the image generator
    #*----------------------
    def save_image(prompt, img_data):
        # Generate a file name based on the prompt
        file_name = prompt.replace(" ", "-") + ".png"

        # If a file with the same name already exists, add a number to the end of the file name
        if os.path.exists(file_name):
            i = 1
            while os.path.exists(file_name):
                file_name = prompt.replace(" ", "-") + "-" + str(i) + ".png"
                i += 1

        # Save the image to a file
        img_data.save(file_name, "PNG", quality=100)

    def generate_images(self):
        # Generate the image using the OpenAI API and the user's input
        image_resp = openai.Image.create(prompt=inP, n=4, size="512x512")

        # Loop through the list of images
        for img_data in image_resp.data:
            
            # Save the image to a file using the save_image function
            save_image(inP, self.DownloadImage("url"))

    def DownloadImage(self):  ## img object
        # Download the image from the URL      
        img_url = img_data["url"]
        img_response = requests.get(img_url)
        img_bytes = img_response.content

        # Load the image from the bytes
        img = Image.open(io.BytesIO(img_bytes))
        return img

    #--------------------------
    # end img gen
    #--------------------------


    @pyqtSlot()
    def generate(self):

        self.attach_file = ""
        if self.attachFile.isChecked():
            attach_name = self.attachName.text()
            if attach_name != "":
                #try:
                    with open(attach_name, 'r') as f:
                        lines = f.readlines()
                        self.attach_file = (f"file : \n'''\n" )
                        for line in lines:
                            self.attach_file += line
                        self.attach_file += (f"'''")
#                except Exception as e:
#                    print("An error occurred while reading the file:", e)
#                    self.attach_file = ""
        self.createHistory()
        self.generateResponse()
    def createHistory(self):
        data = self.input_field.toMarkdown()
        self.input_field.clear()
        current_text = self.response_field.toMarkdown()
        self.response_field.append(f"<span style='color: lightblue;'>{self.convTag_me}</span>" + data)
        self.sendBuffer = f"Topic-{self.topic_field.text()}\n{self.response_field.toMarkdown()}\n{self.attach_file}"        #f"User: {user_id}\n{prompt}\n{check_attach()}" 

        
    def generateResponseLocal(self):    
        model = transformers.TFGPT2Model.from_pretrained("./ggml-model-q4_1.bin")
#        model = transformers.TFGPT2Model.from_pretrained("./model.bin")
        model.to(torch.device("cuda"))
        # Generate text using the model
        input_text = 'Hello, how are you today?'
        output_text = model.generate(
            prompt=self.sendBuffer, 
            max_length=128, 
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p= self.top_p,
            n= self.n)

        # Print the generated text
        print(output_text)
        self.response_field.append(output_text)

    def getKey(self):
        # check if attached is checked
	    with open("./api_key.txt", 'r') as f:
	    	_ = f.readlines()
	if f'_:3' = "sk_":
		self.API_KEY = _
		

    def generateResponse(self):    
        try:
            # Generate a response to the full prompt
#            response = openai.Completion.create(
#                engine="text-davinci-003",
#                prompt=self.sendBuffer,
#                max_tokens=self.max_tokens,
#                temperature=self.temperature,
#                top_p=self.top_p,
#                n=self.n,
#            )

	    self.setKey
            ENDPOINT_URL = "https://api.openai.com/v1/completions"
            response = requests.post(
                ENDPOINT_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.API_KEY}",
                },
                json={
                    "prompt": self.sendBuffer,
                    "model":"text-davinci-003",
                    #"model":"code-davinici-001",
                    #"model":"text-ada-001",
                   
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "n": self.n,
                },)


            # Set the response in the response widget
            #self.response_field.append("<span style='color: blue;'><b><u>----------------------</b></u></span><br>")
            #print(response["choices"][0]["text"])
#            if response.json()["choices"][0]["text"] == ('choices'):
#                print(response.json())
#            else:
            print(response.json()["choices"][0]["text"])
            self.response_field.append("Bot :" + response.json()["choices"][0]["text"])
        except Exception as e:
            # Handle the error here
            print(response.json())
            print(e)
    def checkifImage(self):
        if self.image_button.toggled():
            self.generate_images()
        else:
            self.generateResponse()


    def initUI(self):
        #extra includes for chat
        self.convTag_me = "Me :"
        self.convTag_bot = "Bot :"
        self.topic = "Topic: bot conversation history test"
        # Create the input field, button, and response widget
        self.setPreset("default")
        #self.stacked_widget.setCurrentIndex(1)
        #self.setLayout(self.mainLayout)

        self.label_topic = QLabel("Topic:")
        self.topic_field = QLineEdit(self.topic)
        # user input
        self.label_Input = QLabel("Input", self)
        self.input_field = MyTextEdit(self)
#        self.input_field.enterEvent(self.generate)
        self.input_field.enterPressed.connect(lambda: self.generate())
        self.label_Output = QLabel("History", self)
        self.preset0_button = QPushButton("writer", self)
        self.preset1_button = QPushButton("programer", self)
        self.preset2_button = QPushButton("rpg writter", self)
        self.preset3_button = QPushButton("....", self)
        self.toolbar_layout = QHBoxLayout()
        self.toolbar_layout.addWidget(self.label_Output)
        self.toolbar_layout.addWidget(self.preset0_button)
        self.toolbar_layout.addWidget(self.preset1_button)
        self.toolbar_layout.addWidget(self.preset2_button)
        self.toolbar_layout.addWidget(self.preset3_button)

        self.preset0_button.clicked.connect(self.aiPreset0)
        self.preset1_button.clicked.connect(self.aiPreset1)
        self.preset2_button.clicked.connect(self.aiPreset2)
        self.preset3_button.clicked.connect(self.aiPreset3)

        self.response_field = MyTextEdit(self)  ## custom version of the text box
        #self.response_field = QTextEdit(self) ## origin version of the text box
        self.response_field.setReadOnly(True)
        #self.response_field.enterPressed(self.generate)
        self.response_field.enterPressed.connect(lambda: self.generate())
 #       self.response_field.verticalScrollBar().setMinimumWidth(100)

        self.clear_button = QPushButton("Clear", self)
        self.remove_button = QPushButton("Remove", self)
        self.generate_button = QPushButton("&Send", self)
        #create chat window features
        self.button_layout = QHBoxLayout()
#        self.mainLayout.addWidget(self.label_Input)
        self.button_layout.addWidget(self.label_Input)
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.remove_button)
        self.button_layout.addWidget(self.generate_button)
        #give them action
        self.clear_button.clicked.connect(self.clear_history)
        self.remove_button.clicked.connect(self.remove_clicked)
        self.generate_button.clicked.connect(self.generate)


        # Create a check box and set its initial state to checked
        self.attachName = QLineEdit("")
        self.browse_button = QPushButton("Select")
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.attachFile = QCheckBox("Attach")
        self.LoadedFile = ""
        self.attachFile.setChecked(False)
        # Create a horizontal layout and add the check box, browse button, and text box
        self.attach_layout = QHBoxLayout()
        self.attach_layout.addWidget(self.attachName)
        self.attach_layout.addWidget(self.browse_button)
        self.attach_layout.addWidget(self.attachFile)


        self.fantasy_story_button = QToolButton()
        self.fantasy_story_button.setText("Fantasy")
        self.fantasy_story_button.setCheckable(True)

        self.science_story_button = QToolButton()
        self.science_story_button.setText("Science")
        self.science_story_button.setCheckable(True)

        self.code_button = QToolButton()
        self.code_button.setText("Code")
        self.code_button.setCheckable(True)

        self.conversation_button = QToolButton()
        self.conversation_button.setText("Conversation")
        self.conversation_button.setCheckable(True)

        self.image_button = QToolButton()
        self.image_button.setText("Image")
        self.image_button.setCheckable(True)

        self.default_button = QToolButton()
        self.default_button.setText("Default")
        self.default_button.setCheckable(True)
        self.default_button.physicalDpiX()
        #build its layout
        self.preset_layout = QHBoxLayout()
        self.preset_layout.addWidget(self.fantasy_story_button)
        self.preset_layout.addWidget(self.science_story_button)
        self.preset_layout.addWidget(self.code_button)
        self.preset_layout.addWidget(self.conversation_button)
        self.preset_layout.addWidget(self.image_button)
        self.preset_layout.addWidget(self.default_button)
        #give them acttion
        self.fantasy_story_button.toggled.connect(lambda: self.setPreset("fantasy_story"))
        self.science_story_button.toggled.connect(lambda: self.setPreset("science_story"))
        self.code_button.toggled.connect(lambda: self.setPreset("code"))
        self.conversation_button.toggled.connect(lambda: self.setPreset("conversation"))
        self.default_button.toggled.connect(lambda: self.setPreset("default"))

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.fantasy_story_button)
        self.buttonGroup.addButton(self.science_story_button)
        self.buttonGroup.addButton(self.code_button)
        self.buttonGroup.addButton(self.conversation_button)
        self.buttonGroup.addButton(self.image_button)
        self.buttonGroup.addButton(self.default_button)

        # Create the stacked widget and the two pages
        self.stacked_widget = QStackedWidget()
        self.page1 = QWidget()
        self.page2 = QWidget()

        # Add the pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.attach_layout)
        self.mainLayout.addLayout(self.preset_layout)
        self.mainLayout.addLayout(self.toolbar_layout)
        self.mainLayout.addWidget(self.topic_field)
        self.mainLayout.addWidget(self.response_field)
        self.mainLayout.addLayout(self.button_layout)
        self.mainLayout.addWidget(self.input_field)

    def loadPage2(self):
        self.label_title = QLabel("Title:")
        self.page2_layout = QVBoxLayout()
        self.page2_layout.addWidget(self.label_title)
        # Set the layout of the second page
        self.page2.setLayout(self.page2_layout)


    def toolbar(self):
        # Create the switch button
        self.switch_button = QPushButton("Switch")
        self.switch_button.clicked.connect(self.switch_pages)

        # Create a horizontal layout and add the switch button and stacked widget
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.switch_button)
        self.layout.addWidget(self.stacked_widget)

        # Create a widget to hold the layout, and set it as the central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def switch_pages(self):
        # Toggle between the two pages
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpenAIWindow()
    window.show()
    app.exec_()

# Code ends










