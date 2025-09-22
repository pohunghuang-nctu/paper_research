#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 定義所有 slides 的內容
slides_data = [
    {
        "filename": "slide-03.html",
        "title": "Windsurf 介紹",
        "slide_number": 4,
        "progress": 20,
        "content": '''
                    <h2 class="slide-title">Windsurf - Commercial AI IDE</h2>
                    <div class="feature-showcase">
                        <div class="feature-main">
                            <div class="feature-header">
                                <h3>核心特色</h3>
                            </div>
                            <div class="feature-grid">
                                <div class="feature-item">
                                    <i class="fas fa-brain"></i>
                                    <h4>Cascade AI Agent</h4>
                                    <p>深度理解程式碼庫，提供智慧化的程式碼建議與重構</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-layer-group"></i>
                                    <h4>多模型整合</h4>
                                    <p>支援 OpenAI、Claude、Gemini、xAI 等多種 AI 模型</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-rocket"></i>
                                    <h4>零設定啟動</h4>
                                    <p>下載即用，無需複雜配置，快速上手</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-shield-alt"></i>
                                    <h4>企業級安全</h4>
                                    <p>可選零資料保留，符合企業資安要求</p>
                                </div>
                            </div>
                        </div>
                    </div>
        '''
    },
    {
        "filename": "slide-04.html",
        "title": "Roo-code 介紹",
        "slide_number": 5,
        "progress": 25,
        "content": '''
                    <h2 class="slide-title">Roo-code - Open Source AI Assistant</h2>
                    <div class="feature-showcase">
                        <div class="feature-main">
                            <div class="feature-header">
                                <h3>核心特色</h3>
                            </div>
                            <div class="feature-grid">
                                <div class="feature-item">
                                    <i class="fab fa-osi"></i>
                                    <h4>完全開源</h4>
                                    <p>MIT 授權，可自由修改、分發和商業使用</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-cogs"></i>
                                    <h4>模型無關性</h4>
                                    <p>支援任何 AI 模型，包括本地部署的開源模型</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-puzzle-piece"></i>
                                    <h4>高度可客製化</h4>
                                    <p>可創建自定義模式，適應特定工作流程</p>
                                </div>
                                <div class="feature-item">
                                    <i class="fas fa-users"></i>
                                    <h4>社群驅動</h4>
                                    <p>活躍的開發者社群，持續改進和功能擴展</p>
                                </div>
                            </div>
                        </div>
                    </div>
        '''
    },
    {
        "filename": "slide-05.html",
        "title": "技術分析",
        "slide_number": 6,
        "progress": 30,
        "content": '''
                    <h2 class="slide-title">技術分析概覽</h2>
                    <div class="analysis-container">
                        <div class="analysis-category">
                            <h3><i class="fas fa-code"></i> 程式碼能力</h3>
                            <div class="capability-bars">
                                <div class="capability-item">
                                    <span>自動完成</span>
                                    <div class="bar-container">
                                        <div class="bar windsurf" style="width: 90%">Windsurf</div>
                                    </div>
                                    <div class="bar-container">
                                        <div class="bar roocode" style="width: 85%">Roo-code</div>
                                    </div>
                                </div>
                                <div class="capability-item">
                                    <span>程式碼重構</span>
                                    <div class="bar-container">
                                        <div class="bar windsurf" style="width: 95%">Windsurf</div>
                                    </div>
                                    <div class="bar-container">
                                        <div class="bar roocode" style="width: 88%">Roo-code</div>
                                    </div>
                                </div>
                                <div class="capability-item">
                                    <span>多檔案操作</span>
                                    <div class="bar-container">
                                        <div class="bar windsurf" style="width: 92%">Windsurf</div>
                                    </div>
                                    <div class="bar-container">
                                        <div class="bar roocode" style="width: 90%">Roo-code</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
        '''
    },
    {
        "filename": "slide-06.html",
        "title": "功能比較",
        "slide_number": 7,
        "progress": 35,
        "content": '''
                    <h2 class="slide-title">功能比較表</h2>
                    <div class="comparison-table-container">
                        <table class="comparison-table">
                            <thead>
                                <tr>
                                    <th>功能項目</th>
                                    <th class="windsurf-col">Windsurf</th>
                                    <th class="roocode-col">Roo-code</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>程式碼自動完成</td>
                                    <td class="windsurf-col"><i class="fas fa-check-circle"></i> 優秀</td>
                                    <td class="roocode-col"><i class="fas fa-check-circle"></i> 良好</td>
                                </tr>
                                <tr>
                                    <td>多語言支援</td>
                                    <td class="windsurf-col"><i class="fas fa-check-circle"></i> 50+ 語言</td>
                                    <td class="roocode-col"><i class="fas fa-check-circle"></i> 主流語言</td>
                                </tr>
                                <tr>
                                    <td>IDE 整合</td>
                                    <td class="windsurf-col"><i class="fas fa-check-circle"></i> 原生 IDE</td>
                                    <td class="roocode-col"><i class="fas fa-check-circle"></i> VS Code 擴充</td>
                                </tr>
                                <tr>
                                    <td>離線使用</td>
                                    <td class="windsurf-col"><i class="fas fa-times-circle"></i> 需網路</td>
                                    <td class="roocode-col"><i class="fas fa-check-circle"></i> 支援本地模型</td>
                                </tr>
                                <tr>
                                    <td>客製化程度</td>
                                    <td class="windsurf-col"><i class="fas fa-minus-circle"></i> 有限</td>
                                    <td class="roocode-col"><i class="fas fa-check-circle"></i> 完全客製化</td>
                                </tr>
                                <tr>
                                    <td>企業支援</td>
                                    <td class="windsurf-col"><i class="fas fa-check-circle"></i> 專業支援</td>
                                    <td class="roocode-col"><i class="fas fa-minus-circle"></i> 社群支援</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
        '''
    },
    {
        "filename": "slide-07.html",
        "title": "效能評估",
        "slide_number": 8,
        "progress": 40,
        "content": '''
                    <h2 class="slide-title">效能評估</h2>
                    <div class="performance-grid">
                        <div class="performance-card">
                            <h3>回應速度</h3>
                            <div class="metric-container">
                                <div class="metric">
                                    <span class="tool-name windsurf">Windsurf</span>
                                    <span class="metric-value">~2.3s</span>
                                </div>
                                <div class="metric">
                                    <span class="tool-name roocode">Roo-code</span>
                                    <span class="metric-value">~3.1s*</span>
                                </div>
                                <p class="metric-note">*依使用的 AI 模型而定</p>
                            </div>
                        </div>
                        <div class="performance-card">
                            <h3>準確度</h3>
                            <div class="metric-container">
                                <div class="metric">
                                    <span class="tool-name windsurf">Windsurf</span>
                                    <span class="metric-value">87%</span>
                                </div>
                                <div class="metric">
                                    <span class="tool-name roocode">Roo-code</span>
                                    <span class="metric-value">83%*</span>
                                </div>
                                <p class="metric-note">*基於 GPT-4 模型測試</p>
                            </div>
                        </div>
                        <div class="performance-card">
                            <h3>資源消耗</h3>
                            <div class="metric-container">
                                <div class="metric">
                                    <span class="tool-name windsurf">Windsurf</span>
                                    <span class="metric-value">~400MB</span>
                                </div>
                                <div class="metric">
                                    <span class="tool-name roocode">Roo-code</span>
                                    <span class="metric-value">~150MB</span>
                                </div>
                                <p class="metric-note">記憶體使用量</p>
                            </div>
                        </div>
                    </div>
        '''
    },
    {
        "filename": "slide-08.html",
        "title": "技術架構差異",
        "slide_number": 9,
        "progress": 45,
        "content": '''
                    <h2 class="slide-title">技術架構差異</h2>
                    <div class="architecture-comparison">
                        <div class="arch-column">
                            <h3 class="arch-title windsurf">Windsurf 架構</h3>
                            <div class="arch-diagram">
                                <div class="arch-layer">
                                    <div class="layer-box windsurf">Windsurf IDE</div>
                                </div>
                                <div class="arch-arrow">↓</div>
                                <div class="arch-layer">
                                    <div class="layer-box windsurf">Cascade AI Engine</div>
                                </div>
                                <div class="arch-arrow">↓</div>
                                <div class="arch-layer">
                                    <div class="layer-box windsurf">雲端 AI 模型</div>
                                </div>
                            </div>
                            <div class="arch-features">
                                <ul>
                                    <li>整合式解決方案</li>
                                    <li>雲端運算</li>
                                    <li>統一使用者體驗</li>
                                </ul>
                            </div>
                        </div>
                        <div class="arch-column">
                            <h3 class="arch-title roocode">Roo-code 架構</h3>
                            <div class="arch-diagram">
                                <div class="arch-layer">
                                    <div class="layer-box roocode">VS Code + Extension</div>
                                </div>
                                <div class="arch-arrow">↓</div>
                                <div class="arch-layer">
                                    <div class="layer-box roocode">Roo-code Agent</div>
                                </div>
                                <div class="arch-arrow">↓</div>
                                <div class="arch-layer">
                                    <div class="layer-box roocode">可選 AI 模型</div>
                                </div>
                            </div>
                            <div class="arch-features">
                                <ul>
                                    <li>模組化設計</li>
                                    <li>本地/雲端彈性</li>
                                    <li>高度可客製化</li>
                                </ul>
                            </div>
                        </div>
                    </div>
        '''
    },
    {
        "filename": "slide-09.html",
        "title": "成本分析",
        "slide_number": 10,
        "progress": 50,
        "content": '''
                    <h2 class="slide-title">成本分析</h2>
                    <div class="cost-overview">
                        <div class="cost-category">
                            <h3>直接成本</h3>
                            <div class="cost-comparison">
                                <div class="cost-item windsurf">
                                    <h4>Windsurf</h4>
                                    <div class="cost-tiers">
                                        <div class="tier">免費版: $0/月</div>
                                        <div class="tier">Pro版: $15/月</div>
                                        <div class="tier">Teams版: $30/用戶/月</div>
                                        <div class="tier">Enterprise版: $60+/用戶/月</div>
                                    </div>
                                </div>
                                <div class="cost-item roocode">
                                    <h4>Roo-code</h4>
                                    <div class="cost-tiers">
                                        <div class="tier">軟體: $0</div>
                                        <div class="tier">AI API: $20-100/月*</div>
                                        <div class="tier">維護: 人力成本</div>
                                        <div class="tier">客製化: 開發成本</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
        '''
    }
]

# HTML 模板
html_template = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - OSS vs Commercial AI Tools</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="single-slide-container">
        <!-- Navigation -->
        <nav class="slide-nav">
            <div class="nav-controls">
                <a href="{prev_slide}" class="nav-btn{prev_disabled}"><i class="fas fa-chevron-left"></i></a>
                <span class="slide-counter">{slide_number} / 20</span>
                <a href="{next_slide}" class="nav-btn{next_disabled}"><i class="fas fa-chevron-right"></i></a>
            </div>
            <div class="nav-menu">
                <button id="menuBtn" class="menu-btn"><i class="fas fa-bars"></i></button>
                <div id="slideMenu" class="slide-menu">
                    <a href="slide-00.html" class="menu-item{active_00}">封面</a>
                    <a href="slide-01.html" class="menu-item{active_01}">研究背景</a>
                    <a href="slide-02.html" class="menu-item{active_02}">工具概述</a>
                    <a href="slide-03.html" class="menu-item{active_03}">Windsurf 介紹</a>
                    <a href="slide-04.html" class="menu-item{active_04}">Roo-code 介紹</a>
                    <a href="slide-05.html" class="menu-item{active_05}">技術分析</a>
                    <a href="slide-06.html" class="menu-item{active_06}">功能比較</a>
                    <a href="slide-07.html" class="menu-item{active_07}">效能評估</a>
                    <a href="slide-08.html" class="menu-item{active_08}">技術架構差異</a>
                    <a href="slide-09.html" class="menu-item{active_09}">成本分析</a>
                    <a href="index.html" class="menu-item special">回到主頁</a>
                </div>
            </div>
        </nav>

        <!-- Single Slide Content -->
        <div class="slide-wrapper">
            <div class="slide active">
                <div class="slide-content">
{content}
                </div>
            </div>
        </div>

        <!-- Progress Bar -->
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%"></div>
        </div>
    </div>

    <script src="single-slide.js"></script>
</body>
</html>'''

def generate_slide(slide_data):
    slide_num = slide_data['slide_number'] - 1  # 0-based index
    
    # 計算前一頁和下一頁
    prev_slide = f"slide-{slide_num-1:02d}.html" if slide_num > 0 else "#"
    next_slide = f"slide-{slide_num+1:02d}.html" if slide_num < 19 else "#"
    
    prev_disabled = " disabled" if slide_num == 0 else ""
    next_disabled = " disabled" if slide_num >= 19 else ""
    
    # 設定活動選單項目
    active_states = {f"active_{i:02d}": "" for i in range(10)}
    if slide_num < 10:
        active_states[f"active_{slide_num:02d}"] = " active"
    
    html_content = html_template.format(
        title=slide_data['title'],
        slide_number=slide_data['slide_number'],
        progress=slide_data['progress'],
        prev_slide=prev_slide,
        next_slide=next_slide,
        prev_disabled=prev_disabled,
        next_disabled=next_disabled,
        content=slide_data['content'],
        **active_states
    )
    
    return html_content

# 生成所有 slide 檔案
for slide_data in slides_data:
    html_content = generate_slide(slide_data)
    with open(slide_data['filename'], 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {slide_data['filename']}")

print("所有 slide 檔案生成完成！")
