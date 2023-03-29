from PyQt5.QtCore import QThread
import timeit, time
from PyQt5.QtTest import QTest

class UiUpdate(QThread):
    def __init__(self, parent):
        super(UiUpdate, self).__init__(parent)
        self.daemon = True
        self.run_stop = True

        self.paint = parent
        self.prev_time = 0
        self.FPS = 15

    def run(self):
        while self.run_stop:

            current_time = timeit.default_timer() - self.prev_time
            if (current_time > 1. / self.FPS):
                self.paint.set_img_Go()
                # FPS = int(1. / current_time)
                # print(FPS)
                self.prev_time = timeit.default_timer()

            QTest.qWait(100)