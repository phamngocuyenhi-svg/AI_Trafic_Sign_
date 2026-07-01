# Vietnamese Traffic Sign Detection

Notebook-first project for Vietnamese traffic sign detection.

Main file:

```text
notebooks/vietnam_traffic_sign_detection_workflow.ipynb
```

The notebook contains the full workflow:

1. Problem definition
2. Imports and helper utilities
3. Data collection
4. Exploratory data analysis
5. Data cleaning
6. Data cleaning and class remapping
7. Balanced training data preparing
8. Model training
9. Model evaluation
10. Inference and camera command

Large generated artifacts are intentionally not committed: raw data, processed data, runs, weights, caches, outputs, and virtual environments.

The notebook uses the Kaggle `maitam/vietnamese-traffic-signs` dataset, removes invalid/duplicate data, remaps active classes, prepares a more balanced YOLO training split, then trains/evaluates YOLO.
