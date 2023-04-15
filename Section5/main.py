import sys

from ingest import ingest
from qa import generate_answer

def _ingest(file_path: str):
    print(f"ファイルを取り込みます: {file_path}")
    ingest(file_path)

def _qa(question: str):
    print(f"質問に回答します: {question}")
    generate_answer(question)

def _show_help():
    help_text = """
使い方:
  python main.py [コマンド] [引数]

コマンド:
  ingest {file_path}   指定したファイルを取り込む
  qa {question}        指定した質問の回答を求める
  --help               このヘルプを表示する
    """
    print(help_text)

def main():
    if len(sys.argv) < 2:
        print("エラー: コマンドが指定されていません")
        _show_help()
        return

    command = sys.argv[1]

    if command == "ingest":
        if len(sys.argv) < 3:
            print("エラー: ファイルパスが指定されていません")
            _show_help()
        else:
            file_path = sys.argv[2]
            _ingest(file_path)
    elif command == "qa":
        if len(sys.argv) < 3:
            print("エラー: 質問が指定されていません")
            _show_help()
        else:
            question = sys.argv[2]
            _qa(question)
    elif command == "--help":
        _show_help()
    else:
        print("エラー: 無効なコマンドです")
        _show_help()


if __name__ == "__main__":
    main()
