from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from user import password, username
from PyQt5 import QtWidgets
from _listunfollowers import Ui_MainWindow
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Instagram:
    def __init__(self, username, password):
        self.browserLang = webdriver.FirefoxOptions()
        self.browserLang.set_preference('intl.accept_languages', 'en,en_US')
        self.browser = webdriver.Firefox(options=self.browserLang)
        self.username = username
        self.password = password
        self.followinglist = []
        self.followerlist = []

    def signIn(self):
        url = "https://www.instagram.com/accounts/login/"
        self.browser.get(url)
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(self.username)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(self.password)
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(4)

    def profile(self):
        target_button = self.browser.find_elements(By.CSS_SELECTOR, "._a9-v ._a9-z button")
        for a in target_button:
            if a.text == "Not Now":
                a.click()
        time.sleep(2)
        prf = self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div")
        prf2 = prf.find_elements(By.CSS_SELECTOR,"span")
        for x in prf2:
            if x.text == "Profile":
                x.click()
                break
        time.sleep(3)

    def follower(self):
        countflw = 0
        self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)
        flw = self.browser.find_elements(By.XPATH,"/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div")
        time.sleep(1)
        for follower in flw:
            span_elements = follower.find_elements(By.CSS_SELECTOR, ".x1rg5ohu span")
            for span_element in span_elements:
                countflw+=1
        totalflwcount = countflw
        time.sleep(1)
        while True:
            self.scroll("_aano")
            time.sleep(2)
            for follower in flw:
                span_elements = follower.find_elements(By.CSS_SELECTOR, ".x1rg5ohu span")
            newflwCount = len(span_elements)
            if totalflwcount != newflwCount:
                totalflwcount = newflwCount
                time.sleep(1)
                pass
            else:
                for follower in flw:
                    span_elements = follower.find_elements(By.CSS_SELECTOR, ".x1rg5ohu span")
                    for span_element in span_elements:
                        self.followerlist.append(span_element.text)
                break
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR,"._abl-").click()
        time.sleep(1)

    def following(self):
        self.browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a").click()
        time.sleep(2)
        dialog = self.browser.find_element(By.CSS_SELECTOR,"div[role=dialog] ._aano").find_elements(By.CSS_SELECTOR,".x1rg5ohu span")
        totalcount = len(dialog)
        time.sleep(2)
        while True:
            self.scroll("_aano")
            time.sleep(2)
            dialog2 = self.browser.find_element(By.CSS_SELECTOR, "div[role=dialog] ._aano").find_elements(
                By.CSS_SELECTOR, ".x1rg5ohu span")
            time.sleep(2)
            newCount = len(dialog2)
            if totalcount != newCount:
                totalcount = newCount
                time.sleep(1)
                pass
            else:
                for a in dialog2:
                  self.followinglist.append(a.text)
                break
        time.sleep(1)

    def scroll(self, div_class):
        div_element = self.browser.find_element(By.CLASS_NAME, div_class)
        self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", div_element)

    def match(self):
        not_followed_back = set(self.followinglist) - set(self.followerlist)
        if not_followed_back:
            app = QtWidgets.QApplication(sys.argv)
            win = QtWidgets.QMainWindow()
            win.setGeometry(200, 200, 600, 800)
            win.setWindowIcon(QIcon('flw.png'))
            ui = Ui_MainWindow()
            ui.setupUi(win)
            ui.btnExit.clicked.connect(self.close)
            for user in not_followed_back:
                ui.listItems.addItem(user)
            ui.listItems.setStyleSheet(""" QListWidget::item { height: 30px;  } 
                                        QListWidget::item:hover { background-color: #40A2D8;}""")
            win.setWindowFlags(Qt.WindowStaysOnTopHint)
            win.show()
            sys.exit(app.exec_())
        else:
            print("Everyone you are following is also following you back.")

    def close(self):
        quit()

instagram = Instagram(username,password)
instagram.signIn()
instagram.profile()
instagram.follower()
instagram.following()
instagram.match()