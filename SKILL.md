# 🎙️ 每日内容汇总 Skill

## 功能描述
自动每天定时抓取15个内容源的最新信息，生成深度总结并推送到飞书云文档。支持RSS抓取、内容去重、LLM深度总结、飞书文档自动更新。

## 使用场景
1. 每日AI资讯、行业动态自动汇总
2. 播客/ Newsletter内容自动整理
3. 个人信息订阅流聚合

## 触发方式
- 定时自动执行（默认每天早上9点）
- 手动执行：`python podcast_update_task.py`

## 配置说明
### 1. 环境配置
```yaml
# config.yaml
feishu_app_id: "cli_xxxxxx"
feishu_app_secret: "xxxxxx"
openai_api_key: "sk-xxxxxx"
doc_id: "Nn7OdlJVsoO6i2xrLYCcPcHXnXc"  # 飞书文档ID
```

### 2. 内容源配置
```yaml
content_sources:
  - name: "Interconnects AI"
    rss: "https://www.interconnects.ai/feed"
    type: "newsletter"
  - name: "Chip Huyen Blog"
    rss: "https://huyenchip.com/feed"
    type: "blog"
```

### 3. 定时配置
默认每天9点执行，可在crontab中修改：
```bash
0 9 * * * /usr/bin/python3 /path/to/podcast_update_task.py >> /var/log/podcast_cron.log 2>&1
```

## 输出格式
每个内容源总结包含：
- 📱 来源信息（发布者、机构、订阅量）
- 🎤 嘉宾/作者信息
- 💬 核心话题（编号）
- 💡 核心观点（编号）

## 依赖
- feedparser >= 6.0.10
- openai >= 1.0.0
- lark-oapi >= 1.0.0
- beautifulsoup4 >= 4.12.0
