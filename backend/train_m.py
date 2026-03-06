import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import json
import os

# ===============================
# CONFIG
# ===============================
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
DATASET_PATH = r"C:\Users\Nishita\Desktop\typ\dataset"
MODEL_DIR = "model"

os.makedirs(MODEL_DIR, exist_ok=True)

# ===============================
# DATA GENERATOR
# ===============================
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

NUM_CLASSES = train_generator.num_classes
print("Number of classes:", NUM_CLASSES)
print("Class indices:", train_generator.class_indices)

# ===============================
# SAVE CLASS NAMES (CRITICAL)
# ===============================
with open(os.path.join(MODEL_DIR, "class_names.json"), "w") as f:
    json.dump(train_generator.class_indices, f)

# ===============================
# MODEL
# ===============================
base_model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# TRAIN
# ===============================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# ===============================
# SAVE MODEL
# ===============================
model.save(os.path.join(MODEL_DIR, "breed_model.keras"))

print("✅ Training complete")
print("✅ Model saved to model/breed_model.keras")
print("✅ Class names saved to model/class_names.json")
