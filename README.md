# Podcast Daily Summary - OpenClaw Skill

自动每日抓取15个内容源，生成深度AI资讯汇总，推送到飞书云文档。

## ✨ 功能特性

- 🚀 **自动抓取**：支持RSS Feed自动抓取，无需手动操作
- 🧠 **深度总结**：LLM生成深度内容总结，包含嘉宾信息、核心话题、核心观点
- 📝 **飞书集成**：自动更新到飞书云文档，支持多人协作查看
- 🔄 **内容去重**：自动跳过已总结过的内容，避免重复
- ⏰ **定时推送**：可配置每日固定时间推送
- 📊 **15个内容源**：5个海外AI资讯 + 10个中文科技播客

## 📋 内容源列表

### 海外AI资讯
1. **The Batch** (DeepLearning.AI) - 每周AI新闻汇总
2. **Interconnects** - 前沿模型分析与政策动态
3. **AI Snake Oil** - 辨别AI真伪与泡沫
4. **Chip Huyen** - ML系统工程实践
5. **Benedict Evans** - 科技战略与趋势分析

### 中文播客
6. 乱翻书
7. 新增长学院
8. 高能量
9. 科技早知道
10. Acquired
11. 卫诗婕漫谈
12. 十字路口Crossing
13. 半拿铁
14. 42章经
15. 张小珺商业访谈

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置
复制配置模板：
```bash
cp config_example.yaml config.yaml
```

编辑`config.yaml`，填入：
- 飞书应用ID和Secret
- OpenAI API Key
- 飞书文档ID（可选，自动创建）

### 3. 手动执行
```bash
python podcast_update_task.py
```

### 4. 定时执行
添加到crontab：
```bash
# 每天早上9点执行
0 9 * * * /usr/bin/python3 /path/to/podcast_update_task.py >> /var/log/podcast_cron.log 2>&1
```

## 📁 项目结构
```
podcast-daily-summary/
├── SKILL.md              # OpenClaw Skill定义
├── README.md             # 项目说明
├── requirements.txt      # Python依赖
├── podcast_update_task.py # 主执行脚本
├── config_example.yaml    # 配置模板
└── history.json          # 已处理内容历史（自动生成）
```

## 🛠️ 技术栈
- **内容抓取**：feedparser + BeautifulSoup4
- **内容总结**：OpenAI GPT-4
- **文档生成**：飞书开放API
- **定时执行**：crontab

## 📝 输出示例
```markdown
## 1. Interconnects - Dean Ball: 开放模型与政府控制

### 📱 来源信息
- 发布者：Nathan Lambert，AI研究员，前AI2
- RSS：https://www.interconnects.ai/feed

### 🎤 嘉宾
- Dean W. Ball：Hyperdimensional主理人，AI政策研究者

### 💬 核心话题
1. 政府管控与开放模型的博弈
2. 开放模型的资金困境（万亿训练成本）
3. 主权AI与全球需求

### 💡 核心观点
- 开放模型是长期保险政策
- 短期困难但长期看好
- 需要新的组织形式解决可持续性
```

## 🤝 贡献
欢迎提交Issue和PR！

## 📄 许可证
MIT License
