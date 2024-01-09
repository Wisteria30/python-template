from typing import Literal

from pydantic import BaseModel

from .common import Document, Range


class Diagnostic(BaseModel):
    message: str
    severity: Literal["error", "warn", "info", "hint"]
    range: Range


class DiagnosticsInput(BaseModel):
    """
    {
        "repo_name": "hello-world",  // string, 必須

        "instruction": "xxx の部分を重点的にレビューしてください", // string, 必須

        // object, 必須
        // 現在編集中のファイルの情報
        "current_doc": {
            "name": "README.md",  // string, 必須
            "content": "# Hello World\n\nファイルの中身",  // string, 必須
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

    instruction: str
    repo_name: str
    current_doc: Document
    relevant_docs: list[Document]


class DiagnosticsOutput(BaseModel):
    """
    {
        "success": true,  // boolean, 必須

        // array
        "diagnostics": [
            {
                "message": "スペルミスしています"  // string, 必須

                // "error" | "warn" | "info" | "hint", 必須
                // コンパイルエラーとかを出すわけではないので、基本 warn 以下になる？
                "severity": "warn",

                // object, 必須
                // 対象ファイルのどの箇所に問題があるかを示す。
                // LLM は文字数を数えられないので、range を正しく出すのに工夫がいるかもしれない。
                // 行数さえ合っていれば多少ズレててもまあ良し？
                "range": {   // object, 必須
                    "start": {   // object, 必須
                        "line": 1,  // int, 必須
                        "character": 2,  // int, 必須
                    },
                    "end": {   // object, 必須
                        "line": 1,  // int, 必須
                        "character": 10,  // int, 必須
                    }
                }
            },
            // ...
        ]
    }
    """

    success: bool
    diagnostics: list[Diagnostic]
