# tools/file_organizer.py
"""
File organizer tool - Simple file management capabilities
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from tools.base_tool import BaseTool, register_tool


class FileOrganizerTool(BaseTool):
    """
    Simple file organization tool for basic file management
    """

    def __init__(self):
        super().__init__(
            name="file_organizer",
            description="Organizes files by type, finds duplicates, creates folder structure",
        )

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute file organization actions

        Actions:
            - 'analyze': Analyze a folder structure
            - 'organize': Organize files by type
            - 'create_folders': Create folder structure
        """
        try:
            if action == "analyze":
                return self._analyze_folder(kwargs.get("folder_path", "."))
            elif action == "organize":
                return self._organize_by_type(kwargs.get("folder_path", "."))
            elif action == "create_folders":
                return self._create_folders(
                    kwargs.get("folder_path", "."), kwargs.get("folders", [])
                )
            else:
                return {"success": False, "error": f"Unknown action: {action}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _analyze_folder(self, folder_path: str) -> Dict[str, Any]:
        """Analyze folder contents and structure"""
        path = Path(folder_path)

        if not path.exists():
            return {"success": False, "error": "Folder does not exist"}

        files = []
        folders = []
        file_types = {}

        for item in path.iterdir():
            if item.is_file():
                files.append(str(item.name))
                ext = item.suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
            elif item.is_dir():
                folders.append(str(item.name))

        return {
            "success": True,
            "result": {
                "total_files": len(files),
                "total_folders": len(folders),
                "file_types": file_types,
                "files": files[:10],  # First 10 files only
                "folders": folders,
            },
        }

    def _organize_by_type(self, folder_path: str) -> Dict[str, Any]:
        """Organize files by their type into subfolders"""
        path = Path(folder_path)

        # Define file type categories
        categories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        }

        moved_files = {}

        for item in path.iterdir():
            if item.is_file():
                ext = item.suffix.lower()

                # Find category for this file type
                category = "Other"
                for cat, extensions in categories.items():
                    if ext in extensions:
                        category = cat
                        break

                # Create category folder if it doesn't exist
                category_path = path / category
                category_path.mkdir(exist_ok=True)

                # Move file to category folder
                new_path = category_path / item.name
                if not new_path.exists():  # Avoid overwriting
                    shutil.move(str(item), str(new_path))
                    moved_files[str(item.name)] = category

        return {
            "success": True,
            "result": {
                "moved_files": moved_files,
                "categories_created": list(categories.keys()) + ["Other"],
            },
        }

    def _create_folders(
        self, base_path: str, folder_names: List[str]
    ) -> Dict[str, Any]:
        """Create a list of folders in the base path"""
        path = Path(base_path)
        created = []

        for folder_name in folder_names:
            folder_path = path / folder_name
            if not folder_path.exists():
                folder_path.mkdir(parents=True)
                created.append(folder_name)

        return {"success": True, "result": {"created_folders": created}}


# Register the tool when module is imported
file_organizer_tool = FileOrganizerTool()
register_tool(file_organizer_tool)
