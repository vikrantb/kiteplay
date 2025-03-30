#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")"

echo "📁 Creating project structure..."

# Directories to create
dirs=(
  "batch_jobs"
  "config"
  "ingestion"
  "src/pipelines"
  "src/utils"
  "tests"
)

# Files to create (auto-generate __init__.py where appropriate)
files=(
  "config/openai_config.yaml"
  "config/settings.yaml"
  "ingestion/rss_watcher.py"
  "ingestion/task_queue_writer.py"
  "ingestion/topic_selector.py"

  "src/__init__.py"
  "src/configs.py"
  "src/definitions.py"

  "src/pipelines/__init__.py"
  "src/pipelines/publishing.py"
  "src/pipelines/video_generation.py"
  "src/pipelines/audio_generation.py"
  "src/pipelines/image_generation.py"
  "src/pipelines/scene_generation.py"
  "src/pipelines/script_generation.py"
  "src/pipelines/video_composition.py"

  "src/utils/__init__.py"
  "src/utils/api_utils.py"
  "src/utils/file_utils.py"
  "src/utils/prompt_utils.py"

  "tests/__init__.py"
  "tests/test_assets.py"

  ".gitignore"
  ".python-version"
  "main.py"
  "video_request.py"
  "README.md"
  "setup.py"
  "setup.cfg"
)

# Create directories
for dir in "${dirs[@]}"; do
  mkdir -p "$dir"
done

# Create files if not exist
for file in "${files[@]}"; do
  if [ ! -f "$file" ]; then
    touch "$file"
    echo "# Created $file" > "$file"
    echo "✅ $file created"
  fi
done

echo "✅ All folders and files are ready!"