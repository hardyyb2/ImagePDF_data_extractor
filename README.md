# PDF Data Extractor

PDF data extractor can be used to extract any kind of required data from image based PDFs.

**Current Purpose** - Currently it is being used to extract phone numbers from the PDFs.

## SETUP

### All steps should be followed from project root :

- Install latest _Python_ release (3.9.5 at the time of writing).  
  [Download Python](https://www.python.org/downloads/)
- Add _Python_ to your system path if on windows  
  [Add to Path ](https://www.educative.io/edpresso/how-to-add-python-to-path-variable-in-windows)
- Install _pip_
  - [Windows](https://phoenixnap.com/kb/install-pip-windows)
  - [Mac](https://stackoverflow.com/questions/17271319/how-do-i-install-pip-on-macos-or-os-x)
- Install virtualenv with  
   `pip install virtualenv`
- Create a virtual env in the project root with  
  `virtualenv env`
- Install all dependencies with  
  `pip install -r requirements.txt`
- Install _tesseract_ on your system
  - [Windows](https://stackoverflow.com/questions/46140485/tesseract-installation-in-windows)
  - `brew install tesseract` on Mac

## GET STARTED

- After installing all the dependencies activate the virtual enviroment with
  - `source env/bin/activate` on Mac
  - `env\Scripts\activate` on Windows
- After activation, in the command line enter  
  `export FLASK_APP=app` and `export FLASK_ENV=development`
- Now run with  
  `flask run`
- Server runs at `localhost:5000`

## HOW TO USE

- Once the server is running on `localhost:5000`, open in browser, upload the PDF and submit.
  > Average time - 1 min/mb (PDF file)
- Alternatively, send a **HTTP POST** request to **/phonenumbers** with _form-data_ field named _'file'_ and attach the PDF to it.

## HOW IT WORKS

- The given PDF is scanned and converted to **png** images using **PyMuPDF** library.
- These images are then evaluated with **pytesseract** which uses **tesseract-OCR** under the hood to recognize letters from images (OCR technology).
- We then pass the extracted text through our function which filters out phone numbers.

> Various other functions can be used to extract other kinds of data from PDF.
