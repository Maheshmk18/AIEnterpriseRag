import os
from pathlib import Path

env_path = Path('backend/.env').absolute()
with open(env_path, 'r', encoding='utf-8') as f:
    print(f.read())
