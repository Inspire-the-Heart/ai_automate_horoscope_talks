import os
import json
import sys
import traceback

from Vionix.utils.logger import get_logger

from Vionix.pipeline.daily_horoscope import HoroscopeMultiLangJsonGenerator
from Vionix.pipeline.daily_horoscope_pipeline import DailyHoroscopePipeline  # <-- change if your path differs

logger = get_logger(__name__)

LANG_KEYS = ["te", "ta", "kn", "ml", "bn", "mr", "hi"]


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    try:
        # ------------------------------------------------------------
        # 1) LOAD CONFIGS (AI generation configs)
        # ------------------------------------------------------------
        meta_cfg_path = os.getenv("VIONIX_CONFIG_META", "./app_config_horoscope_meta.json")
        signs_cfg_path = os.getenv("VIONIX_CONFIG_SIGNS", "./app_config_horoscope_signs.json")

        meta_cfg = load_config(meta_cfg_path)
        signs_cfg = load_config(signs_cfg_path)

        # ------------------------------------------------------------
        # 2) GENERATE / LOAD FINAL JSONS (7 files)
        # ------------------------------------------------------------
        logger.info("🧠 Step 1: Generating / Loading Horoscope JSONs...")
        pipeline = HoroscopeMultiLangJsonGenerator(meta_cfg, signs_cfg)
        pipeline.run()



        # ------------------------------------------------------------
        # 4) LOOP EACH LANGUAGE JSON -> CREATE VIDEO
        # ------------------------------------------------------------
        logger.info("🎬 Step 2: Rendering 7 videos from generated JSONs...")

        for lang in LANG_KEYS:
            json_file = f"horoscope_{lang}.json"
            if not os.path.exists(json_file):
                raise Exception(f"Missing JSON file: {json_file}")
            # ------------------------------------------------------------
            # 3) VIDEO CONFIG
            # ------------------------------------------------------------
            video_cfg_path = os.getenv("VIONIX_CONFIG_VIDEO", f"./app_config_horoscope_{lang}_sm.json")
            video_cfg = load_config(video_cfg_path)

            cfg = dict(video_cfg)

            # Force load local JSON (no AI here)
            cfg["horoscope"] = dict(cfg.get("horoscope", {}))
            cfg["horoscope"]["enabled"] = False
            cfg["horoscope"]["file"] = json_file

            # Output mp4 per language
            cfg["video_file"] = f"daily_horoscope_{lang}.mp4"

            logger.info(f"➡️ Rendering: {lang} | JSON={json_file} | MP4={cfg['video_file']}")
            DailyHoroscopePipeline(cfg).run()

        logger.info("✅ DONE: All 7 videos generated successfully.")

    except Exception:
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
