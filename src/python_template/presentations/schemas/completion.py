from pydantic import BaseModel

from .common import Completion, CurrentDocument, Document


class CompletionInput(BaseModel):
    """
    {
        "repo_name": "hello-world",  // string, 必須

        // object, 必須
        // 現在編集中のファイルの情報
        "current_doc": {
            "name": "README.md",  // string, 必須
            "content": "# Hello World\n\nファイルの中身",  // string, 必須

            // object, 必須
            // カーソルの位置
            "position": {
                "line": 2,  // int, 必須
                "character": 10  // int, 必須
            }
        },

        // object, 必須
        // プロジェクト内の別ファイルの情報
        // 20 件ぐらいに制限する
        "relevant_docs": [
            {
                // string, 必須
                "name": "src/main.py",
                // string, 必須
                "content": "import os\n\n\n\ndef main():\n    print(\"Hello World\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
            },
            {
                "name": "src/foo.py",
                "content": "..."
            },
            // ...
        ]
    }
    """

    repo_name: str
    current_doc: CurrentDocument
    relevant_docs: list[Document]


class CompletionOutput(BaseModel):
    """
    {
        "success": true, // boolean, 必須
        // array
        // 同じプロンプトに対して並列で複数生成させてユーザーに選ばせることも可能なので、配列にしておく。
        "completions": [
            {
                "text": "補完テキスト1"  // string, 必須
            },
            {
                "text": "補完テキスト2"
            }
        ]
    }
    """

    success: bool
    completions: list[Completion]
