"""Education-only comparison: same synthetic data, same held-out test set.
No pretrained models or large model weights are stored.
"""
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 42
EPOCHS = 30
OUT = Path(__file__).resolve().parent / "results"


def scores(y, probs):
    pred = (np.asarray(probs).reshape(-1) >= 0.5).astype(int)
    return {
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "f1": round(float(f1_score(y, pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y, probs)), 4),
    }


def main():
    import torch
    from torch import nn
    import tensorflow as tf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    np.random.seed(SEED)
    torch.manual_seed(SEED)
    tf.keras.utils.set_random_seed(SEED)
    torch.set_num_threads(1)

    x, y = make_classification(
        n_samples=1200, n_features=12, n_informative=8, n_redundant=2,
        n_classes=2, weights=[0.5, 0.5], flip_y=0.02, random_state=SEED,
    )
    xtr, xte, ytr, yte = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=SEED
    )
    scaler = StandardScaler()
    xtr = scaler.fit_transform(xtr).astype("float32")
    xte = scaler.transform(xte).astype("float32")

    lr = LogisticRegression(max_iter=1000, random_state=SEED)
    lr.fit(xtr, ytr)
    results = {"LogisticRegression": scores(yte, lr.predict_proba(xte)[:, 1])}

    # PyTorch: two hidden layers and binary logit loss, CPU only.
    net = nn.Sequential(nn.Linear(12, 24), nn.ReLU(),
                        nn.Linear(24, 12), nn.ReLU(), nn.Linear(12, 1))
    optimizer = torch.optim.Adam(net.parameters(), lr=0.005)
    loss_fn = nn.BCEWithLogitsLoss()
    tx = torch.tensor(xtr)
    ty = torch.tensor(ytr.astype("float32")).reshape(-1, 1)
    net.train()
    for _ in range(EPOCHS):
        optimizer.zero_grad()
        loss = loss_fn(net(tx), ty)
        loss.backward()
        optimizer.step()
    net.eval()
    with torch.no_grad():
        probs = torch.sigmoid(net(torch.tensor(xte))).numpy().ravel()
    results["PyTorch"] = scores(yte, probs)

    # TensorFlow/Keras: comparable architecture; independent random initialization.
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(12,)),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(12, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
                  loss="binary_crossentropy")
    model.fit(xtr, ytr, epochs=EPOCHS, batch_size=len(xtr), shuffle=False, verbose=0)
    results["TensorFlow"] = scores(yte, model.predict(xte, verbose=0).ravel())

    payload = {
        "status": "executed_locally_not_independently_verified",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": "scikit-learn synthetic make_classification; not real-world data",
        "seed": SEED,
        "n_total": len(y),
        "n_train": len(ytr),
        "n_test": len(yte),
        "train_test_split": "80/20 stratified, fixed seed",
        "scaling": "StandardScaler fitted on train only",
        "training": {"epochs": EPOCHS, "device": "CPU", "torch_batch": "full",
                     "tensorflow_batch": "full", "architecture": "12-24-12-1"},
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scikit_learn": sklearn.__version__, "pytorch": torch.__version__,
                     "tensorflow": tf.__version__},
        "metrics": results,
        "limitations": [
            "Synthetic educational data only",
            "One train/test split and one initialization per neural network",
            "Different frameworks do not share initialized weights",
            "Not a lottery or news prediction model",
        ],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    models = list(results)
    values = [results[name]["f1"] for name in models]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(models, values)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Held-out F1 score")
    ax.set_title("Synthetic data: test F1 by model")
    fig.text(0.02, 0.01, "Source: generated synthetic data | 1200 rows | seed 42 | test n=240", fontsize=8)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(OUT / "compare.png", dpi=120)
    fig.savefig(OUT / "compare.svg")
    plt.close(fig)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("Saved:", OUT / "metrics.json")


if __name__ == "__main__":
    main()
