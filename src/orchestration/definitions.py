from dagster import Definitions
from orchestration.video_generation import (
    load_concept_plan,
    generate_script,
    generate_visuals,
    generate_voiceover,
    compose_video,
)

defs = Definitions(
    assets=[
        load_concept_plan,
        generate_script,
        generate_visuals,
        generate_voiceover,
        compose_video,
    ]
)