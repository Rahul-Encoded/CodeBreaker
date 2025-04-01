import \
    sys  # Import the sys module for system-specific parameters and functions (e.g., command-line arguments, exiting the program).
import os  # Import the os module for interacting with the operating system (e.g., environment variables, file paths).
import time  # Import the time module for time-related functions (e.g., pausing execution).
import \
    cv2  # Import the OpenCV library (cv2) for image processing tasks (e.g., capturing, processing, and displaying images).
import numpy as np  # Import the NumPy library (np) for numerical operations, especially for working with arrays.
import \
    google.generativeai as genai  # Import the google.generativeai library for interacting with Google's generative AI models.
import pytesseract  # Import the pytesseract library for optical character recognition (OCR) tasks.
import markdown  # Import the markdown library to convert markdown text to HTML
import mss  # Import the mss library for fast screen capture.
from dotenv import \
    load_dotenv  # Import the load_dotenv function from the dotenv library to load environment variables from a .env file.
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, \
    QScrollArea  # Import necessary PyQt5 widgets for creating the GUI.
from PyQt5.QtCore import Qt, QThread, \
    pyqtSignal  # Import necessary PyQt5 core modules for GUI functionality and threading.
import ctypes

# Set the path to Tesseract OCR executable (Windows specific)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Rahul\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"  # Specifies the path to the Tesseract OCR executable.  This is crucial for pytesseract to work correctly.  The path may need to be adjusted based on the user's installation location.

# Load API key from .env file
load_dotenv()  # Loads environment variables from a .env file into the process's environment.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Retrieves the value of the GOOGLE_API_KEY environment variable.
if not GOOGLE_API_KEY:  # Checks if the GOOGLE_API_KEY is missing or empty.
    raise ValueError(
        "Missing Google API Key! Check your .env file.")  # Raises a ValueError exception if the API key is missing, indicating a configuration error.

# Configure LLM model
genai.configure(
    api_key=GOOGLE_API_KEY)  # Configures the google.generativeai library with the provided API key.  This authenticates the application to use Google's generative AI services.
model = genai.GenerativeModel(
    "gemini-2.0-flash")  # Initializes a GenerativeModel object with the "gemini-2.0-flash" model, which is a faster, cheaper version of gemini.  This model will be used to generate text.


def select_region():
    """
Manually select a region for screen capture using OpenCV mouse events.
Ensures the selection window stays on top and is undetectable by screen-sharing tools.
    """
    with mss.mss() as sct:  # Creates an mss object for screen capture.
        screenshot = np.array(sct.grab(sct.monitors[1]))  # Capture the full screen and convert it to a NumPy array.

    coords = []  # Initializes an empty list to store the coordinates of the selected region.

    def mouse_callback(event, x, y, flags, param):
        """
Callback function for mouse events in the OpenCV window.
Records the coordinates of the mouse when the left button is pressed and released.
        """
        if event == cv2.EVENT_LBUTTONDOWN:  # Checks if the left mouse button was pressed.
            coords.clear()  # Clears the coordinates list to start a new selection.
            coords.append((x, y))  # Appends the current mouse coordinates to the list.
        elif event == cv2.EVENT_LBUTTONUP:  # Checks if the left mouse button was released.
            coords.append((x, y))  # Appends the current mouse coordinates to the list.
            cv2.destroyAllWindows()  # Closes the OpenCV window after the region is selected.

    # Create the OpenCV window
    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)  # Creates an OpenCV window named "Select Region."
    cv2.setWindowProperty("Select Region", cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)  # Sets the window to full-screen mode.

    # Ensure the window stays on top using Windows API
    hwnd = ctypes.windll.user32.FindWindowW(None, "Select Region")  # Get the handle of the OpenCV window.
    if hwnd:
        # Set the window to stay on top
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0,
                                          0x0001 | 0x0002)  # HWND_TOPMOST | SWP_NOMOVE | SWP_NOSIZE

        # Make the window layered and transparent
        ctypes.windll.user32.SetWindowLongW(hwnd, 20, 0x00080000 | 0x00000020)  # WS_EX_LAYERED | WS_EX_TRANSPARENT

        # Exclude the window from screen sharing (undetectable by Google Meet, Zoom, etc.)
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)  # WDA_MONITOR

    cv2.setMouseCallback("Select Region", mouse_callback)  # Sets the mouse callback function.

    while len(coords) < 2:  # Loops until two coordinates (start and end) are collected.
        cv2.imshow("Select Region", screenshot)  # Displays the screenshot in the window.
        cv2.waitKey(1)  # Waits for a key event for 1 millisecond.

    x1, y1 = coords[0]  # Extracts the x and y coordinates of the starting point.
    x2, y2 = coords[1]  # Extracts the x and y coordinates of the ending point.

    return min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)  # Returns the selected region's coordinates.


def capture_question(region):
    """
Captures a selected screen region and extracts text using OCR.
    """
    try:
        with mss.mss() as sct:  # Creates an mss object for screen capture.
            monitor = {"top": region[1], "left": region[0], "width": region[2],
                       "height": region[3]}  # Defines the region to capture based on the provided coordinates.
            screenshot = sct.grab(monitor)  # Captures the specified region of the screen.
            img = np.array(screenshot)  # Converts the screenshot to a NumPy array for image processing.

            # Preprocess image
            gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)  # Converts the image to grayscale.
            _, processed_img = cv2.threshold(gray, 0, 255,
                                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Applies adaptive thresholding to create a binary image, improving OCR accuracy.

            return pytesseract.image_to_string(
                processed_img).strip()  # Performs OCR on the processed image and returns the extracted text, removing leading/trailing whitespace.
    except Exception as e:  # Catches any exceptions that occur during the screenshot capture or OCR process.
        print(f"[!] Screenshot capture failed: {e}")  # Prints an error message if the screenshot capture fails.
        return None  # Returns None to indicate that the question capture failed.


class LLMThread(QThread):
    """
A QThread to run the LLM inference without blocking the GUI.
    """
    result_ready = pyqtSignal(str)  # Defines a custom signal that emits a string when the LLM processing is complete.

    def __init__(self, question):
        """
Initializes the LLMThread with the question to be processed.
        """
        super().__init__()  # Calls the constructor of the parent class (QThread).
        self.question = question  # Stores the question to be processed by the LLM.

    def run(self):
        """
The main function executed when the thread starts.
It calls the LLM to generate a response to the question and emits the result_ready signal with the answer.
        """
        try:
            prompt = f"Solve this question using C++ with necessary comments inside a markdown code block:\n{self.question}"  # Creates a prompt for the LLM including a request to provide the answer in C++ with comments.
            response = model.generate_content(prompt)  # Sends the prompt to the LLM model and retrieves the response.
            answer = response.text if response.text else "No answer generated."  # Extracts the answer from the response. If the response is empty, provides a default message.
        except Exception as e:  # Catches any exceptions that occur during the LLM processing.
            answer = f"Error: {e}"  # Sets the answer to an error message if an exception occurs.

        self.result_ready.emit(
            answer)  # Emits the result_ready signal with the answer. This signal is connected to the GUI to update the display.


class TransparentOverlay(QWidget):
    """
A transparent overlay window to display the LLM's answer.
The size of the window dynamically adjusts to fit the content.
"""

    def __init__(self, x=800, y=0):
        """
Initializes the TransparentOverlay with a default position and size.
        """
        super().__init__()  # Calls the constructor of the parent class (QWidget).

        # Set window flags to make it stay on top, frameless, and act as a tool window
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.X11BypassWindowManagerHint
        )

        # Make the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)  # Makes the background of the window transparent.
        self.setAttribute(Qt.WA_NoSystemBackground)  # Prevents the window from having a default system background.
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # Prevents the window from activating when shown.

        # Get the window handle (HWND) for the current window
        hwnd = int(self.winId())

        # Set the window to be layered and transparent (for Windows)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x00080000 | 0x00000020)  # WS_EX_LAYERED | WS_EX_TRANSPARENT

        # Exclude the window from screen sharing (undetectable by Google Meet, Zoom, etc.) (for Windows)
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)  # WDA_MONITOR

        # Set the style for the overlay: semi-transparent background and rounded corners
        self.setStyleSheet("background-color: rgba(1, 1, 1, 50%); border-radius: 10px;")

        # Create a vertical layout to arrange the label
        self.layout = QVBoxLayout()
        self.label = QLabel("Fetching...", self)
        self.label.setTextFormat(Qt.RichText)  # Enables rich text formatting (like HTML) in the label
        self.label.setStyleSheet("color: white; font-size: 20px; padding: 10px;")  # Style the label
        self.label.setWordWrap(True)  # Ensure text wraps within the label

        # Add the label to the main layout
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Set initial size and position of the window
        self.resize(800, 600)
        self.move(x, y)
        self.show()

    def update_text(self, new_text):
        """
Updates the text in the label with the new LLM answer.
Dynamically adjusts the window size to fit the content without scrollbars.
        """
        if self.label.text() == new_text:  # Check if the new text is the same as the current text
            return

        # Convert markdown to HTML using the 'fenced_code' and 'codehilite' extensions for code formatting
        import markdown
        html_text = markdown.markdown(new_text, extensions=['fenced_code', 'codehilite'])
        self.label.setText(html_text)

        # Calculate the size of the label based on its content
        self.label.adjustSize()  # Adjusts the size of the label to fit the content

        # Calculate the new size of the window based on the label's size
        padding = 40  # Add padding for margins and styling
        new_width = min(self.label.width() + padding, 1200)  # Limit the maximum width to 1200 pixels
        new_height = min(self.label.height() + padding, 800)  # Limit the maximum height to 800 pixels

        # Resize the window to fit the content
        self.resize(new_width, new_height)


if __name__ == "__main__":
    time.sleep(2)  # Stealth delay before execution. Pauses the execution for 2 seconds to avoid immediate detection.

    selected_region = select_region()  # User selects the region on the screen. Calls the select_region function to allow the user to select a region on the screen.
    question_text = capture_question(selected_region)  # Captures the question from the selected region using OCR.

    app = QApplication(sys.argv)  # Creates a QApplication object, which is necessary for any PyQt GUI application.

    overlay = TransparentOverlay()  # Creates an instance of the TransparentOverlay window.

    if question_text:  # Checks if the question text was successfully captured.
        llm_thread = LLMThread(question_text)  # Creates an instance of the LLMThread with the captured question.
        llm_thread.result_ready.connect(
            overlay.update_text)  # Connects the result_ready signal from the LLMThread to the update_text slot in the TransparentOverlay.  This allows the GUI to update when the LLM processing is complete.
        llm_thread.start()  # Starts the LLMThread, initiating the LLM processing in a separate thread.
    else:
        overlay.update_text(
            "Failed to capture question.")  # Updates the overlay text to indicate a failure if the question capture failed.

    sys.exit(app.exec_())  # Starts the PyQt event loop and exits the application when the loop finishes.
