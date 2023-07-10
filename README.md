# ChooseCourses_NTUST
**用於112學年度時的選課系統**
用於"國立臺灣科技大學選課系統"之選課工具。每次登入後約可持續加選8小時，之後將被系統強制登出需再次手動登入。

## 功能說明：
 <img src="https://github.com/KenLo51/ChooseCourses_NTUST/blob/main/images/Screenshot%202023-01-01%20020738.png?raw=true" width="501" height="395" />  
由上而下，由左而右分別為:  

1. 上半區塊顯示課程，並勾選須加選課程  
2. 課程代碼可額外興新增課程  
3. "執行敘數量"設定重複加選時所開啟執行敘數量，越高則平均嘗試加選頻率越高  
4. "加選間隔"設定執行敘內每次加選時間間格(秒)  
5. "開始選課"(或"停止選課")用以開始或停止重複加選清單中勾選課程  
6. "選取全部"、"反向選取"與"刪除選取項目"為輔助選取課程工具  
7. "匯入帶選課程"從課程查詢系統匯入帶選清單  
8. "尚未登入"(或"成功登入")顯示登入狀態，點即可手動立即檢查登入狀態  
9. "Cookies來源"需選擇以登入瀏覽器，抓取Cookies資料以登入系統  
10. "重新載入Cookies"重新抓取Cookies資料  
11. "電腦抽選後選課"(或"課程加退選")選擇目前選課情形  

## 使用方法：  

1. 使用任一瀏覽器登入選課系統  
2. 啟動程式後依目前選課進度選取"電腦抽選後選課"或"課程加退選"，預設應為"課程加退選"  
3. 設定"Cookies來源"為1.所登入之瀏覽器  
4. 確認其左方是否從"尚未登入"轉換為"成功登入"，若否則重複1.~3.直至出現"成功登入"  
5. 從"匯入帶選課程"或"新增課程"加入課程至上方清單，並於清單中勾選所需加選課程  
6. 點擊"開始選課"即開始重複加選課程直到強制登出選課系統  

## 
1. browser-cookie3           0.16.2
2. requests                  2.28.1
