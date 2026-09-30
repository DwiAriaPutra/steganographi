from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Membaca citra cover dan stego
cover = Image.open("images/image_1.png").convert("RGB")
stego = Image.open("test_results/image_1_4000B.png").convert("RGB")

cover = np.asarray(cover)
stego = np.asarray(stego)

# Menghitung histogram setiap channel RGB
def histogram(image):
    return [
        np.bincount(image[:, :, channel].ravel(), minlength=256)
        for channel in range(3)
    ]

hist_cover = histogram(cover)
hist_stego = histogram(stego)

# Membuat grafik perbandingan
plt.figure(figsize=(10, 5))

for i, color in enumerate(["R", "G", "B"]):
    plt.plot(
        range(256), hist_cover[i],
        label=f"{color} Cover"
    )
    plt.plot(
        range(256), hist_stego[i],
        linestyle="--",
        label=f"{color} Stego"
    )

plt.title("Perbandingan Histogram Cover dan Stego")
plt.xlabel("Intensitas Piksel")
plt.ylabel("Jumlah Piksel")
plt.legend(ncol=3)
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()