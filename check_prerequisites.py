#!/usr/bin/env python3
"""Check prerequisites for CAD Agents system."""

import sys
import logging
import platform
import subprocess
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is 3.10 or higher."""
    python_version = sys.version_info
    logger.info(f"Current Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        logger.error("❌ Python 3.10 or higher is required for this project")
        logger.info("\nInstallation instructions for Python 3.10 or higher:")
        
        if platform.system() == "Darwin":  # macOS
            logger.info("""
On macOS:
1. Using Homebrew (recommended):
   $ brew install python@3.10
   
2. Using the official installer:
   Download from https://www.python.org/downloads/

After installation, create a new virtual environment using Python 3.10:
   $ /path/to/python3.10 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -e .
""")
        elif platform.system() == "Linux":
            logger.info("""
On Linux:
1. Ubuntu/Debian:
   $ sudo apt update
   $ sudo apt install python3.10 python3.10-venv python3.10-dev
   
2. Fedora:
   $ sudo dnf install python3.10
   
3. Using pyenv (recommended for any Linux distribution):
   $ curl https://pyenv.run | bash
   $ pyenv install 3.10.0
   $ pyenv local 3.10.0
   
After installation, create a new virtual environment using Python 3.10:
   $ python3.10 -m venv .venv
   $ source .venv/bin/activate
   $ pip install -e .
""")
        elif platform.system() == "Windows":
            logger.info("""
On Windows:
1. Using the official installer (recommended):
   Download from https://www.python.org/downloads/
   
2. Using winget:
   $ winget install -e --id Python.Python.3.10
   
After installation, create a new virtual environment using Python 3.10:
   $ py -3.10 -m venv .venv
   $ .venv\\Scripts\\activate
   $ pip install -e .
""")
        
        return False
    else:
        logger.info("✅ Python version is 3.10 or higher")
        return True

def check_freecad_mcp():
    """Check if FreeCAD MCP submodule is available."""
    root_dir = Path(__file__).parent
    mcp_dir = root_dir / "freecad-mcp"
    
    if not mcp_dir.exists():
        logger.error("❌ FreeCAD MCP directory not found at %s", mcp_dir)
        logger.info("""
To clone the freecad-mcp submodule:
   $ git submodule update --init --recursive
""")
        return False
    
    logger.info("✅ FreeCAD MCP submodule found")
    return True

def check_mcp_package():
    """Check if MCP package is installed."""
    try:
        import mcp
        logger.info(f"✅ MCP package is installed (version {mcp.__version__})")
        return True
    except ImportError:
        logger.error("❌ MCP package is not installed")
        logger.info("""
To install the MCP package:
   $ pip install mcp>=0.3.0
""")
        return False
    except AttributeError:
        # If __version__ is not available
        logger.info("✅ MCP package is installed (version unknown)")
        return True

def main():
    """Run all checks."""
    logger.info("Checking prerequisites for CAD Agents system...\n")
    
    python_check = check_python_version()
    if not python_check:
        logger.error("\n❌ Prerequisites check failed - Python version requirement not met")
        return False
    
    freecad_mcp_check = check_freecad_mcp()
    
    if python_check:
        # Only check for MCP package if Python version is correct
        mcp_check = check_mcp_package()
    else:
        mcp_check = False
    
    if python_check and freecad_mcp_check and mcp_check:
        logger.info("\n✅ All prerequisites met!")
        return True
    else:
        logger.error("\n❌ Prerequisites check failed - please address the issues above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 