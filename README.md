# 儿童识字小报生成器

根据主题和标题，自动生成儿童识字小报的 AI 绘图提示词，并调用即梦/Seedream API 生成图片。

## 功能特性

- **自动词汇联想**：根据场景自动联想 15-20 个相关词汇（人物、物品、环境）
- **完整提示词**：填充 re.md 模板，生成可直接使用的提示词
- **即梦 API**：调用豆包 Seedream 模型生成图片
- **支持多场景**：超市、医院、公园、学校、餐厅、图书馆、农场、海边

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# Linux/Mac
export JIMENG_API_KEY='your-api-key'

# Windows PowerShell
$env:JIMENG_API_KEY='your-api-key'
```

或复制配置示例文件：
```bash
copy config.example.env .env
# 然后编辑 .env 填入 API Key
```

### 3. 运行

**交互模式**（引导输入）：
```bash
python main.py -i
```

**命令行模式**：
```bash
# 仅生成提示词
python main.py -s 超市 -t 走进超市

# 生成提示词并调用 API
python main.py -s 超市 -t 走进超市 -k $JIMENG_API_KEY

# 保存提示词到文件
python main.py -s 超市 -t 走进超市 --save
```

## 项目结构

```
jimeng-pic/
├── generator.py      # 提示词生成器（词汇联想 + 模板填充）
├── api_client.py     # 即梦 API 客户端
├── main.py           # 主入口
├── requirements.txt  # 依赖
└── README.md
```

## 支持的场景

| 场景 | 核心词汇示例 |
|------|-------------|
| 超市 | 收银员、货架、购物车、苹果、牛奶 |
| 医院 | 医生、护士、病床、体温计、口罩 |
| 公园 | 长椅、花坛、蝴蝶、蜻蜓、风筝 |
| 学校 | 教室、黑板、讲台、课本、铅笔 |
| 餐厅 | 厨师、服务员、餐桌、包子、面条 |
| 图书馆 | 管理员、书架、书、笔、笔记本 |
| 农场 | 农场、麦子、稻谷、牛、羊 |
| 海边 | 海滩、贝壳、沙、太阳、船 |

## API 说明

- **模型**：doubao-seedream-5.0-lite
- **尺寸**：1600x2848（竖版 9:16，A4 比例）
- **格式**：response_format=url
- **水印**：关闭

## 获取 API Key

访问 [火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) 创建 API Key。
