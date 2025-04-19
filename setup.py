"""Legacy setup.py for backward compatibility.

This file is provided for backward compatibility with tools that don't yet support pyproject.toml.
For modern Python packaging, pyproject.toml is used.
"""

from setuptools import setup

setup(
    name="cad-agents",
    version="0.1.0",
    description="A system of agents designed to help engineers with CAD modeling tasks",
    python_requires=">=3.9",
    install_requires=[
        "google-adk>=0.2.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
    },
    packages=["cad_agents"],
) 