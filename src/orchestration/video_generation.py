import logging

from dagster import Definitions, AssetExecutionContext, asset
from pathlib import Path
import yaml


# --- Asset 1: Load a concept plan from YAML ---
@asset(description="Load a concept plan from YAML file")
def load_concept_plan(context: AssetExecutionContext) -> dict:
    """
    Loads a concept plan YAML file (e.g., a Chanakya Neeti principle) into a Python dictionary.
    """
    plan_path = Path("plans/video_plan_001.yml")
    if not plan_path.exists():
        raise FileNotFoundError(f"Concept plan not found: {plan_path}")

    context.log.info(f"Loading concept plan from {plan_path}")
    with open(plan_path, "r") as f:
        data = yaml.safe_load(f)

    return data

# --- Asset 2: Generate script from concept plan ---
@asset(description="Generate a script from the concept plan", deps=[load_concept_plan])
def generate_script(load_concept_plan: dict) -> str:
    """
    Generates a script based on the concept plan.
    """
    saying = load_concept_plan.get("content", {}).get("saying")
    story = load_concept_plan.get("content", {}).get("story")
    application = load_concept_plan.get("content", {}).get("real_life_application")

    script = f"Saying: {saying}\nStory: {story}\nHow it applies: {application}"
    return script

# --- Asset 3: Generate visuals from script ---
@asset
def generate_visuals(generate_script: str) -> str:
    """
    Generates visual placeholders based on the script.
    """
    return generate_script + "visuals_generated.png"

# --- Asset 4: Generate voiceover from script ---
@asset
def generate_voiceover(generate_script: str) -> str:
    """
    Generates voiceover placeholder from script.
    """
    return generate_script + "voiceover_generated.mp3"

# --- Asset 5: Compose final video ---
@asset
def compose_video(generate_voiceover: str, generate_visuals: str) -> str:
    """
    Combines voiceover and visuals into a video.
    """
    logging.info("Composing final video..." + generate_voiceover + generate_visuals + "final_video.mp4")
    print("Composing final video..." + generate_voiceover + generate_visuals + "final_video.mp4")
    return generate_voiceover + generate_visuals + "final_video.mp4"
