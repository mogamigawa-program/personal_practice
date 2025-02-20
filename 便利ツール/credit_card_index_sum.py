import pandas as pd

# CSVファイルを読み込む（適宜ファイル名を変更してください）
file_path = input("CSVファイルのパスを入力してください: ").strip('"')

try:
    # Shift_JISエンコーディングで読み込む
    df = pd.read_csv(file_path, header=None, encoding="shift_jis")

    # 2列目の項目ごとの合計金額を計算
    summary = df.groupby(1)[2].sum().reset_index()

    # 結果を表示
    print("\n支出合計:")
    print(summary.to_string(index=False))

    # 出力ファイル名の入力を受け付ける
    output_path = file_path.replace(".csv", "_summary.csv")
    summary.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\n集計結果を {output_path} に保存しました。")

except UnicodeDecodeError:
    print("エンコーディングエラー: UTF-8またはShift_JIS以外のエンコーディングの可能性があります。")
    print("Excelで開いて、UTF-8またはShift_JISで保存し直してみてください。")
except FileNotFoundError:
    print("ファイルが見つかりません。パスを確認してください。")
except Exception as e:
    print(f"予期しないエラーが発生しました: {e}")

