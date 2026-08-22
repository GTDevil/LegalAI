"""Standalone entry point for the LegalAI Loan Settlement Agent server."""

import argparse
import webbrowser

import uvicorn

from app.main import app


def main() -> None:
    parser = argparse.ArgumentParser(description="LegalAI Loan Settlement Agent")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open API docs in the default browser after startup",
    )
    args = parser.parse_args()

    if args.open_browser:
        webbrowser.open(f"http://{args.host}:{args.port}/docs")

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
