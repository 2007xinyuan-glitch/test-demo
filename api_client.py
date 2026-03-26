"""
即梦/Seedream 图片生成 API 客户端
"""

import requests
import json
import os
from typing import Optional, List


class JimengClient:
    """即梦 API 客户端"""

    def __init__(self, api_key: str = None, endpoint: str = None):
        """
        初始化客户端

        Args:
            api_key: API密钥，不传则从环境变量 JIMENG_API_KEY 读取
            endpoint: API端点，不传则使用默认值
        """
        self.api_key = api_key or os.getenv("JIMENG_API_KEY")
        if not self.api_key:
            raise ValueError("请提供 API Key，或设置环境变量 JIMENG_API_KEY")

        self.endpoint = endpoint or "https://ark.cn-beijing.volces.com/api/v3/images/generations"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt: str,
        model: str = "doubao-seedream-4-5-251128",
        size: str = "2K",
        response_format: str = "url",
        watermark: bool = True,
        **kwargs
    ) -> dict:
        """
        生成单张图片

        Args:
            prompt: 提示词
            model: 模型名称
            size: 图片尺寸 (2K/4K 或 像素如 1600x2848)
            response_format: 返回格式 (url/b64_json)
            watermark: 是否添加水印

        Returns:
            API 响应结果
        """
        data = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "response_format": response_format,
            "watermark": watermark,
            "sequential_image_generation": "disabled",
            "stream": False
        }

        # 添加可选参数
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=data,
            timeout=120
        )

        result = response.json()

        if "error" in result:
            raise Exception(f"API 错误: {result['error']['code']} - {result['error']['message']}")

        return result

    def generate_images(
        self,
        prompt: str,
        model: str = "doubao-seedream-4-5-251128",
        size: str = "2K",
        max_images: int = 6,
        response_format: str = "url",
        watermark: bool = True,
        **kwargs
    ) -> dict:
        """
        生成组图（多张关联图片）

        Args:
            prompt: 提示词
            model: 模型名称
            size: 图片尺寸 (2K/4K 或 像素如 1600x2848)
            max_images: 最大图片数量
            response_format: 返回格式
            watermark: 是否添加水印

        Returns:
            API 响应结果
        """
        data = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "response_format": response_format,
            "watermark": watermark,
            "sequential_image_generation": "auto",
            "stream": False,
            "sequential_image_generation_options": {
                "max_images": max_images
            }
        }

        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=data,
            timeout=180
        )

        result = response.json()

        if "error" in result:
            raise Exception(f"API 错误: {result['error']['code']} - {result['error']['message']}")

        return result


def save_images(result: dict, output_dir: str = "./output"):
    """
    保存生成的图片到本地

    Args:
        result: API 响应结果
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)

    data_list = result.get("data", [])
    created = result.get("created", 0)

    saved_paths = []

    for i, item in enumerate(data_list):
        if "url" in item:
            # 下载图片
            url = item["url"]
            ext = "png" if url.endswith(".png") else "jpg"
            filename = f"image_{created}_{i+1}.{ext}"
            filepath = os.path.join(output_dir, filename)

            response = requests.get(url)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            saved_paths.append(filepath)
            print(f"[OK] 图片已保存: {filepath}")

        elif "b64_json" in item:
            # 保存 base64
            import base64
            ext = "png"
            filename = f"image_{created}_{i+1}.{ext}"
            filepath = os.path.join(output_dir, filename)

            img_data = base64.b64decode(item["b64_json"])
            with open(filepath, "wb") as f:
                f.write(img_data)

            saved_paths.append(filepath)
            print(f"[OK] 图片已保存: {filepath}")

        elif "error" in item:
            print(f"[X] 第 {i+1} 张图片生成失败: {item['error']['message']}")

    return saved_paths


if __name__ == "__main__":
    # 简单测试
    print("API 客户端已就绪")
    print("请设置环境变量 JIMENG_API_KEY 或在代码中传入 api_key")
