import pytest
from ..utils import slugify


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Hello World", "hello-world"),
        ("FastAPI_is Great!", "fastapi_is-great"),
        ("  leading and trailing  ", "leading-and-trailing"),
        ("Multiple---dashes___and__underscores", "multiple-dashes___and__underscores"),
        ("Symbols!@# and $%^ punctuation", "symbols-and-punctuation"),
        ("MiXeD CaSe and   Spacing", "mixed-case-and-spacing"),
        ("", ""),
        ("---only symbols---", "only-symbols"),
        ("Already-slugified-text", "already-slugified-text"),
    ],
)
def test_slugify(input_text, expected):
    assert slugify(input_text) == expected


def test_slugify_does_not_mutate_input():
    original = "Keep THIS Safe!"
    _ = slugify(original)
    assert original == "Keep THIS Safe!"
