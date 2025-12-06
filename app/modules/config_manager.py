"""
Config Manager - Handles detection and management of multiple Hyprland config files.

This module provides utilities to:
- Detect the main config file and any sourced files
- Display information about config files being used
- Ensure proper handling of multi-file configurations
"""
import os
from pathlib import Path

# HyprData import moved to functions to prevent crash on missing config


def expand_path(path: str) -> str:
    """Expand environment variables and ~ in a path."""
    return os.path.expanduser(os.path.expandvars(path))


def get_config_files_info() -> list[dict]:
    """
    Get information about all config files being used.
    
    Returns:
        List of dicts with keys: 'path', 'expanded_path', 'exists', 'is_main'
    """
    files_info = []
    
    # Import HyprData lazily
    try:
        from ..imports import HyprData
    except ImportError:
        from hyprparser import HyprData

    # Get main config path
    main_path = HyprData.path if hasattr(HyprData, 'path') else None
    
    # Get all files from hyprparser
    if hasattr(HyprData, 'files') and HyprData.files:
        for i, file in enumerate(HyprData.files):
            file_path = file.path if hasattr(file, 'path') else str(file)
            expanded = expand_path(file_path)
            is_main = (i == 0) or (expanded == expand_path(main_path) if main_path else False)
            
            files_info.append({
                'path': file_path,
                'expanded_path': expanded,
                'exists': os.path.exists(expanded),
                'is_main': is_main,
                'index': i,
            })
    
    # If no files found, try to get from main path
    if not files_info and main_path:
        expanded = expand_path(main_path)
        files_info.append({
            'path': main_path,
            'expanded_path': expanded,
            'exists': os.path.exists(expanded),
            'is_main': True,
            'index': 0,
        })
    
    return files_info


def get_main_config_path() -> str:
    """Get the expanded path to the main config file."""
    files_info = get_config_files_info()
    if files_info:
        # Find main file
        for info in files_info:
            if info['is_main']:
                return info['expanded_path']
        # If no main marked, return first
        return files_info[0]['expanded_path']
    
    # Fallback to default
    default = expand_path("$HOME/.config/hypr/hyprland.conf")
    return default


def get_config_summary() -> str:
    """
    Get a human-readable summary of config files being used.
    
    Returns:
        String describing the config setup
    """
    files_info = get_config_files_info()
    
    if not files_info:
        return "No config files detected"
    
    main_file = next((f for f in files_info if f['is_main']), files_info[0])
    other_files = [f for f in files_info if not f['is_main']]
    
    summary = f"Main config: {main_file['expanded_path']}"
    if not main_file['exists']:
        summary += " (not found)"
    
    if other_files:
        summary += f"\nSourced files ({len(other_files)}):"
        for f in other_files:
            summary += f"\n  - {f['expanded_path']}"
            if not f['exists']:
                summary += " (not found)"
    
    return summary


def check_config_files() -> dict:
    """
    Check the status of all config files.
    
    Returns:
        Dict with 'valid', 'main_exists', 'missing_files', 'total_files'
    """
    files_info = get_config_files_info()
    
    if not files_info:
        return {
            'valid': False,
            'main_exists': False,
            'missing_files': [],
            'total_files': 0,
            'message': 'No config files detected'
        }
    
    main_file = next((f for f in files_info if f['is_main']), files_info[0])
    missing = [f for f in files_info if not f['exists']]
    
    return {
        'valid': main_file['exists'],
        'main_exists': main_file['exists'],
        'missing_files': [f['expanded_path'] for f in missing],
        'total_files': len(files_info),
        'sourced_files': len([f for f in files_info if not f['is_main']]),
        'message': get_config_summary()
    }

DEFAULT_CONFIG_URL = "https://raw.githubusercontent.com/hyprwm/Hyprland/main/example/hyprland.conf"


def download_default_config(target_path: str = None) -> bool:
    """
    Download the default Hyprland config from GitHub and save it.
    
    Args:
        target_path: Path to save config to. If None, uses default location.
        
    Returns:
        True if successful, False otherwise.
    """
    import urllib.request
    import shutil
    
    if target_path is None:
        target_path = expand_path("$HOME/.config/hypr/hyprland.conf")
        
    target_path = os.path.abspath(expand_path(target_path))
    target_dir = os.path.dirname(target_path)
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Download and save
        with urllib.request.urlopen(DEFAULT_CONFIG_URL) as response, open(target_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        print(f"Successfully downloaded default config to {target_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading default config: {e}")
        return False
