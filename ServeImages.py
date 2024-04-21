import json
import os
import tkinter.filedialog
from functools import lru_cache
from pprint import pprint

import flask
from flask import send_file

allowedFileTypes = [("Exif extracted file in json", ".json")]
Exiffilename = tkinter.filedialog.askopenfilename(filetypes=allowedFileTypes)
print(Exiffilename)

app = flask.Flask(__name__)

dir = tkinter.filedialog.askdirectory()

# Single Directory only mapping
# Multi-directory will be supported soon....
Mappingdict = {}


@lru_cache()
def LoadFiles():
    with open(Exiffilename, "r") as f:
        JSON = json.load(f)
    for data in JSON:
        srcFile = data.get("SourceFile")
        print(f"Lodaded file {srcFile}")
        file = os.path.basename(srcFile)
        Mappingdict.setdefault(file, srcFile)

    pprint(Mappingdict)


LoadFiles()


@app.route("/SumuPhotoLauncher/<file>")
def ServeImage(file):
    dir = Mappingdict.get(file)
    # return f"<H1>{dir}</H1>"
    return send_file(dir)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090)
