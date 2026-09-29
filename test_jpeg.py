from PIL import Image

STEGO_IMAGE = "test_results/image_1_4000B.png"
JPEG_IMAGE = "test_results/image_1_4000B.jpg"

# Buka stego image
image = Image.open(STEGO_IMAGE).convert("RGB")

# Simpan ulang sebagai JPEG
image.save(JPEG_IMAGE, "JPEG", quality=95)

print("Stego PNG :", STEGO_IMAGE)
print("JPEG      :", JPEG_IMAGE)
print("JPEG berhasil dibuat.")