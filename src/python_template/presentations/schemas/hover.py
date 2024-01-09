from pydantic import BaseModel

from .common import CurrentDocument, Range


class HoverInfo(BaseModel):
    text: str
    range: Range


class HoverInput(BaseModel):
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
    }
    """

    repo_name: str
    current_doc: CurrentDocument


class HoverOutput(BaseModel):
    """
    {
        "success": true, // boolean, 必須

        // object | null | undefined
        // カーソル位置に紐づく情報が特に無い場合は null | undefined
        "info": {
            // string, 必須
            // ツールチップに表示されるテキスト
            "text": "Markdown テキスト [リンク](https://example.com)",

            // カーソル位置の単語の範囲
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
    }
    """

    success: bool
    info: HoverInfo | None
