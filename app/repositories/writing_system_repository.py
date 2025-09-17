from __future__ import annotations

import unicodedata as ud
from collections import Counter
from dataclasses import dataclass
from typing import Optional

import icu


@dataclass(frozen=True)
class WritingSystemDetectorConfig:
    noise_scripts: frozenset[str] = frozenset({"Zyyy", "Zinh", "Zzzz"})
    ignore_categories_prefixes: frozenset[str] = frozenset({"P", "S"})
    ignore_ascii_digits: bool = True
    max_extensions_per_char: int = 4
    min_useful_chars: int = 1


class WritingSystemDetector:
    def __init__(self, config: Optional[WritingSystemDetectorConfig] = None):
        self.cfg = config or WritingSystemDetectorConfig()

    def _is_noise_char(self, cp: int) -> bool:
        ch = chr(cp)

        if self.cfg.ignore_ascii_digits and "0" <= ch <= "9":
            return True

        cat = ud.category(ch)
        if cat and cat[0] in self.cfg.ignore_categories_prefixes:
            return True

        return False

    def _script_shortnames_from_extensions(self, cp: int) -> list[str]:
        exts = icu.Script.getScriptExtensions(cp)
        names = [icu.Script(e).getShortName() for e in exts]
        useful = [s for s in names if s not in self.cfg.noise_scripts]
        if 0 < self.cfg.max_extensions_per_char < len(useful):
            return []
        return useful

    def _scripts_in_text(self, text: str) -> Counter[str]:
        counts: Counter[str] = Counter()
        useful_chars = 0

        for cp in map(ord, text):
            if self._is_noise_char(cp):
                continue

            useful = self._script_shortnames_from_extensions(cp)
            if useful:
                counts.update(useful)
                useful_chars += 1

        if useful_chars < self.cfg.min_useful_chars:
            return Counter()

        return counts

    def detect(self, text: str) -> str:
        if not isinstance(text, str) or not text:
            raise ValueError("Input must be a non-empty string")

        counts = self._scripts_in_text(text)
        if not counts:
            raise ValueError("No valid scripts found in the input text")

        return counts.most_common(1)[0][0]


if __name__ == "__main__":
    print(WritingSystemDetector().detect("Hallo Welt"))