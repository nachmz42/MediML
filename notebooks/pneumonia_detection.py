import os

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

test_dir = os.path.join(parent_dir, "raw_data", "chest_xray", "test")
train_dir = os.path.join(parent_dir, "raw_data", "chest_xray", "train")
val_dir = os.path.join(parent_dir, "raw_data", "chest_xray", "val")

