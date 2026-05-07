class LoginPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:5000/login")

    def login(self, username="qapm", password="quality123"):
        self.page.get_by_test_id("username").fill(username)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-button").click()
