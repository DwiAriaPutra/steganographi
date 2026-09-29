"""
Entry point GUI.

Jalankan::

    python -m gui
"""

from .app import SteganographyApp


def main():
    """
    Menjalankan GUI sampai jendela ditutup.
    """

    SteganographyApp().run()


if __name__ == "__main__":

    main()
