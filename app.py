import pyautogui
import pyperclip
import time
import re

print("===== クリップボード退避＆復元マクロ 完全版 起動完了 =====")
print("TurboWarpからの指示を待っています...")

temporary_clipboard = ""
last_text = ""

while True:
    try:
        current_text = pyperclip.paste()
        
        if current_text != last_text and current_text.startswith("turbowarp_cmd:"):
            last_text = current_text
            cmd_data = current_text.replace("turbowarp_cmd:", "").strip()
            
            # カンマで細かく分割する
            parts = [p.strip() for p in cmd_data.split(",")]
            
            # --- 1. ダブルクリックの処理 (例: click,double,1500,20) ---
            if parts[0] == "click" and len(parts) >= 2 and parts[1] == "double":
                if len(parts) >= 4:  # 座標（X, Y）まである場合
                    x = int(parts[2])
                    y = int(parts[3])
                    pyautogui.doubleClick(x, y)
                    print(f"【実行】指定座標をダブルクリック: X={x}, Y={y}")
                else:
                    pyautogui.doubleClick()
                    print("【実行】現在の位置をダブルクリック")

            # --- 2. 通常クリックの処理 (例: click,1500,20) ---
            elif parts[0] == "click":
                if len(parts) >= 3:  # 座標（X, Y）がある場合
                    x = int(parts[1])
                    y = int(parts[2])
                    pyautogui.click(x, y)
                    print(f"【実行】指定座標をクリック: X={x}, Y={y}")
                else:
                    pyautogui.click()
                    print("【実行】現在の位置をクリック")
            
            # --- 3. 文章の一括入力処理 (例: write"こんにちは！") ---
            elif parts[0].startswith("write"):
                match = re.search(r'"([^"]+)"', cmd_data)
                if match:
                    text_to_write = match.group(1)
                    old_clip = temporary_clipboard
                    pyperclip.copy(text_to_write)
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.05)
                    temporary_clipboard = old_clip
                    print(f"【実行】文章を入力しました: {text_to_write}")
                    
            # --- 4. 単体・同時キー入力の処理 (例: key"Y") ---
            elif parts[0].startswith("key"):
                match = re.search(r'"([^"]+)"', cmd_data)
                if match:
                    key_content = match.group(1)
                    if "+" in key_content:
                        keys = [k.strip().lower() for k in key_content.split("+")]
                        pyautogui.hotkey(*keys)
                        print(f"【実行】キー同時押し: {' + '.join(keys)}")
                    else:
                        pyautogui.press(key_content.lower())
                        print(f"【実行】キー入力: {key_content.lower()}")
                
            # クリップボードを元の状態（Temporary）に戻す
            pyperclip.copy(temporary_clipboard)
            last_text = temporary_clipboard
            
        elif not current_text.startswith("turbowarp_cmd:") and current_text != last_text:
            temporary_clipboard = current_text
            last_text = current_text

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        
    time.sleep(0.1)
