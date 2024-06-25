from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from instance.db.connect import db, File
import os

file_router = Blueprint("file_router", __name__)

# 配置上传文件的目录
UPLOAD_FOLDER = "var/static/uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "vpsw"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@file_router.route("/upload", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"code": 400, "msg": "没有上传文件"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"code": 400, "msg": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename if file.filename else "空的文件名")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # 记录文件元数据到数据库
        new_file = File(
            filename=filename, upload_time=datetime.utcnow(), user_id=get_jwt_identity()
        )
        db.session.add(new_file)
        db.session.commit()
        return (
            jsonify(
                {"code": 200, "msg": "File uploaded successfully", "filename": filename}
            ),
            200,
        )
    else:
        return jsonify({"code": 400, "msg": "File type not allowed"}), 400


@file_router.route("/files", methods=["GET"])
@jwt_required()
def get_files():
    user_id = get_jwt_identity()
    files = File.query.filter_by(user_id=user_id).all()
    if not files:
        return jsonify({"code": 404, "msg": "没有找到文件"}), 404
    files_data = [
        {"id": file.id, "filename": file.filename, "upload_time": file.upload_time}
        for file in files
    ]
    return jsonify({"code": 200, "files": files_data}), 200
