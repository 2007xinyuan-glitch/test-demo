"""
儿童识字小报生成器 - Web 服务器
"""

import os
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from generator import generate_prompt, SCENE_VOCABULARY
from api_client import JimengClient, save_images

app = Flask(__name__)
CORS(app)

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)


@app.route("/api/scenes", methods=["GET"])
def list_scenes():
    """获取支持的场景列表"""
    return jsonify({
        "scenes": list(SCENE_VOCABULARY.keys())
    })


@app.route("/api/generate-prompt", methods=["POST"])
def gen_prompt():
    """生成提示词"""
    data = request.json
    scene = data.get("scene", "")
    title = data.get("title", "")

    if not scene:
        return jsonify({"error": "缺少 scene 参数"}), 400

    if not title:
        title = f"走进{scene}"

    prompt = generate_prompt(scene, title)
    return jsonify({
        "scene": scene,
        "title": title,
        "prompt": prompt
    })


@app.route("/api/generate-image", methods=["POST"])
def gen_image():
    """生成图片"""
    data = request.json
    scene = data.get("scene", "")
    title = data.get("title", "")
    api_key = data.get("api_key", "") or os.getenv("JIMENG_API_KEY", "")
    model = data.get("model", "doubao-seedream-4-5-251128")
    size = data.get("size", "1600x2848")

    if not api_key:
        return jsonify({"error": "缺少 api_key"}), 400
    if not scene:
        return jsonify({"error": "缺少 scene"}), 400

    if not title:
        title = f"走进{scene}"

    # 生成提示词
    prompt = generate_prompt(scene, title)

    # 调用 API
    try:
        client = JimengClient(api_key=api_key)
        result = client.generate_image(
            prompt=prompt,
            model=model,
            size=size,
            watermark=False
        )

        # 保存图片
        saved = save_images(result, "./output")

        return jsonify({
            "success": True,
            "images": saved,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/images/<filename>")
def get_image(filename):
    """获取生成的图片"""
    return send_file(f"output/{filename}")


@app.route("/")
def index():
    return send_file("templates/index.html")


if __name__ == "__main__":
    print("=" * 50)
    print("儿童识字小报生成器 API 服务器")
    print("=" * 50)
    print("访问 http://localhost:5000")
    print("API 文档: http://localhost:5000/")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)
