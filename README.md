# **CodeBreaker**  
---

## **What is CodeBreaker?**  
CodeBreaker is a **stealthy, AI-powered tool** designed to extract coding questions from screen captures and provide real-time solutions using Google's generative AI models. The script leverages **OCR**, **low-level system APIs**, and **AI wizardry** to operate undetected by screen-sharing tools like Google Meet or Zoom.  

With **dynamic screenshot control**, **adaptive OCR processing**, and a **transparent overlay GUI**, CodeBreaker ensures you stay ahead of the curve—whether you're solving coding challenges, debugging, or just flexing your engineering skills.  

---

## **Features**  
🔥 **Key Features That Make CodeBreaker a Total Menace:**  

1. **Stealth Mode Activated 🌚**  
   - Uses Windows-specific APIs (`SetWindowDisplayAffinity`, layered windows) to make the app **invisible to screen-sharing tools**.  
   - No taskbar presence, no trace—just pure ninja mode.  

2. **Dynamic Screenshot Capture 📸**  
   - Allows users to manually select a region of the screen for capturing.  
   - Processes images with adaptive thresholding to improve OCR accuracy.  

3. **AI-Powered Solutions 💻✨**  
   - Sends captured questions to Google's `gemini-2.0-flash` model for real-time solutions.  
   - Generates code in **C++** (with comments!) inside markdown blocks for readability.  

4. **Transparent Overlay GUI 🌟**  
   - Displays answers in a **transparent, frameless window** that stays on top without activating.  
   - Dynamically adjusts size to fit content, ensuring no scrollbars or clutter.  

5. **Threaded Execution ⚡**  
   - Runs LLM inference in a separate thread to keep the GUI responsive.  
   - Ensures smooth performance even during heavy AI processing.  

6. **Open Source & Hackable 🛠️**  
   - Public repo: Fork it, tweak it, make it better. We’re here to learn and grow together.  

---

## **How It Works**  

### **Tech Stack**  
- **Python**: The backbone of the project.  
- **OpenCV**: For image capture and processing.  
- **Tesseract OCR**: Extracts text from screenshots.  
- **Google Generative AI**: Provides real-time solutions to coding questions.  
- **PyQt5**: Powers the transparent overlay GUI.  
- **Windows APIs**: Ensures stealth and invisibility to screen-sharing tools.  

---

### **Workflow**  
1. **Region Selection**  
   - The user manually selects a region of the screen using OpenCV's mouse callback.  
   - The selection window is **full-screen**, **undetectable**, and **on top** at all times.  

2. **Screenshot Capture & OCR**  
   - Captures the selected region using `mss`.  
   - Preprocesses the image (grayscale + adaptive thresholding) to enhance OCR accuracy.  
   - Extracts text using Tesseract OCR.  

3. **AI Inference**  
   - Sends the extracted question to Google's `gemini-2.0-flash` model.  
   - Requests a solution in **C++** with necessary comments inside a markdown code block.  

4. **Transparent Overlay Display**  
   - Displays the AI-generated answer in a **transparent, frameless window**.  
   - Dynamically resizes the window to fit the content, ensuring clean visuals.  

---

## **Installation**  

### **Prerequisites**  
1. **Python 3.12+**  
   - Install Python from [here](https://www.python.org/downloads/).  

2. **Tesseract OCR**  
   - Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).  
   - Update the path in `pytesseract.pytesseract.tesseract_cmd` if necessary.  

3. **Google API Key**  
   - Create a `.env` file in the root directory with your Google API key:  
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```  

4. **Dependencies**  
   - Install required libraries:  
     ```bash
     pip install -r requirements.txt
     ```  

---

## **Usage**  

1. Clone the repo:  
   ```bash
   git clone https://github.com/yourusername/CodeBreaker.git
   cd CodeBreaker
   ```  

2. Run the script:  
   ```bash
   python main.py
   ```  

3. Select the region of the screen containing the coding question.  
4. Watch as CodeBreaker extracts the question, processes it, and displays the AI-generated solution in a sleek overlay.  

---


## **Future Plans**  

🚀 **Next-Level Ideas to Explore:(Maybe🤣)**  
- **Packaging into an App**: Convert the script into a standalone application with keybindings for automation.  
- **Multi-Language Support**: Extend AI responses to include Python, Java, JavaScript, etc.  
- **Advanced Stealth**: Experiment with deeper low-level hooks and anti-detection techniques.  
- **Community Contributions**: Add features based on user feedback and contributions.  

---

## **Shoutouts**  

🙏 **Special Thanks to the Homies:**  
- **Roy Lee ([@roy-lee-swe](https://www.linkedin.com/in/roy-lee-swe/))**  
   - his idea sparked this madness—no code copied tho, just vibes borrowed. We don't do that here **Black Panther reference🙌🏻👐🏻**. TRULY GOATED!


---

## **Disclaimer**  

⚠️ **Use Responsibly:**  
CodeBreaker is intended for educational purposes only. Always respect ethical guidelines and terms of service when using automated tools.  

---

## **Contribute**  

🌟 **Wanna Help?**  
- Fork the repo, make improvements, and submit a PR.  
- Report bugs or suggest features via [Issues](https://github.com/RahulEncoded/CodeBreaker/issues).  

Let’s make CodeBreaker **PURE FIRE** 🔥🔥  


*"Still got so much to learn, tbh 😮‍💨. But hey, that’s the fun part, right?"*  

--- 

**Tagline:**  
**"CodeBreaker: Breaking Barriers, Not Rules. ABSOLUTELY UNHINGED BEHAVIOR AND I’M HERE FOR IT!! 🔥🔥"**