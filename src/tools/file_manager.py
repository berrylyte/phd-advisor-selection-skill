"""
File Manager
Handle progress.md and tracker.md persistence
"""

from pathlib import Path
from typing import Dict


class FileManager:
    """Manage reading and writing progress files"""

    @staticmethod
    def read_progress_md(file_path: Path) -> str:
        """Read progress markdown file"""
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return ""

    @staticmethod
    def write_progress_md(file_path: Path, content: str) -> bool:
        """Write progress markdown file"""
        try:
            file_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return False

    @staticmethod
    def read_tracker(file_path: Path) -> str:
        """Read email tracker file"""
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return "# Email & Application Tracker\n\n"

    @staticmethod
    def append_to_tracker(file_path: Path, entry: str) -> bool:
        """Append entry to tracker file"""
        try:
            current = FileManager.read_tracker(file_path)
            current += f"\n{entry}"
            file_path.write_text(current, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error appending to {file_path}: {e}")
            return False
