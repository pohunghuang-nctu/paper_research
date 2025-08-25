# Windsurf 企業版部署選項分析

本文旨在整理與分析 Windsurf AI 編碼工具針對企業客戶提供的部署選項，特別是關於本地託管（On-Premise/Self-Hosted）的相關資訊。資訊來源為 Windsurf 官方網站、部落格及技術文件。

## 結論摘要

- **舊有 Self-Hosted 方案已停止**：Windsurf 曾提供一個完整的自我託管方案（Self-Hosted Offering），但根據官方部落格，該方案目前已進入「維護模式」，不再對新客戶提供。
- **現行方案：混合部署（Hybrid Deployment）**：取而代之的是一個名為「混合部署選項（Hybrid Deployment Option）」的方案，此為其企業版（Enterprise Plan）的一部分。
- **運作核心：自訂企業 URL**：混合部署的核心機制是允許企業客戶在開發人員的 IDE 插件中，設定一個自訂的後端伺服器 URL。這使得程式碼相關的請求可以被導向企業內部的伺服器，而非 Windsurf 的公有雲，從而確保程式碼的隱私與安全。
- **深入資訊需洽詢官方**：關於後端伺服器的具體架構、硬體需求、部署流程等詳細技術文件並未公開。企業若有興趣，需直接聯繫 Windsurf 銷售團隊以獲取進一步資訊。

---

## 詳細查證過程

### 1. Self-Hosted 方案進入維護模式

根據 Windsurf 官方部落格文章 [Self-Hosted Deployment Maintenance Mode](https://windsurf.com/blog/self-hosted-deployment-maintenance-mode)，官方明確表示：

> "We have decided to place our self-hosted offering in maintenance mode, and offer a new single-tenant hosted offering that can expose our agentic capabilities."

這證實了過去的純本地部署方案已不再是主流選項。

### 2. 混合部署選項 (Hybrid Deployment Option)

在 [Windsurf for Enterprise](https://windsurf.com/enterprise) 的官方頁面上，其「Enterprise」方案的特色列表中明確包含了「**Hybrid deployment option**」，證實了此為現行的主要方案。

### 3. 混合部署的技術實現

雖然沒有專門的架構文件，但在各個 IDE 插件的技術文件中，可以找到其運作的蛛絲馬跡。以 JetBrains IDE 為例，其[疑難排解頁面](https://docs.windsurf.com/troubleshooting/plugins-enterprise/jetbrains)提供了如何設定自訂企業 URL 的說明：

> **How to reset or change your Enterprise URL**
> 1. Go to `Tools → Codeium Enterprise → Reset Codeium Enterprise Updater`.
> 2. Enter the new URL...
> 3. Restart your IDE.

此功能讓 IDE 插件能將請求發送到企業指定的端點，實現了混合部署的基礎。這意味著企業可以將一部分服務（特別是處理程式碼的服務）保留在內部網路中，同時可能仍需與 Windsurf 的雲端進行授權或模型更新等通訊。
