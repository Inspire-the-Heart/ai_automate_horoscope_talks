import os
import json
import sys
import traceback

from Vionix.utils.logger import get_logger
from Vionix.pipeline.daily_horoscope_pipeline import DailyHoroscopePipeline

logger = get_logger(__name__)

ALL_LANGS = ["te", "ta", "kn", "ml", "bn", "mr", "hi"]


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    try:
        # ✅ Get lang from CLI OR env
        lang = None

        if len(sys.argv) > 1:
            lang = sys.argv[1].strip().lower()

        if not lang:
            lang = os.getenv("LANGUAGE", "").strip().lower()

        if lang not in ALL_LANGS:
            raise Exception(f"Invalid lang '{lang}'. Allowed: {ALL_LANGS}")

        json_file = f"horoscope_{lang}.json"
        if not os.path.exists(json_file):
            raise Exception(f"Missing JSON file: {json_file}")

        video_cfg_path = os.getenv(
            "VIONIX_CONFIG_VIDEO",
            f"./app_config_horoscope_{lang}_sm.json"
        )

        video_cfg = load_config(video_cfg_path)
        cfg = dict(video_cfg)

        # Force local JSON
        cfg["horoscope"] = dict(cfg.get("horoscope", {}))
        cfg["horoscope"]["enabled"] = False
        cfg["horoscope"]["file"] = json_file

        cfg["video_file"] = f"daily_horoscope_{lang}.mp4"

        logger.info(f"➡️ Rendering: {lang} -> {cfg['video_file']}")
        DailyHoroscopePipeline(cfg).run()

        logger.info("✅ DONE")

    except Exception:
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
