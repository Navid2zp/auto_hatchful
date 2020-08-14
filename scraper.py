from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

SPACE_OPTIONS = ["Fashion", "Health and beauty", "Home and garden", "Food and drink", "Sports and rec",
                 "Gifts and collectibles", "Tech", "Art and photos", "Services", "Games", "Children", "Pets",
                 "None of the above"]

VISUAL_STYLES = ["Bold", "Calm", "Reliable", "Classic", "Conservative", "Creative", "Elegant", "Energetic", "Friendly",
                 "Futuristic", "Industrial", "Innovative", "Modern", "Natural", "Strong", "Vintage", "Youthful",
                 "None of the above"]

LOGO_USAGES = ["Online store or website", "Social media", "Print and swag", "Business cards", "Large surfaces",
               "Physical stores"]


class HatchfulScraper:
    def __init__(self, name, slogan=None):
        self.name = name
        self.slogan = slogan
        options = webdriver.ChromeOptions()
        # options.add_argument("--start-maximized")
        options.add_argument(
            '--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1"')
        # Change the driver path if it doesn't match your os or path
        self._browser = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)

    # They detect robots using mouse movements and time spent choosing options
    # This function will do some random mouse movements on elements on the page to avoid detection
    def _random_mouse_movements(self):
        buttons = self._browser.find_elements_by_tag_name("button")
        # Random number of movements
        tries = random.randint(3, 7)
        while tries != 0:
            # Random delays between mouse movements
            random_sleep = random.randint(300, 1500) / 1000
            time.sleep(random_sleep)
            action = ActionChains(self._browser)
            button = random.choice(buttons)
            action.move_to_element(button).perform()
            tries -= 1

    # This function will wait till the given tag with the given task becomes present on the page
    # timeout is the maximum number of tries
    # sleep is the duration of delay
    def _text_based_wait(self, tag, text, timeout, sleep):
        tries = 0
        while tries <= timeout:
            h1 = self._browser.find_element_by_tag_name(tag)
            if text in h1.text:
                return True
            time.sleep(sleep)
        return False

    # Clicks on the next button
    # It's same for every step
    def _click_next(self):
        next_button = self._browser.find_element_by_xpath("//button[contains(text(),'Next')]")
        action = ActionChains(self._browser)
        action.move_to_element(next_button).perform()
        next_button.click()

    # Finds and clicks on the option based on the given text
    def _click_option(self, text):
        final_el = self._find_element_by_text("button", text)
        # You can't click on the button itself
        # Click should be done on parent element
        final_el = final_el.find_element_by_xpath('..')

        # Some options are at the end of the page
        # Scroll down and then try if any exceptions happened
        try:
            action = ActionChains(self._browser)
            time.sleep(0.3)
            action.move_to_element(final_el).perform()
            time.sleep(0.05)
            final_el.click()
        except:
            self._browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            action = ActionChains(self._browser)
            time.sleep(0.3)
            action.move_to_element(final_el).perform()
            time.sleep(0.06)
            final_el.click()

    # Find an element based on the given tag name and text
    def _find_element_by_text(self, tag, text):
        els = self._browser.find_elements_by_tag_name(tag)
        for el in els:
            if text in el.text:
                return el
        raise Exception("couldn't find text element")

    # Loads the entry point for creating a logo
    def _run_browser(self):
        self._browser.get("https://hatchful.shopify.com/onboarding/pick-space")
        # Check if page is loaded properly
        loaded = self._text_based_wait("h1", "Choose your business space", 4, 1)
        if not loaded:
            raise Exception("Page didn't load!")

    # Selects a random space
    def _select_space(self):
        space = random.choice(SPACE_OPTIONS)
        print("Selected space:", space)
        self._click_option(space)
        time.sleep(2)
        self._click_next()
        return space

    # Selects a random visual style
    def _select_visual_style(self):
        style = random.choice(VISUAL_STYLES)
        print("Selected visual style:", style)
        self._click_option(style)
        time.sleep(2)
        self._click_next()
        return style

    # Fills the name and slogan
    def _fill_name_slogan_inputs(self):
        name_field = self._browser.find_element_by_name("businessName")
        name_field.clear()
        for c in self.name:
            name_field.send_keys(c)
            time.sleep(0.012)
        time.sleep(0.32)
        # Slogan is optional
        if self.slogan:
            slogan_field = self._browser.find_element_by_name("slogan")
            slogan_field.clear()
            for c in self.slogan:
                slogan_field.send_keys(c)
                time.sleep(0.01)
        # Wait for form validation
        time.sleep(2)
        self._click_next()

    # Selects a random number of usages
    def _select_usages(self):
        # Number of usages to select
        k = random.randint(0, 6)
        print(k, "random usages")
        # Random usages
        usages = random.sample(LOGO_USAGES, k=k)
        for usage in usages:
            print("Selecting", usage)
            self._click_option(usage)
        time.sleep(0.73)
        self._click_next()

    # Slowly scrolls down to the end of page so all items can be loaded
    def _scroll_down_page(self, speed=9):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self._browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self._browser.execute_script("return document.body.scrollHeight")

    # Selects a random logo at the last step
    def _select_logo(self):
        time.sleep(4)
        self._scroll_down_page()

        buttons = self._browser.find_elements_by_tag_name("button")
        # Number of available logos
        # there are two buttons that are not logos (login and register)
        buttons = buttons[2:]
        selected_logo = random.choice(buttons)
        action = ActionChains(self._browser)
        action.move_to_element(selected_logo).perform()
        print("Selected a random logo")
        selected_logo.click()

    # Screenshot the logo
    def _take_screenshot(self):
        # Maximize the screen to have the largest size possible
        self._browser.maximize_window()
        imgs = self._browser.find_elements_by_tag_name("img")
        if len(imgs) < 2:
            raise Exception("logo didn't load!")
        path = "logos/{0}.png".format(self.name)
        imgs[1].screenshot(path)
        return path

    def create(self):
        self._run_browser()
        self._random_mouse_movements()
        self._select_space()
        time.sleep(0.2)
        self._random_mouse_movements()
        self._select_visual_style()
        time.sleep(0.25)
        self._fill_name_slogan_inputs()
        time.sleep(0.2)
        self._select_usages()
        time.sleep(1)
        self._select_logo()
        time.sleep(1)
        path = self._take_screenshot()
        # Close browser
        self._browser.quit()
        return path
