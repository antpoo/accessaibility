# AccessAIbility

Accessibility problems while using your computer? We got you! Use ASL signs and hand gestures to interact with your keyboard, your right index finger as cursor, and use your head to click and scroll.


## Requirements

You must use [Python](https://www.python.org/downloads/) version 3.12 as certain libraries only work with that.


## Installation

Open a terminal in the folder you want to install the program in and enter the following commands:
```
git clone https://github.com/antpoo/accessaibility.git
cd accessaibility
python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt
```

Next, run app.py with the following:
```
python app.py
```
Wait for it to load and it should launch the GUI window with options for configuration. At this point, all the features are already running. Close the GUI window in order to exit the program.


## Usage

Keyboard:
- Left hand
- American Sign Language for typing letters
- Enter: I Love You 
- Caps Lock: Open Palm
- Space: Thumbs Up
- Backspace: Thumbs Down.

Mouse:
- Index finger on right hand moves cursor
- Open mouth for left click
- Lift your head up for right click
- Turn your head left to scroll down
- Turn your head right to scroll up


## Configuration

You can customize your settings in the GUI window so that it best suits your needs.
- Left hold threshold: distance your mouth has to open to register as left click
- Right hold threshold: distance your head has to tilt up to register as right click
- Hold: when set to True, will press down the key and hold it for as long as you hold up the sign. When set to False, will press and release the key, and if you want to press it again, you must change to some other/no gesture first


## Troubleshooting

For the letters J and Z, try pointing to the side.

If left click or right click isn't working as desired, try moving closer or farther to the camera.
