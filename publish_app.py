# publish_app.py
import streamlit as st
from pathlib import Path
import os

# 创建 cookies 目录
Path("cookies").mkdir(exist_ok=True)

# 导入各平台发布函数
try:
    from publishers.zhihu import publish_zhihu
    from publishers.toutiao import publish_toutiao
    from publishers.netease import publish_netease
    from publishers.sohu import publish_sohu
    from publishers.eastmoney import publish_eastmoney
except ImportError as e:
    st.error(f"❌ 模块导入失败: {e}")
    st.stop()

def run_publisher(name, func, content):
    try:
        with st.spinner(f"⏳ {name} 发布中..."):
            func(content)
        st.success(f"✅ {name} 发布成功！")
    except Exception as e:
        st.error(f"❌ {name} 失败: {str(e)}")

st.set_page_config(page_title="📤 五平台一键发布", layout="centered")
st.title("📤 五平台一键发布工具")
st.caption("支持：知乎｜今日头条｜网易号｜搜狐号｜东方财富")

content = st.text_area(
    "📝 文章内容（第一行请以「标题：」开头）",
    height=300,
    placeholder=(
        "示例：\n"
        "标题：2026年AI投资新机遇\n"
        "随着大模型技术突破，AI应用正加速落地...\n"
    ),
)

if st.button("🚀 一键发布到全部平台", type="primary"):
    if not content or not content.strip():
        st.error("❌ 内容为空，请粘贴文章！")
    else:
        # 按顺序发布
        run_publisher("知乎", publish_zhihu, content)
        run_publisher("今日头条", publish_toutiao, content)
        run_publisher("网易号", publish_netease, content)
        run_publisher("搜狐号", publish_sohu, content)
        run_publisher("东方财富", publish_eastmoney, content)
        
        st.balloons()
        st.success("🎉 所有平台发布任务已完成！")
