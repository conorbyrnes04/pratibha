"""Lexicon lemma validators and loader.

Reads ``data/lexicon/lemmas/*.yml`` and ``data/lexicon/index.yml``.
Import-safe: no FastAPI routes (routes live elsewhere).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LEXICON_ROOT = ROOT / "data" / "lexicon"

LemmaMaturity = Literal["structural_draft", "strong_draft", "canonical"]
RelatedRelation = Literal["related_as", "diverges_from", "rough_analogue"]
ScriptKey = Literal[
    "iast", "devanagari", "greek", "chinese", "pinyin", "arabic", "latin"
]


class RelatedLemma(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lemma_id: str
    relation: RelatedRelation
    note: Optional[str] = None

    @field_validator("lemma_id")
    @classmethod
    def _slug_lemma_id(cls, v: str) -> str:
        return _require_slug(v, "related.lemma_id")


class Sense(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    short: str
    etymology: Optional[str] = None
    traps: list[str] = Field(default_factory=list)
    traditions: list[str] = Field(default_factory=list)
    exemplars: list[str] = Field(default_factory=list)
    body: Optional[str] = None

    @field_validator("id")
    @classmethod
    def _sense_id(cls, v: str) -> str:
        v = v.strip()
        if not v or "." not in v:
            raise ValueError(f"sense id must look like '<lemma>.<sense>', got {v!r}")
        return v

    @field_validator("traditions", mode="before")
    @classmethod
    def _norm_traditions(cls, v: Any) -> list[str]:
        return _normalize_tags(v)


class Lemma(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    maturity: LemmaMaturity
    scripts: dict[str, str] = Field(default_factory=dict)
    aliases: list[str] = Field(default_factory=list)
    traditions: list[str] = Field(default_factory=list)
    related: list[RelatedLemma] = Field(default_factory=list)
    senses: list[Sense]

    @field_validator("id")
    @classmethod
    def _lemma_id(cls, v: str) -> str:
        return _require_slug(v, "id")

    @field_validator("scripts")
    @classmethod
    def _scripts(cls, v: dict[str, str]) -> dict[str, str]:
        allowed = {
            "iast",
            "devanagari",
            "greek",
            "chinese",
            "pinyin",
            "arabic",
            "latin",
        }
        out: dict[str, str] = {}
        for key, val in (v or {}).items():
            if key not in allowed:
                raise ValueError(f"unknown script key {key!r}; allowed={sorted(allowed)}")
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"script {key!r} must be a non-empty string")
            out[key] = val.strip()
        return out

    @field_validator("traditions", mode="before")
    @classmethod
    def _norm_traditions(cls, v: Any) -> list[str]:
        return _normalize_tags(v)

    @field_validator("senses")
    @classmethod
    def _nonempty_senses(cls, v: list[Sense]) -> list[Sense]:
        if not v:
            raise ValueError("lemma must have at least one sense")
        return v

    @model_validator(mode="after")
    def _sense_ids_match_lemma(self) -> "Lemma":
        for sense in self.senses:
            prefix = sense.id.split(".", 1)[0]
            if prefix != self.id:
                raise ValueError(
                    f"sense id {sense.id!r} must start with lemma id {self.id!r}"
                )
        return self


class LexiconIndexItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    short: str
    traditions: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        return _require_slug(v, "index.id")

    @field_validator("traditions", mode="before")
    @classmethod
    def _norm_traditions(cls, v: Any) -> list[str]:
        return _normalize_tags(v)


class LexiconIndex(BaseModel):
    model_config = ConfigDict(extra="ignore")

    lemmas: list[LexiconIndexItem] = Field(default_factory=list)


def _require_slug(v: str, field: str) -> str:
    s = (v or "").strip().lower()
    if not s:
        raise ValueError(f"{field} must be a non-empty slug")
    for ch in s:
        if not (ch.isalnum() or ch in "-_"):
            raise ValueError(
                f"{field} must be ascii slug (alnum/hyphen/underscore), got {v!r}"
            )
    if s != (v or "").strip():
        # allow exact lowercase already; reject uppercase
        if (v or "").strip() != s:
            raise ValueError(f"{field} must be lowercase, got {v!r}")
    return s


def _normalize_tags(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        v = [v]
    if not isinstance(v, list):
        raise ValueError("traditions must be a list of strings")
    out: list[str] = []
    for item in v:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"invalid tradition tag: {item!r}")
        tag = item.strip().lower().replace(" ", "_")
        out.append(tag)
    return out


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_lemma_file(path: Path | str) -> Lemma:
    data = _read_yaml(Path(path))
    if not isinstance(data, dict):
        raise ValueError(f"lemma file must be a mapping: {path}")
    return Lemma.model_validate(data)


def load_index(path: Path | str) -> LexiconIndex:
    data = _read_yaml(Path(path))
    if data is None:
        return LexiconIndex(lemmas=[])
    if not isinstance(data, dict):
        raise ValueError(f"index must be a mapping: {path}")
    return LexiconIndex.model_validate(data)


def load_lexicon(root: Path | str | None = None) -> dict[str, Any]:
    """Load all lemma YAMLs + index.

    Returns::
        {
          "root": str,
          "index": [LexiconIndexItem as dict, ...],
          "lemmas": {id: Lemma as dict, ...},
          "errors": [],  # raised instead; reserved for soft mode later
        }
    """
    lex_root = Path(root) if root is not None else DEFAULT_LEXICON_ROOT
    lemmas_dir = lex_root / "lemmas"
    index_path = lex_root / "index.yml"

    if not lemmas_dir.is_dir():
        raise FileNotFoundError(f"lexicon lemmas directory not found: {lemmas_dir}")

    lemmas: dict[str, Lemma] = {}
    for path in sorted(lemmas_dir.glob("*.yml")) + sorted(lemmas_dir.glob("*.yaml")):
        lemma = load_lemma_file(path)
        stem = path.stem
        if stem != lemma.id:
            raise ValueError(
                f"filename stem {stem!r} must match lemma id {lemma.id!r} ({path})"
            )
        if lemma.id in lemmas:
            raise ValueError(f"duplicate lemma id {lemma.id!r}")
        lemmas[lemma.id] = lemma

    index = load_index(index_path) if index_path.is_file() else LexiconIndex(lemmas=[])
    index_ids = {item.id for item in index.lemmas}
    lemma_ids = set(lemmas)

    missing_in_index = sorted(lemma_ids - index_ids)
    extra_in_index = sorted(index_ids - lemma_ids)
    if missing_in_index or extra_in_index:
        parts = []
        if missing_in_index:
            parts.append(f"missing from index: {missing_in_index}")
        if extra_in_index:
            parts.append(f"extra in index: {extra_in_index}")
        raise ValueError("index/lemma mismatch — " + "; ".join(parts))

    # Prefer index order when present.
    ordered_index = index.lemmas
    if not ordered_index:
        ordered_index = [
            LexiconIndexItem(
                id=lid,
                short=lemmas[lid].senses[0].short,
                traditions=list(lemmas[lid].traditions),
            )
            for lid in sorted(lemmas)
        ]

    return {
        "root": str(lex_root),
        "index": [item.model_dump() for item in ordered_index],
        "lemmas": {lid: lem.model_dump() for lid, lem in lemmas.items()},
        "errors": [],
    }
