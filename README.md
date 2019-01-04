# Hotspot toggle tray icon
This script creates a tray icon that shows whether your wireless connection is in hotspot mode or not. When you click on it - the app toggles the hotspot config.
### How does it work? Dependencies
I wrote the app, because the built in settings in KDE couldn't activate my wireless adapter as a hotspot properly (some WPA shenanigans), but [create_ap](https://github.com/oblique/create_ap) could. So I wanted to have a GUI for that.

In Arch based distros create_ap comes with a systemd service unit (sorry, I haven't tested other distros). This extension just polls the state of the create_ap service every second and changes the icon respectively. On click it either starts and enables or stops and disables the create_ap service (that's why you will get two password prompts). I found no simple and safe solution to let the app work without a password prompt.

I use the Qt library (PySide2 = Qt python bindings), so you need to have python and pyside2 installed.

After you install create_ap it's preferable that you test it in the terminal. You'll probably need to edit /etc/create_ap.conf with your ethernet and wifi adapter names (terminal:"ip addr" or "ifconfig"), as well as a name (SSID) and password for the hotspot. [Here's the Arch wiki for reference.](/etc/create_ap.conf)

In order to start the indicator on boot you can add it as an autostart entry. In KDE there's Autostart in the settings, in GNOME - via Tweak tools. To do it yourself you can use Arronax.

If anyone wants to package the script or add features I'd be happy to collaborate.