import os
import shutil
import sys


class FileManipulator:

    VALID_OPERATIONS = ["reverse", "copy", "duplicate-contents", "replace-string"]

    # 操作名とパスの存在をチェックし、インスタンス変数に設定
    def __init__(self, operation, input_path, output_path=None):
        if operation not in self.VALID_OPERATIONS:
            raise ValueError(f"無効な操作です: {operation}")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"入力ファイルが存在しません: {input_path}")
        self.operation = operation
        self.input_path = input_path
        self.output_path = output_path

    # ファイルの内容を逆順で読み込み・書き込み
    def reverse(self):
        with open(self.input_path, "r") as f:
            data = f.read()
        with open(self.ensure_output(), "w") as f:
            f.write(data[::-1])

    # ファイルを指定先にコピー
    def copy(self):
        shutil.copyfile(self.input_path, self.ensure_output())

    # ファイル内容を指定回数だけ複製して上書き保存
    def duplicate_contents(self, times):
        with open(self.input_path, "r") as f:
            data = f.read()
        with open(self.input_path, "w") as f:
            for _ in range(times):
                f.write(data)

    # ファイル内の文字列を検索・置換し上書き保存
    def replace_string(self, needle, new_string):
        with open(self.input_path, "r") as f:
            data = f.read()
        with open(self.input_path, "w") as f:
            f.write(data.replace(needle, new_string))

    # コマンドに応じて適切なメソッドを呼び出し
    def execute(self, *args):
        if self.operation == "reverse":
            self.reverse()
        elif self.operation == "copy":
            self.copy()
        elif self.operation == "duplicate-contents":
            times = int(args[0])
            self.duplicate_contents(times)
        elif self.operation == "replace-string":
            needle, new_string = args
            self.replace_string(needle, new_string)

    # output_pathの設定をチェックし、返却
    def ensure_output(self):
        if not self.output_path:
            raise ValueError("output_path が必要です")
        return self.output_path

# 引数の数・操作・ファイル存在を検証し、メッセージを表示
def validate_arguments(args):
    if len(args) < 4:
        print("引数が足りません。")
        return False
    if args[1] not in FileManipulator.VALID_OPERATIONS:
        print("無効な操作です。")
        return False
    if not os.path.exists(args[2]):
        print("入力ファイルが存在しません。")
        return False
    op = args[1]
    if op == "duplicate-contents" and len(args) < 5:
        print("duplicate-contents には複製回数が必要です。")
        return False
    if op == "replace-string" and len(args) < 6:
        print("replace-string には置換対象文字列と新しい文字列が必要です。")
        return False
    return True


def main():
    args = sys.argv
    if not validate_arguments(args):
        sys.exit(1)

    operation = args[1]
    input_path = args[2]
    output_path = args[3]

    manipulator = FileManipulator(operation, input_path, output_path)

    if operation == "duplicate-contents":
        times = int(args[4])
        manipulator.execute(times)
    elif operation == "replace-string":
        needle = args[4]
        new_string = args[5]
        manipulator.execute(needle, new_string)
    else:
        manipulator.execute()


if __name__ == "__main__":
    main()
