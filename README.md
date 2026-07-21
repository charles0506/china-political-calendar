# 中國重要政治會議行事曆

提供可供 Google Calendar、Apple Calendar 與 Outlook 訂閱的 iCalendar（ICS）行事曆，整理中國重要例行政治會議與政策會議。

## 訂閱網址

Repository 改成 **Public** 後，使用：

```text
https://raw.githubusercontent.com/charles0506/china-political-calendar/main/china-political-calendar.ics
```

> 注意：目前 repository 若為 Private，Google Calendar 等外部服務無法定期讀取 Raw URL。

## 事件狀態

- `【已官宣】`：日期已由中國官方機構公布或會議已舉行。
- `【預估】`：依歷年慣例建立的觀察區間，不代表正式日期。
- `【待官宣】`：會議屬重要例行機制，但尚未公布日期。

所有未正式公布的事件均使用 `STATUS:TENTATIVE`，避免將推估誤認為正式日程。正式日期公布後，應保留原 UID 並修改日期，以避免訂閱者產生重複事件。

## 目前涵蓋

- 全國人民代表大會年度會議
- 中國人民政治協商會議全國委員會年度會議
- 中共中央全體會議觀察窗
- 中央紀律檢查委員會全體會議
- 中央經濟工作會議
- 中央農村工作會議
- 中共中央政治局季度經濟會議觀察窗
- 中國共產黨全國代表大會觀察窗

## 資料結構

```text
data/events.json                 事件資料
scripts/build_calendar.py        產生 ICS
china-political-calendar.ics     可訂閱行事曆
.github/workflows/build.yml       自動重新產生與驗證
```

## 更新原則

1. 優先使用中國政府網、中國人大網、全國政協網、中央紀委國家監委網站、新華社等官方來源。
2. 未公布日期不得填成確定事件。
3. 多日會議的 ICS `DTEND` 採排他日期，確保行事曆正確顯示最後一天。
4. 日期異動時保留 UID，並提高 `SEQUENCE`。
5. 時區以中國標準時間／台灣時間（UTC+8）理解；全日事件不受時區換算影響。

## 手動產生

```bash
python scripts/build_calendar.py
```

## 重要限制

中國政治會議中，只有全國兩會等少數會議具有高度穩定的年度時段。中央全會、政治局會議、中央經濟工作會議等，正式日期通常在會前才公布，因此本行事曆會將推估內容明確標成觀察窗。