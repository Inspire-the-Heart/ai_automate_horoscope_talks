import json
import sys

from Vionix.pipeline.daily_horoscope_pipeline import DailyHoroscopePipeline
from Vionix.utils.logger import get_logger
from Vionix.utils.exceptions import VionixError

logger = get_logger()



def load_config(path="app_config_horoscope_mh_sm.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        logger.error(f"Config file not found at {path}")
        raise VionixError(f"Config file not found at {path}")

    except Exception as e:
        logger.exception("Failed to load config")
        raise VionixError(f"Failed to load config: {e}") from e


def main():
    try:
        print("\n🚀 Starting Vionix Daily Horoscope Pipeline...")

        cfg = load_config()

        pipeline = DailyHoroscopePipeline(cfg)
        output = pipeline.run()

        print("\n✅ Final video created at:", output)
        logger.info(f"Final output: {output}")

    except VionixError as e:
        logger.error("Pipeline terminated: " + str(e))
        print("\n❌ Pipeline terminated. Check logs.")
        sys.exit(1)

    except Exception as e:
        logger.exception("Unhandled error in main")
        print("\n❌ Unexpected failure. Check logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
