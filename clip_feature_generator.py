import boto3
import clip
import torch
import math
import numpy as np
import pandas as pd
from PIL import Image
import shutil
import os
from functools import lru_cache

@lru_cache(maxsize=1) # lazy loading
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return clip.load("ViT-B/32", device=device)
# 0- model
# 1 - preproces





