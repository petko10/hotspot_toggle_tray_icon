#!/usr/bin/env python

import sys, os, subprocess
from PySide2.QtWidgets import QApplication, QSystemTrayIcon
from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon


def serviceIsActive():
    status = subprocess.getoutput("systemctl is-active create_ap")
    if status == "active":
        return True
    else:
        return False


def toggleHotspot():
    if serviceIsActive():
        subprocess.call(["systemctl", "disable", "create_ap"])
        subprocess.call(["systemctl", "stop", "create_ap"])
    else:
        subprocess.call(["systemctl", "enable", "create_ap"])
        subprocess.call(["systemctl", "start", "create_ap"])


def main():
    basePath = os.path.dirname(os.path.realpath(__file__))
    app = QApplication(sys.argv)
    activeIcon = QIcon()
    activeIcon.addFile(os.path.join(basePath, "wifi.svg"))
    inactiveIcon = QIcon()
    inactiveIcon.addFile(os.path.join(basePath, "wifi-off.svg"))
    trayIcon = QSystemTrayIcon(inactiveIcon)
    trayIcon.activated.connect(toggleHotspot)

    def syncIcon():
        if serviceIsActive():
            trayIcon.setIcon(activeIcon)
        else:
            trayIcon.setIcon(inactiveIcon)

    timer = QTimer()
    timer.setInterval(1000)
    timer.timeout.connect(syncIcon)
    timer.start()
    trayIcon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
