from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
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


@file_router.route("/files/info", methods=["GET"])
@jwt_required()
def get_files():
    user_id = get_jwt_identity()
    files = File.query.filter_by(user_id=user_id).all()
    if not files:
        return jsonify({"code": 404, "msg": "没有找到文件"}), 404
    files_data = [
        {
            "id": file.id,
            "filename": file.filename,
            "upload_time": file.formatted_upload_time(),
        }
        for file in files
    ]
    return jsonify({"code": 200, "files": files_data}), 200


@file_router.route("/download/<int:file_id>", methods=["GET"])
@jwt_required()
def download_file(file_id):
    """
    下载文件

    该函数用于处理下载文件的请求。根据提供的文件ID和用户ID，从数据库中查询对应的文件信息。如果文件不存在，则返回404状态码和相应的错误消息。如果文件存在，则返回文件的下载链接。

    参数:
        file_id (int): 文件的ID。

    返回:
        flask.Response: 文件的下载响应。

    """
    user_id = get_jwt_identity()
    file = File.query.filter_by(id=file_id, user_id=user_id).first()
    if not file:
        return jsonify({"code": 404, "msg": "文件未找到"}), 404
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"code": 404, "msg": "文件未找到"}), 404
