"""DNA fragment classification demo using two NCBI RefSeq genomes.

Creates 1,000 ten-base fragments per reference genome, extracts six features,
trains a Decision Tree, evaluates a stratified holdout, and predicts the
assignment sequence. Requires internet access for first-time genome download.
"""
import random
import requests
import pandas as pd
import numpy as np
from io import StringIO
from Bio import SeqIO
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.dummy import DummyClassifier

SEED = 42
FRAGMENT_LENGTH = 10
SAMPLES_PER_GROUP = 1000
GENOMES = {
    "Group A": "NC_000913.3",  # Escherichia coli K-12 MG1655
    "Group B": "NC_000908.2",  # Mycoplasma genitalium G37
}
FEATURES = ["A_count", "T_count", "G_count", "C_count", "Length", "GC_percent"]
UNKNOWN = "ATGCGCGATC"

def fetch_genome(accession):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    response = requests.get(url, params={
        "db": "nuccore", "id": accession, "rettype": "fasta", "retmode": "text"
    }, timeout=90)
    response.raise_for_status()
    record = SeqIO.read(StringIO(response.text), "fasta")
    return str(record.seq).upper()

def fragments(sequence):
    sequence = "".join(x for x in sequence if x in "ATGC")
    return [
        sequence[i:i + FRAGMENT_LENGTH]
        for i in range(0, len(sequence) - FRAGMENT_LENGTH + 1, FRAGMENT_LENGTH)
        if len(sequence[i:i + FRAGMENT_LENGTH]) == FRAGMENT_LENGTH
    ]

def extract(sequence):
    counts = {base: sequence.count(base) for base in "ATGC"}
    length = len(sequence)
    return {
        "A_count": counts["A"], "T_count": counts["T"],
        "G_count": counts["G"], "C_count": counts["C"],
        "Length": length,
        "GC_percent": 100 * (counts["G"] + counts["C"]) / length,
    }

def main():
    random.seed(SEED)
    np.random.seed(SEED)
    records = []
    for group, accession in GENOMES.items():
        pool = fragments(fetch_genome(accession))
        if len(pool) < SAMPLES_PER_GROUP:
            raise RuntimeError(f"Not enough fragments for {group}")
        chosen = random.sample(pool, SAMPLES_PER_GROUP)
        for index, sequence in enumerate(chosen, 1):
            records.append({
                "Sequence_ID": f"{group.replace(' ', '')}_{index:04d}",
                "DNA_Sequence": sequence, "Group": group, **extract(sequence)
            })

    df = pd.DataFrame(records).sample(frac=1, random_state=SEED).reset_index(drop=True)
    df.to_csv("dna_sequence_dataset.csv", index=False)
    X, y = df[FEATURES], df["Group"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify=y
    )
    model = DecisionTreeClassifier(max_depth=4, random_state=SEED)
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    print(f"Test accuracy: {accuracy_score(y_test, predicted):.4%}")
    print("Confusion matrix (Group A, Group B):")
    print(confusion_matrix(y_test, predicted, labels=["Group A", "Group B"]))
    print(classification_report(y_test, predicted))
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    print(f"Majority baseline: {accuracy_score(y_test, baseline.predict(X_test)):.4%}")
    print("Feature importance:")
    print(pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False))
    unknown_features = pd.DataFrame([extract(UNKNOWN)])[FEATURES]
    print(f"Unknown: {UNKNOWN}")
    print("Prediction:", model.predict(unknown_features)[0])
    print("Probabilities:", dict(zip(model.classes_, model.predict_proba(unknown_features)[0])))

if __name__ == "__main__":
    main()
