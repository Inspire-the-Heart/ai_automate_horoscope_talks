import os
import json
from Vionix.pipeline.daily_horoscope import HoroscopeMultiLangJsonGenerator
# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    meta_cfg_path = os.getenv("VIONIX_CONFIG_META", "../../tests/app_config_horoscope_meta.json")
    signs_cfg_path = os.getenv("VIONIX_CONFIG_SIGNS", "../../tests/app_config_horoscope_signs.json")

    meta_cfg = load_config(meta_cfg_path)
    signs_cfg = load_config(signs_cfg_path)

    pipeline = HoroscopeMultiLangJsonGenerator(meta_cfg, signs_cfg)
    pipeline.run()


if __name__ == "__main__":
    main()