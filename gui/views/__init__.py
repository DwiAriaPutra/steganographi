"""
Isi tiap tab GUI.

- ``embed_tab``    : form embed message
- ``extract_tab``  : form extract message
- ``analysis_tab`` : pratinjau, metrik, histogram, LSB
"""

from .analysis_tab import AnalysisTab

from .embed_tab import EmbedTab

from .extract_tab import ExtractTab

from .histogram_view import HistogramView

from .lsb_view import LsbView


__all__ = [
    "EmbedTab",
    "ExtractTab",
    "AnalysisTab",
    "HistogramView",
    "LsbView",
]
