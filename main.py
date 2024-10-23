import glob
import os
import time
from io import BytesIO

from PIL import Image
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

x = 1300
y = 1200
off = 160

try:
    print("Drivers initialization")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={x},{y}")

    # Use Service for executable_path management
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

except Exception as e:
    print(f"Driver Error: {e}")
    exit(1)

print("Driver initialized!")

# URL = 'https://international.scholarvox.com/reader/docid/88865376/page/'
URL = 'https://ofppt.scholarvox.com/reader/docid/88880131/page/1?searchterm=intelligence'
# pdf = FPDF(unit="pt", format=(x - 2 * off + 20, y + 50))
pdf = FPDF(unit="pt")
pdf.set_auto_page_break(0)

try:
    for i in range(1, 10):
        dir = "output"
        name = f"output/images/page{i}.png"
        # print(f"Starting {name}")
        
        driver.get(URL + str(i))
        # time.sleep(1.5)
        
        # Capture screenshot and process image
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        output_img = im.crop((off, 0, x - off - 40, y))
        output_img.save(name)
        
        # Add to PDF
        pdf.add_page()
        pdf.image(name)
        
        print(f"{name.split('.')[0]} done!")
    
    pdf.output("output/pdfs/output.pdf")
    driver.quit()
    
    # delete the screenshots
    for file in glob.glob("output/images/page*.png"):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting {file}: {e}")
    
except Exception as e:
    print(f"Error encountered: {e}")
    driver.quit()
