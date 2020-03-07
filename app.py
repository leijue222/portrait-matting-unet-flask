# -*- coding:utf-8 -*-
import os
import re
import flask
from PIL import Image

from web.flask_config import input_path, output_path, bg_path
from web.flask_utils import change_channels_to_rgb, merge_image_name, tid_maker
from web.matting import process

app = flask.Flask(__name__)
model = None
use_gpu = False


def segmentation(image_path):
    names = re.findall(r'[^\\/:*?"<>|\r\n]+$', image_path)
    mask_path = output_path + names[0]
    change_channels_to_rgb(image_path)
    cmd_predict = "python predict.py -i {0} -o {1}".format(image_path, mask_path)
    os.system(cmd_predict)
    mask = Image.open(mask_path)
    img = Image.open(image_path)
    if mask.size != img.size:
        w, h = img.size
        mask = mask.resize((w, h))
        mask.save(mask_path)
    return mask_path


@app.route("/api/wechat/upload", methods=["POST"])
def upload():
    data = {"success": False}
    file = flask.request.files['file']
    file_type = flask.request.form.get("type", type=str)
    file_name = file_type + tid_maker() + '.png'
    file_path = './static/' + file_type + '/' + file_name
    file.save(file_path)
    file_photo = file_type + "/" + file_name + '.png'
    data["filePath"] = flask.url_for('static', _external=True, filename=file_photo)
    data["fileName"] = file_name
    data["success"] = True
    return flask.jsonify(data)


@app.route("/api/wechat/matting", methods=["POST"])
def wechat_matting():
    data = {"success": False}
    im_name = flask.request.form.get("im", type=str)
    bg_name = flask.request.form.get("bg", type=str)
    im_path = input_path + im_name
    segmentation(im_path)
    process(im_name, bg_name)

    merge_name = merge_image_name(im_name, bg_name) + '-merge.png'
    merge_photo = "merge/" + merge_name
    data["result"] = flask.url_for('static', _external=True, filename=merge_photo)
    data["success"] = True
    return flask.jsonify(data)


@app.route("/api/seg", methods=["POST"])
def seg():
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            input_image = flask.request.files['image']
            file_name = input_image.filename
            image_path = input_path + file_name
            input_image.save(image_path)
            segmentation(image_path)

            in_photo = "input/" + file_name
            data["upload"] = flask.url_for('static', _external=True, filename=in_photo)
            out_photo = "output/" + file_name
            data["result"] = flask.url_for('static', _external=True, filename=out_photo)
            data["success"] = True
    return flask.jsonify(data)



@app.route("/api/matting", methods=["POST"])
def matting():
    data = {"success": False}
    print("files:", flask.request.files)
    bg_image = flask.request.files['bg']
    im_image = flask.request.files['im']
    bg_name = bg_image.filename
    im_name = im_image.filename
    im_path = input_path + im_name
    bg_image.save(bg_path + bg_name)
    im_image.save(im_path)

    segmentation(im_path)
    process(im_name, bg_name)

    merge_name = merge_image_name(im_name, bg_name) + '-merge.png'
    merge_photo = "merge/" + merge_name
    data["result"] = flask.url_for('static', _external=True, filename=merge_photo)
    data["success"] = True
    return flask.jsonify(data)


@app.route("/api/clean", methods=["POST"])
def clean():
    data = {"success": False}
    minutes = flask.request.form.get("minutes", type=str, default=30)
    if flask.request.method == "POST":
        cmd_in = "find ./static/input/ -type f -mmin +" + minutes + " -exec rm {} \;"
        cmd_out = "find ./static/output/ -type f -mmin +" + minutes + " -exec rm {} \;"
        cmd_bg = "find ./static/bg/ -type f -mmin +" + minutes + " -exec rm {} \;"
        cmd_merge = "find ./static/merge/ -type f -mmin +" + minutes + " -exec rm {} \;"
        os.system(cmd_in)
        os.system(cmd_out)
        os.system(cmd_bg)
        os.system(cmd_merge)
        data["success"] = True
    return flask.jsonify(data)


if __name__ == '__main__':
    # im_name = '2.jpg'
    # bg_name = 'bg3.jpg'
    # img, alpha, fg, bg = process(im_name, bg_name)
    app.run(host='127.0.0.1', port=5000)
