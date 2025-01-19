import matplotlib.pyplot as plt

# ファイルを読み込んで線で出力する関数
def plot_hilbert_curve_from_file(filename):
    points = []
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("Area"):
                try:
                    # "Area (x, y)" の形式を解析
                    start_idx = line.find("(")  # 最初の "(" の位置
                    end_idx = line.rfind(")")  # 最後の ")" の位置
                    if start_idx != -1 and end_idx != -1:
                        position = line[start_idx + 1 : end_idx]  # 中身を抽出
                        x, y = map(float, position.split(","))
                        points.append((x, y))
                except Exception as e:
                    print(f"Skipping invalid line: {line.strip()} | Error: {e}")

    if points:
        # 点を線で結ぶ
        x_vals, y_vals = zip(*points)
        plt.figure(figsize=(6, 6))
        plt.plot(x_vals, y_vals, marker="o", linestyle="-", color="blue")
        plt.title("Hilbert Curve")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.show()
    else:
        print("No valid points found in the file.")

# プログラム例
if __name__ == "__main__":
    plot_hilbert_curve_from_file("output.txt")
