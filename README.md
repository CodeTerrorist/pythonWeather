AppMetereologia - Documentation

Description:
------------
AppMetereologia is a desktop application developed in Python using PyQt5, which allows users to check weather and air quality information for any city in the world, using the OpenWeatherMap API.

Features:
---------
- Current temperature and "feels like" temperature.
- Weather emoji representation.
- Textual weather description (e.g., "clear sky", "light rain").
- Display of relative humidity.
- Wind speed and direction (in km/h and cardinal points).
- Precipitation information (rain or snow).
- Air quality display (from "Good" to "Hazardous").
- User-friendly and responsive graphical interface.

How to use:
-----------
1. Run the `main.py` file.
2. Enter the desired city name in the text field.
3. Click the "Pesquisar" (Search) button.
4. Weather and air quality information will be displayed on the screen.

Requirements:
-------------
- Python 3.x
- PyQt5
- requests

Installing dependencies:
------------------------
pip install PyQt5 requests

API:
----
The application uses the OpenWeatherMap API to obtain weather and air quality data. You need a valid API key, which is already set in the code.

Error handling:
---------------
The application handles various connection and API response errors, displaying user-friendly messages in case of issues such as city not found, invalid API key, server unavailable, and others.

Customization:
--------------
The layout and interface colors can be changed directly in the `UI()` method of the `AppMetereologia` class, where the stylesheet is defined.

