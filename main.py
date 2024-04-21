import json
import os
import re
import sys
from functools import lru_cache
from pprint import pprint
from tkinter.filedialog import askopenfilename
import flask
from flask import request, jsonify, url_for
from dms2dec.dms_convert import dms2dec
import geocoder
from flask import render_template, redirect

allowedFileTypes = [("Exif extracted file in json", ".json")]
Exiffilename = askopenfilename(filetypes=allowedFileTypes)
print(Exiffilename)

if Exiffilename == "":
    sys.exit(1)

app = flask.Flask(__name__)

GetImages = []


@lru_cache()
def GetCurrentLocation():
    currLoc = geocoder.ip('me')
    print(currLoc.latlng)
    return currLoc.latlng


@lru_cache()
def ParseExifJson():
    OUT = []
    with open(Exiffilename, "r") as f:
        JSON = json.load(f)
        for data in JSON:
            try:
                if data.get("SourceFile") and data.get("GPSPosition"):
                    name = data.get("SourceFile")
                    print(name)
                    unformattedloc = data.get("GPSPosition")
                    latlangDMS = unformattedloc.split(",")
                    DMSMatchPattern = r"(.*) deg (.*)' (.*)\" ([A-Z])"
                    matchReLat = re.match(DMSMatchPattern, latlangDMS[0], re.MULTILINE)
                    latdeg = matchReLat.group(0)
                    latmin = matchReLat.group(1)
                    latsec = matchReLat.group(2)
                    latdir = matchReLat.group(3)
                    matchReLong = re.match(DMSMatchPattern, latlangDMS[1], re.MULTILINE)
                    longdeg = matchReLong.group(0)
                    longmin = matchReLong.group(1)
                    longsec = matchReLong.group(2)
                    longdir = matchReLong.group(3)
                    latiDD = dms2dec(f"""{latdeg}°{latmin}'{latsec}"{latdir}""")
                    LongiDD = dms2dec(f"""{longdeg}°{longmin}'{longsec}"{longdir}""")
                    print(latiDD, LongiDD)
                    OUT.append([latiDD, LongiDD])
            except Exception as e:
                print("ERROR:\n", e)
        return OUT


@lru_cache()
def ParseExifJsonWithName():
    OUT = []
    NameList = []
    with open(Exiffilename, "r") as f:
        JSON = json.load(f)
        for data in JSON:
            try:
                if data.get("SourceFile") and data.get("GPSPosition"):
                    name = data.get("SourceFile")
                    print(name)
                    unformattedloc = data.get("GPSPosition")
                    latlangDMS = unformattedloc.split(",")
                    DMSMatchPattern = r"(.*) deg (.*)' (.*)\" ([A-Z])"
                    matchReLat = re.match(DMSMatchPattern, latlangDMS[0], re.MULTILINE)
                    latdeg = matchReLat.group(0)
                    latmin = matchReLat.group(1)
                    latsec = matchReLat.group(2)
                    latdir = matchReLat.group(3)
                    matchReLong = re.match(DMSMatchPattern, latlangDMS[1], re.MULTILINE)
                    longdeg = matchReLong.group(0)
                    longmin = matchReLong.group(1)
                    longsec = matchReLong.group(2)
                    longdir = matchReLong.group(3)
                    latiDD = dms2dec(f"""{latdeg}°{latmin}'{latsec}"{latdir}""")
                    LongiDD = dms2dec(f"""{longdeg}°{longmin}'{longsec}"{longdir}""")
                    print(latiDD, LongiDD)
                    OUT.append([latiDD, LongiDD])
                    NameList.append(name)
            except Exception as e:
                print("ERROR:\n", e)
        return OUT, NameList


def GetImagesWithin(KM, latlanrcvd: list):
    dist = 0.0090437173 * KM
    filterlatlow = latlanrcvd[0] - dist
    filterlanglow = latlanrcvd[1] - dist
    filterlathigh = latlanrcvd[0] + dist
    filterlanghigh = latlanrcvd[1] + dist
    AllLatLanglist, NameList = ParseExifJsonWithName()
    filteredLatLang = []
    for indx, ll in enumerate(AllLatLanglist):
        if ll[0] > filterlatlow and ll[0] < filterlathigh and ll[1] < filterlanghigh and ll[1] > filterlanglow:
            filteredLatLang.append({"LatLng": ll, "Name": NameList[indx]})
    pprint(filteredLatLang)
    print(len(filteredLatLang))
    return filteredLatLang


@app.route("/")
def ServeMap():
    CurrLatLang = GetCurrentLocation()
    LatLangImage = ParseExifJson()
    return render_template("index.html", LatLang=CurrLatLang, ImagesLatLang=LatLangImage)


@app.route("/viewer")
def Viewer():
    global GetImages
    return render_template("imageGall.html", AllIImagesList=GetImages)


# 4 points method ?
# Do it 4 more times
@app.route("/Photos", methods=["POST"])
def ShowPhotos():
    global GetImages
    if request.method == "POST":
        latLang = request.get_json()["latlang"]
        print(latLang)
        clickedLat = latLang.get('lat')
        clickedLng = latLang.get('lng')
        sendLL = []
        sendLL.append(float(clickedLat))
        sendLL.append(float(clickedLng))
        filteredLatLngNames = GetImagesWithin(1, sendLL)
        print(filteredLatLngNames)
        GetImages = []
        for pic in filteredLatLngNames:
            GetImages.append(os.path.basename(pic.get("Name")))
        return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
