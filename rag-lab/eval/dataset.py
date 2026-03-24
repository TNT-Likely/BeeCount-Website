from __future__ import annotations

import json
from pathlib import Path

from common.models import EvalCase


def load_eval_dataset(path: Path) -> tuple[str, list[EvalCase]]:
    payload = json.loads(path.read_text(encoding='utf-8'))

    if isinstance(payload, list):
        return 'v0', [EvalCase.model_validate(item) for item in payload]

    version = payload.get('dataset_version', 'v0')
    cases = [EvalCase.model_validate(item) for item in payload.get('cases', [])]
    return version, cases
