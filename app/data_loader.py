# Load YAML files into memory so backend can serve /verses and /daily quickly.
import yaml, os, glob, hashlib, datetime, pytz

DATA_DIR = os.environ.get("DATA_DIR","data/yaml/siva_sutra")

def load_all():
    out = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.yml"))):
        with open(path, "r", encoding="utf-8") as f:
            item = yaml.safe_load(f)
            item["_id"] = os.path.splitext(os.path.basename(path))[0]
            out.append(item)
    return out

ALL_VERSES = load_all()

def pick_daily(user_id="guest", tz="Europe/Paris"):
    if not ALL_VERSES:
        return None
    now = datetime.datetime.now(pytz.timezone(tz))
    key = f"{now.year}-{now.month}-{now.day}-{user_id}"
    h = hashlib.sha1(key.encode()).hexdigest()
    idx = int(h,16) % len(ALL_VERSES)
    return ALL_VERSES[idx]
