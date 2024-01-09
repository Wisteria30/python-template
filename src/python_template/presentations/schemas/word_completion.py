from pydantic import BaseModel

from .common import Completion, CurrentDocument


class WordCompletionInput(BaseModel):
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
                "character": 6  // int, 必須
            }
        },
    }
    """

    repo_name: str
    current_doc: CurrentDocument


class WordCompletionOutput(BaseModel):
    """
    {
        "success": true, // boolean, 必須
        // array

        "completions": [
            {
                "text": "補完単語1"  // string, 必須,
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
            {
                "text": "補完単語2",
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
            }
        ]
    }
    """

    success: bool
    completions: list[Completion]
