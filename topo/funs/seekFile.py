"""
Mongo Database APIs
"""


import json
import re
import time

import pymongo


def seekFile(fileName):
    """
    Get a dict by filename from Mongodb Data Server

    :param fileName: 文件名，无需路径
    :return: dict
    """
    client = pymongo.MongoClient(host='soowin.icu', port=27017)

    db = client.topos
    db.authenticate("topouser1", "123456")
    collection = db.jsonfiles
    result = collection.find_one({"fileName": fileName})
    client.close()
    if result == None: return None
    else: return result["fileRaw"]


def uploadFile(fileObj):
    fs = str(fileObj.read(), encoding="utf-8")
    try:
        fileRawData = json.loads(fs)
    except json.decoder.JSONDecodeError:
        fileRawData = fs
    newFileDict = {
        "fileRaw": fileRawData,
        "fileVersion": "v1",
        "fileName": re.search('filename="(.*)"', fileObj.headers.get("Content-Disposition")).group(1)
    }

    if seekFile(newFileDict["fileName"]) == None:

        client = pymongo.MongoClient(host='soowin.icu', port=27017)

        db = client.topos
        db.authenticate("topouser1", "123456")
        collection = db.jsonfiles
        result = collection.insert_one(newFileDict)
        client.close()

        return newFileDict["fileName"]

    else: return newFileDict["fileName"]

def uploadFileWithName(fileObj, fileName):

    newFileDict = {
        "fileRaw": fileObj,
        "fileVersion": "v1",
        "fileName": fileName
    }
    client = pymongo.MongoClient(host='soowin.icu', port=27017)

    db = client.topos
    db.authenticate("topouser1", "123456")
    collection = db.jsonfiles
    collection.insert_one(newFileDict)
    client.close()


def fileHistroy() -> str:
    fh = ""
    client = pymongo.MongoClient(host='soowin.icu', port=27017)

    db = client.topos
    db.authenticate("topouser1", "123456")
    collection = db.jsonfiles
    result = collection.find()
    for i in result:
        thisname = i["fileName"]
        if thisname.endswith(".txt.json") or thisname.endswith(".gml.json"):
            continue
        fh = fh + "<option>" + thisname + "</option>"
    client.close()
    return fh


if __name__ == '__main__':
    f = seekFile("topo.json")
    print(type(f))
