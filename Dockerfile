# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 必要ファイルをコピー
COPY file_manipulator.py .
COPY input.txt .

# デフォルトでは何もしないで待機
CMD ["tail", "-f", "/dev/null"]
