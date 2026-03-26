"""
儿童识字小报生成器 - 主入口
结合提示词生成 + 即梦 API 调用
"""

import os
import argparse
from generator import generate_prompt, SCENE_VOCABULARY
from api_client import JimengClient, save_images


def interactive_mode():
    """交互模式：引导用户输入"""
    print("=" * 50)
    print("   儿童识字小报生成器")
    print("=" * 50)
    print()

    # 显示支持的场景
    print("支持的场景：")
    for i, scene in enumerate(SCENE_VOCABULARY.keys(), 1):
        print(f"  {i}. {scene}")
    print()

    # 获取场景
    scene = input("请输入主题/场景（或输入序号）: ").strip()
    if scene.isdigit():
        idx = int(scene) - 1
        scene_list = list(SCENE_VOCABULARY.keys())
        if 0 <= idx < len(scene_list):
            scene = scene_list[idx]

    # 获取标题
    title = input("请输入小报大标题: ").strip()
    if not title:
        title = f"走进{scene}"

    print()
    print(f"场景: {scene}")
    print(f"标题: {title}")
    print()

    # 生成提示词
    print("正在生成提示词...")
    prompt = generate_prompt(scene, title)
    print(prompt)
    print()

    # 确认是否生成图片
    confirm = input("是否调用 API 生成图片？(y/n): ").strip().lower()
    if confirm != 'y':
        return

    # 调用 API
    run_api(prompt)


def run_api(prompt: str, api_key: str = None):
    """调用 API 生成图片"""
    try:
        client = JimengClient(api_key=api_key)

        print("正在调用即梦 API 生成图片（可能需要几十秒）...")
        result = client.generate_image(
            prompt=prompt,
            size="1600x2848",  # 竖版 9:16
            watermark=False
        )

        # 保存图片
        saved = save_images(result, "./output")
        print(f"\n共生成 {len(saved)} 张图片")

        # 打印完整响应（调试用）
        print("\n--- 完整响应 ---")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except ValueError as e:
        print(f"配置错误: {e}")
        print("请设置环境变量: export JIMENG_API_KEY='your-api-key'")
    except Exception as e:
        print(f"错误: {e}")


def main():
    parser = argparse.ArgumentParser(description="儿童识字小报生成器")
    parser.add_argument("--scene", "-s", help="主题/场景")
    parser.add_argument("--title", "-t", help="小报标题")
    parser.add_argument("--prompt", "-p", help="直接传入提示词")
    parser.add_argument("--api-key", "-k", help="API Key（也可设置 JIMENG_API_KEY 环境变量）")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--save", action="store_true", help="保存提示词到文件")

    args = parser.parse_args()

    if args.interactive or (not args.scene and not args.prompt):
        interactive_mode()
        return

    # 命令行模式
    if args.prompt:
        prompt = args.prompt
        if args.save:
            with open("prompt_output.md", "w", encoding="utf-8") as f:
                f.write(prompt)
            print("提示词已保存到 prompt_output.md")
        if args.api_key or os.getenv("JIMENG_API_KEY"):
            run_api(prompt, api_key=args.api_key)
        else:
            print("提示词已生成，未提供 API Key，跳过图片生成")
    else:
        if not args.scene:
            print("错误: 请提供 --scene 参数")
            return

        title = args.title or f"走进{args.scene}"
        prompt = generate_prompt(args.scene, title)

        print("=" * 50)
        print("生成的提示词:")
        print("=" * 50)
        print(prompt)

        if args.save:
            filename = f"prompt_{args.scene}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"\n提示词已保存到 {filename}")

        if args.api_key or os.getenv("JIMENG_API_KEY"):
            confirm = input("\n是否调用 API 生成图片？(y/n): ").strip().lower()
            if confirm == 'y':
                run_api(prompt, api_key=args.api_key)
        else:
            print("\n提示词已生成，设置 JIMENG_API_KEY 环境变量后可调用 API")


if __name__ == "__main__":
    main()
