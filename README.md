## Your-Photos-On-Openstreetmap (Leaflet.js)

Description
-----
This  application allows users to explore photos based on their geographic location captured through EXIF metadata. It leverages a two-flask app backend architecture:

Image Server: Manages image storage, retrieval, and delivery.
Map Server: Powers the interactive map using OpenStreetMap and Leaflet.js.
The JavaScript frontend facilitates user interaction and communication with the backend.

Technologies
----
* Frontend: JavaScript
* Backend: Python (Flask)
* Maps: OpenStreetMap, Leaflet.js
* EXIF Metadata Processing: exiftool (binary)

Requirements
-----
* Python 3.x (https://www.python.org/downloads/)
* Flask (https://flask.palletsprojects.com/)
* exiftool (download instructions at https://packages.debian.org/exiftool)

Install Dependencies:
----
Bash
pip install -r requirements.txt
Configure EXIFTool Path:


``` shell
exiftool.exe -json <folder path>
```

``` Bash
python main.py
python ServeImages.py
```
Usage

Access the application in your web browser at the http://localhost:5000. The interface should display a map and allow users to query for photos based on location:

Zoom and Pan: Navigate the map to the desired area of interest.
Query: You can click in a location on map and view the images http://localhost:5000/viewer

Any questions/bugs/want to contribute please feel free :)