# Optional: MLOps pipeline using tools like MLflow for tracking and monitoring models

import mlflow
from mlflow import sklearn

def log_model(model, run_name="resume_ranker"):
    mlflow.start_run(run_name=run_name)
    
    # Log the model
    mlflow.sklearn.log_model(model, "model")
    
    mlflow.end_run()

# Example usage:
# log_model(trained_model)
