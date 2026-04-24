"""Application entry point for the clock project."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from controllers.appController import AppController


def main() -> int:
    """Create the Qt application and start the event loop."""
    app = QApplication(sys.argv)

    controller = AppController()
    controller.showMainWindow()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
