import os
import shutil

SOURCE_DIR = r"C:\Users\Nishita\Desktop\typ\dataset\clean_images"
DEST_DIR = r"C:\Users\Nishita\Desktop\typ\dataset"

os.makedirs(DEST_DIR, exist_ok=True)

animals = ["cattle", "buffalo"]
image_exts = (".jpg", ".jpeg", ".png")

total_copied = 0

for animal in animals:
    animal_path = os.path.join(SOURCE_DIR, animal)

    if not os.path.exists(animal_path):
        print(f"❌ Path not found: {animal_path}")
        continue

    for breed in os.listdir(animal_path):
        breed_path = os.path.join(animal_path, breed)

        if not os.path.isdir(breed_path):
            continue

        dest_breed_path = os.path.join(DEST_DIR, breed)
        os.makedirs(dest_breed_path, exist_ok=True)

        for img in os.listdir(breed_path):
            if img.lower().endswith(image_exts):
                src_img = os.path.join(breed_path, img)
                dst_img = os.path.join(dest_breed_path, img)

                shutil.copy(src_img, dst_img)
                total_copied += 1

print("✅ Dataset preparation complete")
print("📸 Total images copied:", total_copied)
