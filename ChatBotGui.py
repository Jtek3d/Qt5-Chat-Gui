#  i don't work on it much and it's far from where i want it it but it's usuable
#
#
# Code starts
import requests
import sys

#gui include
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

global window

class settings():
    def __init__(self):
        self.title = "Gui Bot"

        self.convTag_me = "Me :"
        self.convTag_bot = "Bot :"

        self.ApiKeyFile = "/home/saite/.bigdisk/Assistant/api_key.txt"

        self.models = ["text-davinci-003","text-curie-001", "text-babbage-001","text-ada-001","davinici-instruct-beta",
        "curie-instruct-beta","text-davinci-002","text-davinci-001"]
        #presets for topics
        self.preset1 = "You are the are a story writer. tell me a story of a hero running jobs in acyberpunkworld."
        self.preset2 = "you are the head code develoveloper gone freelance, and i'm the paying customer"
        self.preset3 = "you are the dungeon master of dungeons and dragons dice roll game."

        self.preset4 = "you will emulate the complete game of the classic bbs game of legend of the red dragon." 
        self.preset4 += "you will control and keep track of all my character inventory stats."
        self.preset4 += "you will generate the battle sequences based om dice rolls"

        self.agent = "text-davinci-003"
        self.max_tokens = 1512
        self.temperature = 0.6
        self.top_p = 1.0
        self.n = 1


    def setPreset(self, preset):
        if preset == "fantasy_story": 
            self.agent = "text-davinci-003"
            self.max_tokens = 1024
            self.temperature = 2.0
            self.top_p = 0.1
            self.n = 10
        elif preset == "science_story":
            self.agent = "text-davinci-003"
            self.max_tokens = 1024
            self.temperature = 0.03
            self.top_p = 1.0
            self.n = 2
        elif preset == "code":
            self.agent = "text-davinci-003"
            self.max_tokens = 1024
            self.temperature = 0.01
            self.top_p = 1
            self.n = 1
        elif preset == "conversation":
            self.agent = "text-davinci-003"
            self.max_tokens = 1512
            self.temperature = 2.0
            self.top_p = 0.33
            self.n = 1
        elif preset == "custom":
            self.agent = "text-davinci-003"
            self.max_tokens = 2048
            self.temperature = 0.8
            self.top_p = 0.50
            self.n = 1
        else:

#            window.modelSelect.setCurrentText("text-davinci-003")
            self.agent = "text-davinci-003"
            self.max_tokens = 1512
            self.temperature = 0.6
            self.top_p = 1.0
            self.n = 1

	#presets for personalities

    def aiPreset0(self, preset):
        self.topic_field.setText(self.preset1)
    def aiPreset1(self, preset):
        self.topic_field.setText(self.preset2)
    def aiPreset2(self, preset):
        self.topic_field.setText(self.preset3)
    def aiPreset3(self, preset):
        self.topic_field.setText(self.preset4)

class OpenAIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        settings().setPreset("default")
        self.Settings = settings()    


    @pyqtSlot()

    ################################
    # button functions
    ################################
    def clear_history(self):
        """Clears the text in the response field widget."""
        self.response_field.clear()

    def readFile(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            # Set the text of the text box to the selected file name
            self.attachName.setText(file_name)

    ################################
    # removes text selection or highlighted post
    ################################
    def remove_clicked(self):
        cursor = self.response_field.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
        # Replace .hasSelectedText() with .textCursor().hasSelection()
        elif self.response_field.textCursor().hasSelection():
            # Replace .selectedText() with .textCursor().selectedText()
            self.response_field.textCursor().removeSelectedText()

    ################################
    # post highlighting for removal
    ################################
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
        self.generateResponseApi()

    def createHistory(self):
        data = self.input_field.toMarkdown()
        self.input_field.clear()
        current_text = self.response_field.toMarkdown()
        self.response_field.append(f"<span style='color: lightblue;'>{self.convTag_me}</span>" + data)
        self.sendBuffer = f"Topic-{self.topic_field.text()}\n{self.response_field.toMarkdown()}\n{self.attach_file}"        #f"User: {user_id}\n{prompt}\n{check_attach()}" 

    def GetKey(self):
        _ = self.readFile(settings().ApiKeyFile)
        x = type(_) 
        if type(_) is list:
            _ = _[0]
        if "\n" in _:
            _ = (_.split('\n'))[0]
        
        if f'{_:.3}' == "sk-":
            return _
        else:
            print("key invalid")
            return None            

        
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

    def generateResponseApi(self):
        #temporary fix
        settings().setPreset("default")

        try:
            ENDPOINT_URL = "https://api.openai.com/v1/completions"
            response = requests.post(
                ENDPOINT_URL,
                headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.GetKey()}",
                    },
                    json={
                        "prompt": self.sendBuffer,
                        "model":  self.modelSelect.currentText(),
                        "max_tokens": settings().max_tokens,
                        "temperature": settings().temperature,
                        "top_p": settings().top_p,
                        "n": settings().n,
                    },
                )


            output = response.json()["choices"][0]["text"]
            print(output)
            #adding color to the output
            self.addcolor(output)
            #remove the top line and the one below will just output
            #self.response_field.append("Bot :" + input)

        except Exception as e:
            # Handle the error here
            print(response.json())
            print(e)

    def generateResponseLib(self):    
        import openai
    # Generate a response to the full prompt
        openai.api_key = self.GetKey(self.Settings.ApiKeyFile)
        response = openai.Completion.create(
            engine=self.agent,
            prompt=self.sendBuffer,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            n=self.n
            )
        output = response.json()["choices"][0]["text"]
        print(output)
        #adding color to the output
        self.addcolor(output)
        #remove the top line and the one below will just output
        #self.response_field.append("Bot :" + input)

        
    def addcolor(self, input):       
        # Set the response in the response widget
        self.response_field.append("<span style='color: blue;'><b><u>----------------------</b></u></span><br>")
        self.response_field.append("Bot :" + input)
        self.response_field.append("<span style='color: blue;'><b><u>----------------------</b></u></span><br>")
    		

    def checkifImage(self):
        if self.image_button.toggled():
            self.generate_images()
        else:
            self.generateResponseApi()


    def initUI(self):
        #extra includes for chat
        self.convTag_me =  settings().convTag_me
        self.convTag_bot = settings().convTag_bot
        self.topic = "Topic: bot conversation history test"

        # setting defaults values, to avoid not defined errors
        settings().setPreset("default")

        #self.stacked_widget.setCurrentIndex(1)
        #self.setLayout(self.mainLayout)


        ################################
        # Setting up topic presets gui
        ################################
        self.label_topic = QLabel("Topic:")
        self.preset0_button = QPushButton("writer", self)
        self.preset1_button = QPushButton("programer", self)
        self.preset2_button = QPushButton("rpg writter", self)
        self.preset3_button = QPushButton("....", self)
        #build its layout
#        self.bodyLayout.addWidget(self.label_Output)
        self.presetTopics_layout = QHBoxLayout()
        self.presetTopics_layout.addWidget(self.label_topic)
        self.presetTopics_layout.addWidget(self.preset0_button)
        self.presetTopics_layout.addWidget(self.preset1_button)
        self.presetTopics_layout.addWidget(self.preset2_button)
        self.presetTopics_layout.addWidget(self.preset3_button)
        #give them acttion
        self.preset0_button.clicked.connect(settings().aiPreset0)
        self.preset1_button.clicked.connect(settings().aiPreset1)
        self.preset2_button.clicked.connect(settings().aiPreset2)
        self.preset3_button.clicked.connect(settings().aiPreset3)




 

        ################################
        # Setting up chat and history action buttons
        ################################
        self.clear_button = QPushButton("Clear", self)
        self.remove_button = QPushButton("Remove", self)
        self.generate_button = QPushButton("&Send", self)
        #build the layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.remove_button)
        self.button_layout.addWidget(self.generate_button)
        #give them action
        self.clear_button.clicked.connect(self.clear_history)
        self.remove_button.clicked.connect(self.remove_clicked)
        self.generate_button.clicked.connect(self.generate)


        ################################
        # Setting up attachment gui
        ################################
        self.label_attach = QLabel("File:")
        self.attachName = QLineEdit("")
        self.browse_button = QPushButton("Select")
        self.browse_button.clicked.connect(self.open_file_dialog)
        self.attachFile = QCheckBox("Attach")
        self.LoadedFile = ""
        self.attachFile.setChecked(False)
        #build its layout
        self.attach_layout = QHBoxLayout()
        self.attach_layout.addWidget(self.label_attach)
        self.attach_layout.addWidget(self.attachName)
        self.attach_layout.addWidget(self.browse_button)
        self.attach_layout.addWidget(self.attachFile)

        ################################
        # setting up model select Gui
        ################################
        self.label_model = QLabel("Model:")
        self.modelSelect = QComboBox()
        self.modelSelect.addItems(settings().models)
        #build its layout
        self.modelSel_layout = QHBoxLayout()
        self.modelSel_layout.addWidget(self.label_model)
        self.modelSel_layout.addWidget(self.modelSelect)

        ################################
        # setting up personality presets
        ################################
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
        #togggle switch effect
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.fantasy_story_button)
        self.buttonGroup.addButton(self.science_story_button)
        self.buttonGroup.addButton(self.code_button)
        self.buttonGroup.addButton(self.conversation_button)
        self.buttonGroup.addButton(self.image_button)
        self.buttonGroup.addButton(self.default_button)


        
        ################################
        # Setting up input fields presets gui
        ################################
        self.label_topic = QLabel("Topic:")
        self.topic_field = QLineEdit(self.topic)
        #build its layout
        self.topic_Layout = QHBoxLayout()
#        self.topic_Layout.addWidget(self.label_topic)
        self.topic_Layout.addWidget(self.topic_field)


        ################################
        # Setting up input fields presets gui
        ################################
        self.label_Output = QLabel("History", self)
        self.label_Input = QLabel("Input", self)

        self.input_field = MyTextEdit(self)
        self.input_field.setMaximumHeight(50)
        self.response_field = MyTextEdit(self)  ## custom version of the text box
        self.response_field.setReadOnly(True)
        #self.response_field = QTextEdit(self) ## origin version of the text box

        #build its layout
        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addLayout(self.topic_Layout)
        self.bodyLayout.addWidget(self.label_Output)
        self.bodyLayout.addWidget(self.response_field)
        self.bodyLayout.addLayout(self.button_layout)
        self.bodyLayout.addWidget(self.label_Input)
        self.bodyLayout.addWidget(self.input_field)
        #give them action
        self.input_field.enterPressed.connect(lambda: self.generate())
        self.response_field.enterPressed.connect(lambda: self.generate())
        #scroll bars were hard to grip, grab and scroll now
        #self.response_field.verticalScrollBar().setMinimumWidth(100)

        
        

        ################################
        # Setting up the main layout
        ################################
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.modelSel_layout)
        self.mainLayout.addLayout(self.attach_layout)
        self.mainLayout.addLayout(self.preset_layout)
        self.mainLayout.addLayout(self.presetTopics_layout)

        self.mainLayout.addLayout(self.bodyLayout)

        #.layout = self.button_layout


        ################################
        # layout switching intended for settings
        ################################
        # Create the stacked widget and the two pages
        
        ################################################################
        #   this area is unused layout switching code 
        #   currently disbled had trouble using it
        ################################################################


#        self.setLayout(self.mainLayout)
        #window.setLayout(self.mainLayout)
        #self.setLayout = self.mainLayout 

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


    def switch_pages(self):
        # Toggle between the two pages
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)
            
class MyTextEdit(QTextEdit):
    enterPressed = pyqtSignal()  # Add the enterPressed signal here

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)
        self.setViewportMargins(0, 0, 0, 0)
	
    ################################
    # this area is for checking if enter is pressed while 
    # inputting something to save on hitting send
    ################################
    @pyqtSlot(QKeyEvent)
    def keyPressEvent(self, event):
#        if event.key() == Qt.Key_Return and not Qt.Key_Shift and not event.modifiers():
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            self.enterPressed.emit()  # Emit the signal here
        else:
            super().keyPressEvent(event)

    ################################
    # this area is for touch screen scrolling and highlighting
    ################################
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpenAIWindow()
    window.setWindowTitle(settings().title)
    window.show()
    app.exec_()

# Code ends
