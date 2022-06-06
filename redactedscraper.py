from chromedriver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import sys

base_url = "https://[INSERT URL HERE]/0:"
timeout = 30
driver = get_driver() #wanted to initialize driver in main, but it meant it would've had to have been passed through every function

class AnyEc: #https://stackoverflow.com/questions/16462177/selenium-expected-conditions-possible-to-use-or
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                res = fn(driver)
                if res:
                    return True
                    # Or return res if you need the element found
            except:
                pass

def scrape_layered_folder(prev_index):
	WebDriverWait(driver, timeout).until(AnyEc( \
	ec.presence_of_element_located((By.XPATH,"//div[@id='list']/div/a")), \
	ec.presence_of_element_located((By.XPATH,"//div[@id='list']/a"))))
	
	files_layered = driver.find_elements(By.XPATH, "//div[@id='list']/div")
	for file_layered in files_layered:
		link = file_layered.find_element(By.XPATH, "./a[1]").get_attribute("href")
		print(link)
	
	folders_layered = driver.find_elements(By.XPATH, "//div[@id='list']/a")
	for folder_layered in folders_layered:
		curr_index=driver.window_handles.index(driver.current_window_handle)
		folder_layered.send_keys(Keys.CONTROL + Keys.ENTER)
		driver.switch_to.window(driver.window_handles[curr_index+1])
		scrape_layered_folder(curr_index)
	
	driver.close()
	driver.switch_to.window(driver.window_handles[prev_index])

def search():
	try:
		orig_url = base_url + "search?q="
		url = orig_url
		for arg in sys.argv[2:]:
			if (url == orig_url): url = url + arg
			else: url = url + "%20" + arg #adds space for args after other args
		driver.get(url)
		WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH,'//div[2]/a')))
		layer_one = driver.find_elements(by=By.XPATH, value='//div[2]/a')
		for item_one in layer_one:
			if (item_one.get_attribute("gd-type") is None):
				item_one.click()
				WebDriverWait(driver, timeout).until(ec.presence_of_element_located((By.XPATH,"//a[contains(text(),'Open')]")))
				driver.find_element(by=By.XPATH, value="//a[contains(text(),'Open')]").send_keys(Keys.CONTROL + Keys.ENTER)
				curr_index=driver.window_handles.index(driver.current_window_handle)
				driver.switch_to.window(driver.window_handles[1])
				scrape_layered_folder(curr_index)
			else: #scrape files
				break #to be coded
			driver.find_element(by=By.CSS_SELECTOR, value='button.btn-close').click()
	except Exception as e: print(e)
	


def home():
	try:
		driver.get(base_url + "/")
		home_index=driver.window_handles.index(driver.current_window_handle)
		scrape_layered_folder(home_index) #home acts like a layered folder in search, I coded this after it so it will be treated as such
	except Exception as e: print(e)
	
def main():
	usage = "Usage:\n- Search (Example: \"python redactedscraper.py search Infinity War\")\n- Home (Example: \"python redactedscraper.py home\")\n"
	if((len(sys.argv) == 1)): 
		print(usage)
		quit()
	if((sys.argv[1] != "home") and (sys.argv[1] != "search")): 
		print(usage)
	else:
		if(sys.argv[1] == "home"): home()
		elif(sys.argv[1] == "search"): search()
	
main()
driver.quit()
