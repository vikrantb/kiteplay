from setuptools import find_packages, setup

setup(
    name="kiteplay",
    packages=find_packages(exclude=["kiteplay_tests"]),
    install_requires=[
        "dagster", # Dagster
        "dagster-cloud", # Dagster Cloud
        "duckdb", # DuckDB
        "dagster-duckdb", # DuckDB
        "dagster-webserver", # Dagster UI
        "requests",  # API calls
        "openai",  # ChatGPT, DALL-E API
        "pillow",  # Image processing
        "moviepy",  # Video processing
        "ffmpeg-python",  # Video editing and composition
        "moviepy",  # Video editing
        "imageio[ffmpeg]",  # Video I/O"
        "pydub",  # Audio processing
        "elevenlabs",  # AI voiceover
    ],
    extras_require={
        "dev": [
            "pytest",
            "dagster-webserver",  # Dagster UI
            "black",  # Code formatting
            "flake8",  # Linting
        ]
    },
)