from flask import jsonify, current_app as app
from PIL import Image
import pytesseract
from pathlib import Path
import shutil
import os
import fitz


# Path for images
image_save_dir = Path("images")

# split the text and find digits with length = 10
def filter_numbers(txt):
    return [str(s) for s in txt.split() if s.isdigit() and len(s) == 10]


def extract_phone_numbers(PDF_file):
    app.logger.info("Process Started...")

    try:
        doc = fitz.open(PDF_file)
        # pages = convert_from_path(PDF_file, 500)
    except Exception as e:
        err = "Failed to Convert File to images, Error: " + str(e)
        app.logger.error(err)
        return err
    finally:
        image_counter = 1

    for pg in range(doc.pageCount):
        app.logger.info("Creating Image for Page = " + str(image_counter))
        # Save the image of the page in system
        image_save_dir.mkdir(exist_ok=True)

        try:
            page = doc[pg]
            rotate = int(0)
            zoom_x = 1.33333333
            zoom_y = 1.33333333
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            pix.writePNG(image_save_dir / f"page_{image_counter}.png")
        except Exception as e:
            err = f"Failed to save image : {image_counter}, Error : {str(e)}"
            app.logger.error(err)
            return err

        image_counter = image_counter + 1

    # get count of total number of pages
    doc.close()
    filelimit = image_counter - 1

    result = []

    for i in range(1, filelimit + 1):
        filename = image_save_dir / f"page_{i}.png"
        # Recognize the text as string in image using pytesserct

        try:
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace("-\n", "")
            filtered_numbers = filter_numbers(text)

            app.logger.info("Filtering numbers for Page = " + str(i))
            for v in filtered_numbers:
                result.append(int(v))
        except Exception as e:
            err = "Failed to extract string" + str(e)
            app.logger.warning(err)

    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        app.logger.info("Deleting Images...")
        shutil.rmtree(image_save_dir)
    except OSError as e:
        app.logger.error(
            "Failed to delete Images folder, Error: %s - %s." % (e.filename, e.strerror)
        )

    try:
        app.logger.info("Deleting PDF")
        os.remove(PDF_file)
    except OSError as e:
        app.logger.error(
            "Failed to delete PDFs , Error: %s - %s." % (e.filename, e.strerror)
        )

    app.logger.info("Process Complete...")

    return result
