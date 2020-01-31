# Watermark-app

The app allows to add some watermark on a big number of images.

There are three main .py files:
- watermark_gui5.py (created by PyQt5 UI code generator, includes GUI code)
- wm_app_logic.py (includes watermark adding logic)
- watermark_app5.py (combines the functionality of watermark_gui5.py and wm_app_logic.py)
wm_res_rc.py is the resource file, includes app's Logo. watermark_gui5.ui and wm_res.qrc are Qt Designer originally generated files.
The other files are images of the Logo.

PyQt5 and Qt Designer were used to create GUI and PIL was used for working with images.
The app is able to work with .bmp, .jpeg and .png images. A watermark image must have .jpeg or .png format.
Only four fixed watermark positions are supported yet.

Note: Menu bar allows to toggle between frames: MainFrame, SettingsFrame, InfoFrame. Only MainFrame and InfoFrame are fully operational now. SettingsFrame is worked on.

How to use the app:
- chose a folder which includes images you want to modify (output folder is created by the app automatically);
- chose a file that you want to be a watermark;
- chose the position for the watermark;
- click the process button;
- the progress bar will show you when the process is finished;
- click the open folder button to watch all the modified images.
