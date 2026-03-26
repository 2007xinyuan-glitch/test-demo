"""
儿童识字小报提示词生成器
根据主题和标题，自动联想词汇并填充模板
"""

# 各场景的词汇联想字典
SCENE_VOCABULARY = {
    "超市": {
        "core_facilities": ["shōu yín yuán 收银员", "huò jià 货架", "gēnggēng chē 购物车", "shōu yín tái 收银台", "dǎ yìn jī 打印机"],
        "common_items": ["píng guǒ 苹果", "niú nǎi 牛奶", "miàn bāo 面包", "shuǐ guǒ 水果", "cǎo méi 草莓", "jú zi 橘子", "bō luó 菠萝", "hā mì guā 哈密瓜"],
        "environment": ["chū kǒu 出口", "rù kǒu 入口", "dēng 灯", "qiáng 墙", "biāo jià 标价牌", "gēnggēng lán 购物篮"]
    },
    "医院": {
        "core_facilities": ["yī shēng 医生", "hù shi 护士", "bìng chuáng 病床", "tīng zhěn shì 诊室", "yào fáng 药房"],
        "common_items": ["tǐ wēn jì 体温计", "yào 药", "bēng dài 绷带", "kǒu zhào 口罩", "zhěn duàn zhǐ 诊断书", "zhù shè qì 注射器", "tuō bǎn 托盘", "shuǐ bēi 水杯"],
        "environment": ["mén zhěn 台诊", "hù dēng 护灯", "chuáng tóu guì 床头柜", "bái bù 帘", "jìào hào qì 叫号器", "yī yào柜 药柜"]
    },
    "公园": {
        "core_facilities": ["cháng chéng 长椅", "huā tán 花坛", " hú dié 蝴蝶", "qīng tíng 蜻蜓", "kōng zhōng 空中"],
        "common_items": ["qiān niú huā 牵牛花", "xiàng pí shù 橡皮树", "cǎo 草", "shù 叶", "fēng zheng 风筝", "zú qiú 足球", "pái qiú 排球", "shā kēng 沙坑"],
        "environment": ["xiǎo jìng 小径", "dēng long 灯笼", "pēn quán 喷泉", "gōng jiǎo 公厕", "zhǐ shi pái 指事牌", "shù yè 树叶"]
    },
    "学校": {
        "core_facilities": ["jiào shì 教室", "hēi bǎn 黑板", "jiǎng tái 讲台", "kè zhuō 课桌", "lǎo shī 老师"],
        "common_items": ["kè běn 课本", "qiān bǐ 铅笔", "xiàng pí 橡皮", "chǐ zi 尺子", "wá wa 娃娃", "qiū qiān 秋千", "lán qiú 篮球", "tiào shéng 跳绳"],
        "environment": ["guó qí 国旗", "mén chuāng 门窗", "zǒu láng 走廊", "cāo chǎng 操场", "tǐ yù guǎn 体育馆", " tú shū guǎn 图书馆"]
    },
    "餐厅": {
        "core_facilities": ["chú shī 厨师", "fú wù yuán 服务员", "cān zhuō 餐桌", "yǐ zi 椅子", "chú fáng 厨房"],
        "common_items": ["páo mó 包子", "miàn tiáo 面条", "mǐ fàn 米饭", "jī dàn 鸡蛋", "qié zi 茄子", "luó bo 胡萝卜", "tāng guō 汤锅", "cài dān 菜单"],
        "environment": ["mén pái 门牌", "zhōng biǎo 钟表", "dēng guāng 灯光", "zhuō bù 桌布", "cān jin 纸巾", "wū dǐng 屋顶"]
    },
    "图书馆": {
        "core_facilities": ["guǎn lǐ yuán 管理员", "shū jià 书架", "yuè dú qū 阅读区", "jì suàn jī 计算机", "zhuō zi 桌子"],
        "common_items": ["shū 书", "bǐ 笔", "bǐ jì běn 笔记本", "dì tú 地图", "zá zhì 杂志", "bào zhǐ 报纸", "gōng jù shū 工具书", "tú huà shū 图画书"],
        "environment": ["mén 门", "chuāng 窗", "dēng 灯", "lóu tī 楼梯", "biāo zhì 标志", "fú 幅"]
    },
    "农场": {
        "core_facilities": ["nóng chǎng 农场", "gōng jù shè 工具棚", "mù wū 木屋", "wū 屋", "shēng kou 牲口"],
        "common_items": ["mài zi 麦子", "dào gǔ 稻谷", "yù mǐ 玉米", "tǔ dòu 土豆", "niú 牛", "yáng 羊", "zhū 猪", "jī 鸡"],
        "environment": ["cǎo duī 草堆", "shuǐ jǐng 水井", "tián 亩", "hé 流", "shù 林", "shān 丘"]
    },
    "海边": {
        "core_facilities": ["shā tān 海滩", "chōng lòng 冲浪板", "bīng xiāng 冰箱", "zhàng péng 帐篷", "dǎo 岛"],
        "common_items": ["bèi ké 贝壳", "shā 沙", "hǎi zǎo 海藻", "pào pao 泡泡", "chōu làn 冲浪", "shuǐ qiāng 水枪", "tǔ 桶", "jué 桨"],
        "environment": ["tài yáng 太阳", "yún 云", "hǎi làng 海浪", "chuán 船", "dēng tái 灯塔", "shā 滩"]
    }
}


def get_vocabulary_by_scene(scene: str) -> dict:
    """根据场景获取联想词汇"""
    scene = scene.strip()
    # 模糊匹配
    for key in SCENE_VOCABULARY:
        if key in scene or scene in key:
            return SCENE_VOCABULARY[key]
    # 默认返回超市（最常见）
    return SCENE_VOCABULARY["超市"]


def generate_prompt(scene: str, title: str) -> str:
    """
    根据主题和标题生成完整的提示词
    """
    vocab = get_vocabulary_by_scene(scene)

    # 构建各部分内容
    core_facilities = ", ".join(vocab["core_facilities"])
    common_items = ", ".join(vocab["common_items"])
    environment = ", ".join(vocab["environment"])

    prompt = f"""请生成一张儿童识字小报《{scene}》，竖版 A4，学习小报版式，适合 5–9 岁孩子 认字与看图识物。

# 一、小报标题区（顶部）

**顶部居中大标题**：《{title}》
* **风格**：十字小报 / 儿童学习报感
* **文本要求**：大字、醒目、卡通手写体、彩色描边
* **装饰**：周围添加与 {scene} 相关的贴纸风装饰，颜色鲜艳

# 二、小报主体（中间主画面）

画面中心是一幅 **卡通插画风的「{scene}」场景**：
* **整体气氛**：明亮、温暖、积极
* **构图**：物体边界清晰，方便对应文字，不要过于拥挤。

**场景分区与核心内容**
1.  **核心区域 A（主要对象）**：表现 {scene} 的核心活动。
2.  **核心区域 B（配套设施）**：展示相关的工具或物品。
3.  **核心区域 C（环境背景）**：体现环境特征（如墙面、指示牌等）。

**主题人物**
* **角色**：1 位可爱卡通人物（职业/身份：与 {scene} 匹配）。
* **动作**：正在进行与场景相关的自然互动。

# 三、必画物体与识字清单（Generated Content）

**请务必在画面中清晰绘制以下物体，并为其预留贴标签的位置：**

**1. 核心角色与设施：**
{core_facilities}

**2. 常见物品/工具：**
{common_items}

**3. 环境与装饰：**
{environment}

*(注意：画面中的物体数量不限于此，但以上列表必须作为重点描绘对象)*

# 四、识字标注规则

对上述清单中的物体，贴上中文识字标签：
* **格式**：两行制（第一行拼音带声调，第二行简体汉字）。
* **样式**：彩色小贴纸风格，白底黑字或深色字，清晰可读。
* **排版**：标签靠近对应的物体，不遮挡主体。

# 五、画风参数
* **风格**：儿童绘本风 + 识字小报风
* **色彩**：高饱和、明快、温暖 (High Saturation, Warm Tone)
* **质量**：8k resolution, high detail, vector illustration style, clean lines."""

    return prompt


if __name__ == "__main__":
    # 测试
    prompt = generate_prompt("超市", "走进超市")
    print(prompt)
