"""
Integration test using Selenium for the NetCDF uploader page.
This test will:
1. Open the browser.
2. Navigate to the upload page.
3. Upload a sample NetCDF file.
4. Select a variable and time step (if applicable).
5. Check that the heatmap plot is generated.
"""

import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Path to a sample NetCDF file for testing
SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample_4d.nc")

class NetCDFUploaderIntegrationTest(unittest.TestCase):
    def setUp(self):
        # Setup Chrome driver using webdriver_manager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)  # Wait up to 5s for elements to appear

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_upload_and_plot(self):
        driver = self.driver

        # Navigate to the upload page
        driver.get("http://localhost:8000/")

        # Find the file input element and upload a file
        file_input = driver.find_element(By.NAME, "file")
        file_input.send_keys(SAMPLE_FILE)

        # Click the submit button
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()

        # Wait a few seconds for the page to reload and plot to render
        time.sleep(3)

        # Optionally, select a variable if dropdown exists
        try:
            var_select = Select(driver.find_element(By.NAME, "variable"))
            var_select.select_by_index(0)  # select first variable
        except:
            pass  # If no dropdown, skip

        # Optionally, select a time step
        try:
            time_input = driver.find_element(By.NAME, "time_idx")
            time_input.clear()
            time_input.send_keys("0")  # first time step
        except:
            pass

        # Click "Update" button to generate plot if needed
        try:
            update_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            update_btn.click()
            time.sleep(3)
        except:
            pass

        # Check that the Plotly heatmap div exists
        plot_div = driver.find_element(By.CLASS_NAME, "js-plotly-plot")
        self.assertIsNotNone(plot_div, "Plotly plot did not render!")

if __name__ == "__main__":
    unittest.main()

