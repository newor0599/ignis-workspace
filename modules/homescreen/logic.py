from ignis.variable import Variable
from ignis.utils import Utils
import datetime


class DATA:
    def __init__(self):
        self.time = Variable(value="")
        self.day = Variable(value="")
        self.update_time()
        Utils.Poll(timeout=1000 * 20, callback=lambda x: self.update_time())

    def update_time(self):
        self.day.value = datetime.date.today().strftime("%A").upper()
        self.time.value = datetime.datetime.now().strftime("%H%M")
