# coding: utf-8
import copy

from handright._util import *

_DEFAULT_END_CHARS = "，。》？；：’”】｝、！％）,.>?;:]}!%)′″℃℉"
_DEFAULT_PERTURB_THETA_SIGMA = 0.07
_DEFAULT_WORD_SPACING = 0
_DEFAULT_LEFT_MARGIN = 0
_DEFAULT_TOP_MARGIN = 0
_DEFAULT_RIGHT_MARGIN = 0
_DEFAULT_BOTTOM_MARGIN = 0


class Template(object):
    """The parameter class for `handright.handwrite()`."""

    def __init__(
            self,
            background: PIL.Image.Image,
            font_size: int,
            font,
            line_spacing: Optional[int] = None,
            fill=None,
            left_margin: int = _DEFAULT_LEFT_MARGIN,
            top_margin: int = _DEFAULT_TOP_MARGIN,
            right_margin: int = _DEFAULT_RIGHT_MARGIN,
            bottom_margin: int = _DEFAULT_BOTTOM_MARGIN,
            word_spacing: int = _DEFAULT_WORD_SPACING,
            line_spacing_sigma: Optional[float] = None,
            font_size_sigma: Optional[float] = None,
            word_spacing_sigma: Optional[float] = None,
            end_chars: str = _DEFAULT_END_CHARS,
            perturb_x_sigma: Optional[float] = None,
            perturb_y_sigma: Optional[float] = None,
            perturb_theta_sigma: float = _DEFAULT_PERTURB_THETA_SIGMA,
    ):
        """Note that, all the Integer parameters are in pixels.

        Although, it provides some reasonable default values for some
        parameters, it is strongly recommended to explicitly set these
        parameters according to the characteristic of a particular task.

        `font` should be a Pillow's font instance. However, the size attribute
        of it will be ignored here.

        `fill` is the pixel value filled to the background as font color, e.g.
        `(255, 0, 0)` for the backgrounds with RGB mode and `0` for the
        backgrounds with L mode.

        `word_spacing` can be less than `0`, but must be greater than
        `-font_size // 2`.

        `line_spacing_sigma`, `font_size_sigma` and `word_spacing_sigma` are the
        sigmas of the gauss distributions of line spacing, font size and word
        spacing, respectively.

        `end_chars` is the collection of Chars which cannot be placed in the
        beginning of a line.

        `perturb_x_sigma`, `perturb_y_sigma` and `perturb_theta_sigma` are the
        sigmas of the gauss distributions of the horizontal position, the
        vertical position and the rotation of strokes, respectively.
        """
        self.set_background(background)
        self.set_font_size(font_size)
        self.set_line_spacing(line_spacing)
        self.set_font(font)
        self.set_fill(fill)
        self.set_left_margin(left_margin)
        self.set_top_margin(top_margin)
        self.set_right_margin(right_margin)
        self.set_bottom_margin(bottom_margin)
        self.set_word_spacing(word_spacing)
        self.set_line_spacing_sigma(line_spacing_sigma)
        self.set_font_size_sigma(font_size_sigma)
        self.set_word_spacing_sigma(word_spacing_sigma)
        self.set_end_chars(end_chars)
        self.set_perturb_x_sigma(perturb_x_sigma)
        self.set_perturb_y_sigma(perturb_y_sigma)
        self.set_perturb_theta_sigma(perturb_theta_sigma)

    def __eq__(self, other) -> bool:
        return (isinstance(other, Template)
                and self.get_background() == other.get_background()
                and self.get_line_spacing() == other.get_line_spacing()
                and self.get_line_spacing_sigma() == other.get_line_spacing_sigma()
                and self.get_font_size() == other.get_font_size()
                and self.get_font_size_sigma() == other.get_font_size_sigma()
                and self.get_font() == other.get_font()
                and self.get_fill() == other.get_fill()
                and self.get_left_margin() == other.get_left_margin()
                and self.get_top_margin() == other.get_top_margin()
                and self.get_right_margin() == other.get_right_margin()
                and self.get_bottom_margin() == other.get_bottom_margin()
                and self.get_word_spacing() == other.get_word_spacing()
                and self.get_word_spacing_sigma() == other.get_word_spacing_sigma()
                and self.get_end_chars() == other.get_end_chars()
                and self.get_perturb_x_sigma() == other.get_perturb_x_sigma()
                and self.get_perturb_y_sigma() == other.get_perturb_y_sigma()
                and self.get_perturb_theta_sigma() == other.get_perturb_theta_sigma())

    def set_background(self, background: PIL.Image.Image) -> None:
        self._background = background

    def set_font_size(self, font_size: int) -> None:
        self._font_size = font_size

    def set_line_spacing(self, line_spacing: Optional[int] = None) -> None:
        if line_spacing is None:
            self._line_spacing = self._font_size
        else:
            self._line_spacing = line_spacing

    def set_font(self, font) -> None:
        self._font = font

    def set_fill(self, fill=None) -> None:
        if fill is None:
            n_bands = count_bands(self._background.mode)
            if n_bands == 1:
                self._fill = 0
            else:
                self._fill = (0,) * n_bands
        else:
            self._fill = fill

    def set_left_margin(self, left_margin: int = _DEFAULT_LEFT_MARGIN) -> None:
        self._left_margin = left_margin

    def set_top_margin(self, top_margin: int = _DEFAULT_TOP_MARGIN) -> None:
        self._top_margin = top_margin

    def set_right_margin(self, right_margin: int = _DEFAULT_RIGHT_MARGIN) -> None:
        self._right_margin = right_margin

    def set_bottom_margin(self, bottom_margin: int = _DEFAULT_BOTTOM_MARGIN) -> None:
        self._bottom_margin = bottom_margin

    def set_word_spacing(self, word_spacing: int = _DEFAULT_WORD_SPACING) -> None:
        self._word_spacing = word_spacing

    def set_line_spacing_sigma(self, line_spacing_sigma: Optional[float] = None) -> None:
        if line_spacing_sigma is None:
            self._line_spacing_sigma = self._font_size / 32
        else:
            self._line_spacing_sigma = line_spacing_sigma

    def set_font_size_sigma(self, font_size_sigma: Optional[float] = None) -> None:
        if font_size_sigma is None:
            self._font_size_sigma = self._font_size / 64
        else:
            self._font_size_sigma = font_size_sigma

    def set_word_spacing_sigma(self, word_spacing_sigma: Optional[float] = None) -> None:
        if word_spacing_sigma is None:
            self._word_spacing_sigma = self._font_size / 32
        else:
            self._word_spacing_sigma = word_spacing_sigma

    def set_end_chars(self, end_chars: str = _DEFAULT_END_CHARS) -> None:
        self._end_chars = end_chars

    def set_perturb_x_sigma(self, perturb_x_sigma: Optional[float] = None) -> None:
        if perturb_x_sigma is None:
            self._perturb_x_sigma = self._font_size / 32
        else:
            self._perturb_x_sigma = perturb_x_sigma

    def set_perturb_y_sigma(self, perturb_y_sigma: Optional[float] = None) -> None:
        if perturb_y_sigma is None:
            self._perturb_y_sigma = self._font_size / 32
        else:
            self._perturb_y_sigma = perturb_y_sigma

    def set_perturb_theta_sigma(self, perturb_theta_sigma: float = _DEFAULT_PERTURB_THETA_SIGMA) -> None:
        self._perturb_theta_sigma = perturb_theta_sigma

    def get_background(self) -> PIL.Image.Image:
        return self._background

    def get_line_spacing(self) -> int:
        return self._line_spacing

    def get_font_size(self) -> int:
        return self._font_size

    def get_font(self):
        return self._font

    def get_fill(self):
        return self._fill

    def get_left_margin(self) -> int:
        return self._left_margin

    def get_top_margin(self) -> int:
        return self._top_margin

    def get_right_margin(self) -> int:
        return self._right_margin

    def get_bottom_margin(self) -> int:
        return self._bottom_margin

    def get_word_spacing(self) -> int:
        return self._word_spacing

    def get_line_spacing_sigma(self) -> float:
        return self._line_spacing_sigma

    def get_font_size_sigma(self) -> float:
        return self._font_size_sigma

    def get_word_spacing_sigma(self) -> float:
        return self._word_spacing_sigma

    def get_end_chars(self) -> str:
        return self._end_chars

    def get_perturb_x_sigma(self) -> float:
        return self._perturb_x_sigma

    def get_perturb_y_sigma(self) -> float:
        return self._perturb_y_sigma

    def get_perturb_theta_sigma(self) -> float:
        return self._perturb_theta_sigma

    def get_size(self) -> Tuple[int, int]:
        return self.get_background().size


def copy_templates(templates: Iterable[Template]) -> Tuple[Template, ...]:
    return tuple(map(copy.copy, templates))
