# 中國行事曆

提供可供 Google Calendar、Apple Calendar 與 Outlook 訂閱的 iCalendar（ICS）行事曆，整理中國重要例行政治會議、政策會議、國防論壇與軍事紀念日。

> 最近人工查核：**2026-07-30（台灣時間）**

## 訂閱網址

```text
https://raw.githubusercontent.com/charles0506/china-political-calendar/main/china-political-calendar.ics
```

> Repository 必須維持 **Public**，Google Calendar 等外部服務才能定期讀取 Raw URL。

## 事件狀態

- `【已官宣】`：日期已由中國官方機構公布或會議已舉行。
- `【預估】`：依歷年慣例建立的觀察區間，不代表正式日期。
- `【待官宣】`：會議屬重要例行機制，但尚未公布日期。

所有未正式公布的事件均使用 `STATUS:TENTATIVE`，避免將推估誤認為正式日程。正式日期公布後，保留原 UID 並修改日期，以避免訂閱者產生重複事件。

## 目前涵蓋

### 政治與政策

- 全國人民代表大會年度會議
- 中國人民政治協商會議全國委員會年度會議
- 中共中央全體會議觀察窗
- 中央紀律檢查委員會全體會議
- 中央經濟工作會議
- 中央農村工作會議
- 中共中央政治局季度經濟會議觀察窗
- 中國共產黨全國代表大會觀察窗

### 軍事與國防

- 北京香山論壇與先導會
- 中國人民解放軍建軍節（八一建軍節）
- 中國人民解放軍海軍成立紀念日
- 中國人民解放軍空軍成立紀念日
- 中國人民解放軍火箭軍成立紀念日（原第二炮兵）

## 自動檢查

GitHub Actions 每週一 **08:00（Asia/Taipei）**執行：

1. 驗證官方來源網址。
2. 重新產生 ICS。
3. 只有內容變更時才提交更新。

目前自動程序主要負責來源檢查與重建 ICS；新官宣日期仍需先完成資料查核，再更新 `data/events.json`。

## 資料結構

```text
data/events.json                         事件資料
scripts/build_calendar.py                產生 ICS
scripts/check_sources.py                 檢查來源網址
china-political-calendar.ics             可訂閱行事曆
.github/workflows/weekly-check.yml        每週檢查與重建
```

## 更新原則

1. 優先使用中國政府網、中國人大網、全國政協網、中央紀委國家監委網站、國防部、中國軍網、新華社等官方來源。
2. 未公布日期不得填成確定事件。
3. 多日會議的 ICS `DTEND` 採排他日期，確保行事曆正確顯示最後一天。
4. 日期異動時保留 UID，並提高 `SEQUENCE`。
5. 時區以中國標準時間／台灣時間（UTC+8）理解；全日事件不受時區換算影響。

## 手動產生

```bash
python scripts/build_calendar.py
```

## 重要限制

中國政治與軍事會議中，只有兩會、建軍節與軍種成立紀念日等事件具有高度穩定日期。中央全會、政治局會議、中央經濟工作會議、北京香山論壇等正式日期可能在會前才公布，因此未官宣項目會明確標成觀察窗。