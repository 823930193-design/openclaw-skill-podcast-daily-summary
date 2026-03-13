<div align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=for-the-badge" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
  
  <h1>🎙️ 每日内容汇总 | Podcast Daily Summary</h1>
  <p>
    <strong>自动每日AI资讯聚合 · 深度总结 · 飞书云文档同步</strong>
  </p>
  <p>
    每天早上9点，自动为你整理15个优质内容源的最新动态，生成深度可读的总结，直接推送到飞书云文档。
  </p>
</div>

---

## 🔥 为什么需要这个Skill？

作为一个关注AI和科技行业的从业者，你是不是每天都在：
- 📚 订阅了几十个Newsletter、播客、博客，却没时间看？
- ⏰ 想利用早上通勤时间了解行业动态，却找不到高质量的内容汇总？
- ✂️ 厌倦了手动复制粘贴链接，整理各种来源的信息？
- 📝 想要深度观点而不是仅仅看标题和摘要？

这个Skill帮你解决所有问题：**一次配置，终身受益，每天自动收到高质量的深度内容汇总，足够你20-30分钟的深度阅读**。

---

## ✨ 功能特性

| 特性 | 描述 |
|------|------|
| 🤖 **全自动抓取** | 支持RSS Feed自动抓取，无需任何手动操作 |
| 🧠 **AI深度总结** | LLM生成专业级深度总结，包含嘉宾背景、核心话题、精选观点 |
| 📝 **飞书集成** | 自动同步到飞书云文档，支持多人协作、评论、分享 |
| 🔄 **智能去重** | 自动识别已总结过的内容，避免重复推送 |
| ⏰ **定时推送** | 可配置每日固定时间推送，默认早上9点 |
| 📊 **15个精选内容源** | 精心挑选5个海外AI资讯 + 10个中文科技播客 |
| 🎯 **高质量内容** | 只选最有深度、最前沿的内容源，拒绝垃圾信息 |

---

## 📋 精选内容源列表

### 🌍 海外AI资讯（5个）
| 名称 | 作者/机构 | 内容方向 | 更新频率 |
|------|----------|----------|----------|
| **The Batch** | DeepLearning.AI（吴恩达团队） | 每周AI行业新闻汇总 | 每周 |
| **Interconnects** | Nathan Lambert（前AI2研究员） | 前沿模型分析、AI政策动态 | 每周2-3次 |
| **AI Snake Oil** | 普林斯顿大学团队 | 辨别AI真伪、揭露行业泡沫 | 每周 |
| **Chip Huyen Blog** | Chip Huyen（斯坦福ML讲师） | ML系统工程、AI落地实践 | 每周 |
| **Benedict Evans** | 前a16z合伙人 | 科技战略、行业趋势分析 | 每周 |

### 🎙️ 中文科技播客（10个）
| 名称 | 内容方向 |
|------|----------|
| **乱翻书** | 互联网、科技行业深度对话 |
| **新增长学院** | 增长、产品、商业案例 |
| **高能量** | 科技创业者访谈 |
| **科技早知道** | 全球科技新闻解读 |
| **Acquired** | 全球科技公司深度剖析 |
| **卫诗婕漫谈** | 消费、品牌、商业观察 |
| **十字路口Crossing** | 前沿科技、未来趋势 |
| **半拿铁** | 商业史、公司沉浮录 |
| **42章经** | 创投、创业、互联网趋势 |
| **张小珺商业访谈** | 一线创业者、投资人深度访谈 |

---

## 🚀 3分钟快速上手

### 1. 安装依赖
```bash
# 克隆仓库
git clone https://github.com/823930193-design/openclaw-skill-podcast-daily-summary.git
cd openclaw-skill-podcast-daily-summary

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置参数
```bash
# 复制配置模板
cp config_example.yaml config.yaml

# 编辑config.yaml，填入你的信息
vim config.yaml
```

需要配置的信息：
```yaml
feishu:
  app_id: "cli_xxxxxx"          # 飞书应用ID
  app_secret: "xxxxxx"          # 飞书应用Secret
  doc_title: "每日内容汇总"      # 文档标题

openai:
  api_key: "sk-xxxxxx"          # OpenAI API Key
  model: "gpt-4"                # 总结用的模型，推荐gpt-4
```

### 3. 手动执行测试
```bash
python podcast_update_task.py
```
执行完成后你会收到飞书文档链接，打开就能看到今日的内容汇总！

### 4. 配置定时执行（每天9点推送）
```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天早上9点执行）
0 9 * * * /usr/bin/python3 /path/to/podcast_update_task.py >> /var/log/podcast_cron.log 2>&1
```

### 🎉 完成！
从此以后，每天早上9点，你都会自动收到最新的深度内容汇总~

---

## 📁 项目结构

```
openclaw-skill-podcast-daily-summary/
├── SKILL.md              # OpenClaw Skill 定义文件
├── README.md             # 你正在看的使用说明
├── requirements.txt      # Python 依赖包列表
├── podcast_update_task.py # 主执行脚本
├── config_example.yaml    # 配置模板
└── history.json          # 已处理内容历史（自动生成）
```

---

## 🛠️ 技术栈

| 模块 | 技术选型 | 说明 |
|------|----------|------|
| 内容抓取 | feedparser + BeautifulSoup4 | RSS解析、网页内容提取 |
| 内容总结 | OpenAI GPT-4 | 生成专业级深度总结 |
| 文档生成 | 飞书开放API | 自动创建/更新飞书云文档 |
| 定时执行 | crontab | Linux系统定时任务 |

---

## 📝 输出示例

```markdown
## 1. Interconnects - Dean Ball: 开放模型与政府控制

### 📱 来源信息
- 发布者：Nathan Lambert，AI研究员，前AI2
- 发布时间：2026-03-13
- 原文链接：https://www.interconnects.ai/p/government-control-open-models

### 🎤 嘉宾信息
- **Dean W. Ball**：Hyperdimensional newsletter主理人，AI政策研究者，长期关注全球AI监管动态。

### 💬 核心话题
1. 美国国防部将Anthropic列为"供应链风险"的政策影响
2. 万亿级训练成本下开放模型的可持续性问题
3. 全球各国"主权AI"建设的需求与挑战
4. 开放模型与闭源模型的能力差距趋势分析

### 💡 核心观点
- 开放模型是"长期保险政策"：即使政府加强AI管控，开源权重模型仍可自由使用
- 短期来看开放模型发展会遇到困难，但长期对整个行业更有利
- 训练成本达到万亿级别后，传统的"commoditize complements"商业模式不再适用
- 需要新的组织形式来解决开放模型的资金和可持续性问题
```

---

## 🤝 贡献

欢迎提交Issue和PR！如果你有更好的内容源推荐，或者功能改进建议，欢迎一起完善这个Skill。

## 📄 许可证

MIT License - 自由使用，自由修改。

---

<div align="center">
  <strong>如果这个Skill对你有帮助，欢迎给个⭐️ Star！</strong>
  <br>
  <sub>Built with ❤️ for OpenClaw community</sub>
</div>