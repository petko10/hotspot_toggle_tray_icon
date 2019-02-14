#!/usr/bin/env python

import sys, os, subprocess
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
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


def handleTrayIconClick(reason):
    if reason != QSystemTrayIcon.Context:
        toggleHotspot()


def main():
    basePath = os.path.dirname(os.path.realpath(__file__))
    app = QApplication(sys.argv)
    contextMenu = QMenu()
    fixAction = QAction("Run 'create__ap --fix-unmanaged' in the terminal as root to fix possible issues")
    contextMenu.addAction(fixAction)
    activeIcon = QIcon()
    activeIcon.addFile(os.path.join(basePath, "wifi.svg"))
    inactiveIcon = QIcon()
    inactiveIcon.addFile(os.path.join(basePath, "wifi-off.svg"))
    trayIcon = QSystemTrayIcon(inactiveIcon)
    trayIcon.setContextMenu(contextMenu)
    trayIcon.activated.connect(handleTrayIconClick)

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
