#!/usr/bin/env python3
"""
每日内容汇总 Skill - 自动抓取RSS内容，生成深度总结，更新到飞书云文档
"""
import os
import json
import time
import yaml
import feedparser
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from openai import OpenAI
from lark import Lark, APIError

# 配置文件路径
CONFIG_PATH = "config.yaml"
HISTORY_PATH = "history.json"

def load_config():
    """加载配置文件"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_history():
    """加载已处理的历史记录"""
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_history(history):
    """保存历史记录"""
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def fetch_rss_content(rss_url):
    """抓取RSS Feed内容"""
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            return None
        
        # 返回最新的一篇
        latest = feed.entries[0]
        return {
            'title': latest.title,
            'link': latest.link,
            'published': latest.published if hasattr(latest, 'published') else datetime.now().strftime("%Y-%m-%d"),
            'content': latest.summary if hasattr(latest, 'summary') else latest.description,
            'author': latest.author if hasattr(latest, 'author') else '未知作者',
            'id': latest.id if hasattr(latest, 'id') else latest.link
        }
    except Exception as e:
        print(f"抓取RSS失败 {rss_url}: {e}")
        return None

def extract_full_content(url):
    """提取网页全文内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除不必要的元素
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
        
        # 提取正文
        text = soup.get_text(separator='\n', strip=True)
        # 清理多余空行
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)[:10000]  # 限制长度
    except Exception as e:
        print(f"提取全文失败 {url}: {e}")
        return None

def generate_deep_summary(content, source_name, config):
    """使用LLM生成深度总结"""
    client = OpenAI(
        api_key=config['openai']['api_key'],
        base_url=config['openai'].get('base_url', 'https://api.openai.com/v1')
    )
    
    prompt = f"""
你是一个专业的内容分析师，需要对以下来自{source_name}的内容进行深度总结。
总结必须包含以下四个部分：
1. 📱 来源信息：发布者、发布时间、原文链接
2. 🎤 嘉宾/作者信息：介绍嘉宾背景、专业领域
3. 💬 核心话题：列出3-5个核心讨论话题，每个1-2句话
4. 💡 核心观点：列出5-8个核心观点，每个观点清晰明确，有深度

内容如下：
{content}

输出格式使用Markdown，不要使用任何多余的说明。
"""
    
    try:
        response = client.chat.completions.create(
            model=config['openai'].get('model', 'gpt-4'),
            messages=[
                {"role": "system", "content": "你是一个专业的内容分析师，擅长深度总结文章核心信息。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"生成总结失败: {e}")
        return None

def init_feishu_client(config):
    """初始化飞书客户端"""
    return Lark(
        app_id=config['feishu']['app_id'],
        app_secret=config['feishu']['app_secret']
    )

def create_feishu_doc(client, title, content):
    """创建飞书云文档"""
    try:
        response = client.create_document(
            title=title,
            content=content
        )
        return response.data['document']['document_id'], response.data['document']['url']
    except APIError as e:
        print(f"创建文档失败: {e}")
        return None, None

def update_feishu_doc(client, doc_id, content, append=True):
    """更新飞书云文档，append=True则追加，False则覆盖"""
    try:
        if append:
            # 先获取现有内容
            doc = client.get_document(doc_id=doc_id)
            existing_content = doc.data['content']
            new_content = existing_content + "\n\n---\n\n" + content
        else:
            new_content = content
        
        response = client.update_document(
            doc_id=doc_id,
            content=new_content
        )
        return True
    except APIError as e:
        print(f"更新文档失败: {e}")
        return False

def main():
    print(f"=== 每日内容汇总任务启动 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # 加载配置
    config = load_config()
    history = load_history()
    feishu_client = init_feishu_client(config)
    
    today = datetime.now().strftime("%Y-%m-%d")
    new_content = []
    no_update_sources = []
    
    # 遍历所有内容源
    for source in config['content_sources']:
        if not source.get('enabled', True):
            continue
            
        source_name = source['name']
        rss_url = source['rss']
        
        print(f"处理内容源: {source_name}")
        
        if not rss_url:
            no_update_sources.append(f"### {source_name}\n❌ 未配置RSS地址\n")
            continue
        
        # 抓取最新内容
        content = fetch_rss_content(rss_url)
        if not content:
            no_update_sources.append(f"### {source_name}\n❌ 获取内容失败\n")
            continue
        
        # 检查是否已处理过
        content_id = content['id']
        if content_id in history:
            no_update_sources.append(f"### {source_name}\n✅ 已检查，无新更新\n")
            continue
        
        # 提取全文
        full_content = extract_full_content(content['link'])
        if not full_content:
            full_content = content['content']
        
        # 生成深度总结
        summary = generate_deep_summary(full_content, source_name, config)
        if not summary:
            no_update_sources.append(f"### {source_name}\n❌ 生成总结失败\n")
            continue
        
        # 加入新内容
        new_content.append(f"## {source_name} - {content['title']}\n{summary}")
        
        # 保存到历史记录
        history[content_id] = {
            'source': source_name,
            'title': content['title'],
            'published': content['published'],
            'processed_at': today
        }
        
        print(f"✅ 完成 {source_name} 总结")
    
    # 保存历史记录
    save_history(history)
    
    # 生成最终文档内容
    doc_content = f"# 🎙️ 每日内容汇总 {today}\n\n"
    
    if new_content:
        doc_content += "## 🆕 今日更新\n\n"
        doc_content += "\n\n---\n\n".join(new_content)
        doc_content += "\n\n---\n\n"
    
    if no_update_sources:
        doc_content += "## ℹ️ 无更新内容源\n\n"
        doc_content += "\n".join(no_update_sources)
    
    # 更新飞书文档
    doc_id = config['feishu'].get('doc_id')
    doc_url = None
    
    if not doc_id:
        # 创建新文档
        doc_id, doc_url = create_feishu_doc(feishu_client, config['feishu']['doc_title'], doc_content)
        print(f"✅ 创建新文档: {doc_url}")
    else:
        # 追加到现有文档
        success = update_feishu_doc(feishu_client, doc_id, doc_content)
        if success:
            doc_url = f"https://www.feishu.cn/docx/{doc_id}"
            print(f"✅ 更新文档成功: {doc_url}")
    
    # 发送通知
    if doc_url:
        send_message = f"✅ 今日内容汇总已更新！\n📄 文档链接：{doc_url}"
        print(send_message)
        # 这里可以添加飞书消息推送逻辑
    
    print("=== 任务执行完成 ===")

if __name__ == "__main__":
    main()
