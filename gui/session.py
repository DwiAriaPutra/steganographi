"""
State sesi GUI.

Menyimpan path gambar yang sedang dianalisis supaya
tab-tab bisa berbagi data tanpa saling mengimpor.
"""


class Session:
    """
    Pembawa state Cover/Stego image pada satu sesi GUI.
    """

    def __init__(self):

        self.cover_image = None

        self.stego_image = None

    def set_pair(
        self,
        cover_image,
        stego_image
    ):
        """
        Menyimpan pasangan cover + stego image hasil embed.
        """

        self.cover_image = cover_image

        self.stego_image = stego_image

    @property
    def is_ready(self):
        """
        True bila kedua gambar sudah tersedia.
        """

        return bool(
            self.cover_image
            and self.stego_image
        )
