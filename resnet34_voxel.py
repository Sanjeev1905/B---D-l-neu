import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Define paths
data_path = '/mnt/data/work/ml_hawaii/test_b2dstar/B2Dslnu_070726/generated_voxel_images'
dataset_dir = '/mnt/data/work/ml_hawaii/test_b2dstar/B2Dslnu_070726/imagedatafor_CNN2'
output_dir = '/mnt/data/work/ml_hawaii/test_b2dstar/B2Dslnu_070726/results'
os.makedirs(output_dir, exist_ok=True)
# Check if dataset directory exists, and create train, test, val splits if not
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir, exist_ok=True)
    for sub_dir in ['train', 'test', 'val']:
        os.makedirs(os.path.join(dataset_dir, sub_dir), exist_ok=True)

    # Get all .npy files
    all_files = [f for f in os.listdir(data_path) if f.endswith('.npy')]

    # Split data: 76 train & 12 %validation, 12% test
    train_files, temp_files = train_test_split(all_files, test_size=0.24, random_state=42)  # 24% left for test + val
    val_files, test_files = train_test_split(temp_files, test_size=0.5, random_state=42)  # Split 24% into 12% each

    # Move files to the dataset directories
    for file in train_files:
        shutil.copy(os.path.join(data_path, file), os.path.join(dataset_dir, 'train', file))
    for file in test_files:
        shutil.copy(os.path.join(data_path, file), os.path.join(dataset_dir, 'test', file))
    for file in val_files:
        shutil.copy(os.path.join(data_path, file), os.path.join(dataset_dir, 'val', file))

    print("Dataset directory created with train, test, and val splits.")
else:
    print("Dataset directory already exists. Skipping creation of train, test, val splits.")

# Custom data generator for regression on three parameters
class CustomDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, data_path, batch_size=64, input_size=(50, 50, 50, 1), shuffle=True):
        self.data_path = data_path
        self.batch_size = batch_size
        self.input_size = input_size
        self.file_list = os.listdir(data_path)
        self.shuffle = shuffle
        self.on_epoch_end()
    
    def _load_data(self, file):
        data = np.load(os.path.join(self.data_path, file))
        X = data  # 3D voxel image
        parts = file.replace(".npy", "").split("_") 
        gL = float(parts[0])
        gR = float(parts[1])
        gP = float(parts[2])
        
        y = [gL, gR, gP]
        return X, y

    def __getitem__(self, index):
        batch_files = self.file_list[index * self.batch_size:(index + 1) * self.batch_size]
        X_batch, y_batch = [], []
        for file in batch_files:
            X, y = self._load_data(file)
            X_batch.append(X)
            y_batch.append(y)
        
        X_batch = np.array(X_batch).reshape(-1, *self.input_size)
        y_batch = np.array(y_batch)
        return X_batch, y_batch

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.file_list)

    def __len__(self):
        return int(np.floor(len(self.file_list) / self.batch_size))

# Residual block with 3 convolution layers
def residual_block(input_tensor, filters, strides=1):
    X = keras.layers.Conv3D(filters, kernel_size=3, strides=strides, padding="same")(input_tensor)
    X = keras.layers.BatchNormalization()(X)
    X = keras.layers.Activation("relu")(X)

    X = keras.layers.Conv3D(filters, kernel_size=3, padding="same")(X)
    X = keras.layers.BatchNormalization()(X)
    X = keras.layers.Activation("relu")(X)

    X = keras.layers.Conv3D(filters, kernel_size=3, padding="same")(X)
    X = keras.layers.BatchNormalization()(X)

    shortcut = input_tensor
    if strides != 1 or input_tensor.shape[-1] != filters:
        shortcut = keras.layers.Conv3D(filters, kernel_size=1, strides=strides, padding="same")(input_tensor)
        shortcut = keras.layers.BatchNormalization()(shortcut)

    X = keras.layers.Add()([X, shortcut])
    X = keras.layers.Activation("relu")(X)
    return X

# ResNet-34 Model Definition
def build_resnet34(input_shape=(50, 50, 50, 1)):
    inputs = keras.layers.Input(shape=input_shape)
    
    # Initial convolutional layer
    X = keras.layers.Conv3D(64, kernel_size=3, strides=2, padding="same")(inputs)
    X = keras.layers.BatchNormalization()(X)
    X = keras.layers.Activation("relu")(X)
    # Max pooling layer immediately after input convolution
    X = keras.layers.MaxPooling3D(pool_size=3, strides=2, padding="same")(X)

    # Residual blocks with [3, 4, 6, 3] configurations
    for filters, reps, strides in zip([64, 128, 256, 512], [3, 4, 6, 3], [1, 2, 2, 2]):
        for block in range(reps):
            X = residual_block(X, filters, strides if block == 0 else 1)  # Strides only for the first block

    X = keras.layers.GlobalAveragePooling3D()(X)
    X = keras.layers.Dense(2000, activation="relu")(X)
    X = keras.layers.Dropout(0.2)(X)  # Dropout after dense layer
    outputs = keras.layers.Dense(3, activation="linear")(X)  # Three outputs for regression

    model = keras.Model(inputs, outputs)
    return model

# Compile model
model = build_resnet34()
# Learning Rate Scheduler
lr_schedule = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',  # Metric to monitor
    factor=0.5,          # Reduce learning rate by this factor
    patience=5,          # Number of epochs with no improvement to wait
    min_lr=1e-8,         # Minimum learning rate
    verbose=1            # Print updates to learning rate
)

model.compile(optimizer=keras.optimizers.Adam(1e-5), loss="mse", metrics=[tf.keras.metrics.RootMeanSquaredError()])

# Print model summary for verification
model.summary()
# Data Generators for train, validation, and test
train_gen = CustomDataGenerator(data_path=os.path.join(dataset_dir, 'train'), batch_size=16, shuffle=True)
val_gen = CustomDataGenerator(data_path=os.path.join(dataset_dir, 'val'), batch_size=16, shuffle=True)
test_gen = CustomDataGenerator(data_path=os.path.join(dataset_dir, 'test'), batch_size=16, shuffle=True)

# Callbacks
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    os.path.join(output_dir, "best_model.keras"),
    save_best_only=True
)
early_stopping_cb = keras.callbacks.EarlyStopping(
    patience=50,
    restore_best_weights=True
)

# List of callbacks
callbacks = [checkpoint_cb, early_stopping_cb, lr_schedule]


# Training
history = model.fit(train_gen, validation_data=val_gen, epochs=80, callbacks=callbacks)
# Evaluate on the test dataset
test_loss, test_rmse = model.evaluate(test_gen, verbose=1)

print(f"Test MSE  : {test_loss:.6f}")
print(f"Test RMSE : {test_rmse:.6f}")

# Plot training history
plt.figure(figsize=(10, 6))
pd.DataFrame(history.history).plot()
plt.title("Training History")
plt.xlabel("Epochs")
plt.ylabel("validation Loss")
plt.ylim(0, 0.03)  # Clip the loss axis to a maximum value of 0.03
plt.grid()
plt.savefig(os.path.join(output_dir, "training_history.png"))

# Predictions and evaluation on test data
y_true, y_pred = [], []
for file in test_gen.file_list:
    X, y = test_gen._load_data(file)
    y_true.append(y)
    y_pred.append(model.predict(X.reshape(1, 50, 50, 50, 1)).flatten())

y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Residual plot
params = ["g_L", "g_R", "g_P"]

for i, param in enumerate(params):

    residual = y_pred[:, i] - y_true[:, i]

    plt.figure(figsize=(6,5))

    plt.scatter(y_true[:, i], residual, alpha=0.7)

    plt.axhline(0, color='red', linestyle='--')

    plt.xlabel(f"True {param}")
    plt.ylabel("Residual (Prediction - Truth)")
    plt.title(f"Residual Plot ({param})")

    plt.grid(True)

    plt.savefig(os.path.join(output_dir,
                f"{param}_residual_plot.png"))
    plt.close()
    
#Residual histogram
params = ["g_L", "g_R", "g_P"]

for i, param in enumerate(params):

    residual = y_pred[:, i] - y_true[:, i]

    plt.figure(figsize=(6,5))

    plt.hist(residual,
             bins=30,
             edgecolor='black')

    plt.axvline(0, color='red', linestyle='--')

    plt.xlabel("Residual")
    plt.ylabel("Counts")
    plt.title(f"Residual Distribution ({param})")

    plt.grid(True)

    plt.savefig(os.path.join(output_dir,
                f"{param}_residual_hist.png"))
    plt.close()
    
# error histogram
params = ["g_L", "g_R", "g_P"]

for i, param in enumerate(params):

    error = np.abs(y_pred[:, i] - y_true[:, i])

    plt.figure(figsize=(6,5))

    plt.hist(error,
             bins=30,
             edgecolor='black')

    plt.xlabel("Absolute Error")
    plt.ylabel("Counts")
    plt.title(f"Absolute Error ({param})")

    plt.grid(True)

    plt.savefig(os.path.join(output_dir,
                f"{param}_absolute_error.png"))
    plt.close()
    

# Plot predicted vs actual for each parameter
for i, param in enumerate(["g_L", "g_R", "g_P"]):
    plt.figure()
    plt.scatter(y_true[:, i], y_pred[:, i], label=f"Predicted vs Actual {param}")
    plt.plot([y_true[:, i].min(), y_true[:, i].max()], [y_true[:, i].min(), y_true[:, i].max()], 'k--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"Predicted vs Actual for {param}")
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"predicted_vs_actual_{param}.png"))

# Plot average prediction
# Calculate the average and standard deviation for each unique actual value
for i, param in enumerate(["g_L", "g_R", "g_P"]):
    unique_actuals = np.unique(y_true[:, i])
    avg_predictions = []
    std_predictions = []
    for actual in unique_actuals:
        indices = np.where(y_true[:, i] == actual)[0]
        avg_predictions.append(np.mean(y_pred[indices, i]))
        std_predictions.append(np.std(y_pred[indices, i]))
    

    # Plot average predicted vs actual for each parameter with error bars
    mse = mean_squared_error(y_true[:, i], y_pred[:, i])
    rmse = np.sqrt(mse)
    plt.text(
    0.05, 0.95,
    f"MSE  = {mse:.5e}\nRMSE = {rmse:.5e}",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment='top',
    bbox=dict(facecolor='white', alpha=0.8)
    )
    plt.figure()
    plt.errorbar(unique_actuals, avg_predictions, yerr=std_predictions, fmt='o', label=f"Average Predicted {param}", capsize=5)
    plt.plot([unique_actuals.min(), unique_actuals.max()], [unique_actuals.min(), unique_actuals.max()], 'k--')
    plt.xlabel("Actual Value")
    plt.ylabel("Average Predicted Value")
    plt.title(f"Average Predicted vs Actual for {param} with Standard Deviation Error Bars")
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"average_prediction_with_error_bars_{param}.png"))

print("Training and evaluation completed. Plots saved.")
