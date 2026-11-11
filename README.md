# DNA Sequence Classification Using Machine Learning

An educational supervised-learning project that classifies short DNA fragments into two groups using nucleotide-composition features and a Decision Tree.

## Objective
Train a model on labelled DNA fragments and predict the group of the unknown sequence `ATGCGCGATC`.

## Dataset
A balanced dataset of 2,000 non-overlapping 10-base fragments was created from two NCBI RefSeq reference genomes:

| Label | Organism | RefSeq accession | Samples |
|---|---|---|---:|
| Group A | Escherichia coli K-12 MG1655 | NC_000913.3 | 1,000 |
| Group B | Mycoplasma genitalium G37 | NC_000908.2 | 1,000 |

Sources: [NCBI NC_000913.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3) and [NCBI NC_000908.2](https://www.ncbi.nlm.nih.gov/nuccore/NC_000908.2).

Each fragment is represented by A, T, G, C counts, sequence length, and GC percentage. Ambiguous-base fragments are excluded. The dataset has 1,000 samples per group.

**Scientific caveat:** fragments come from only one reference genome per group. A random fragment-level split is not independent-genome validation; performance may reflect genome-specific GC composition rather than general biological signals.

## Model and measured results
- Model: scikit-learn Decision Tree, `max_depth=4`, `random_state=42`
- Split: stratified 80% train / 20% test, `random_state=42`
- Test accuracy: **73.75%** (295 / 400 correct)
- Majority-class baseline: 50.00%

Confusion matrix (rows = actual; columns = predicted; order A, B):

| | Predicted A | Predicted B |
|---|---:|---:|
| Actual A | 146 | 54 |
| Actual B | 51 | 149 |

Unknown sequence `ATGCGCGATC` is predicted as **Group A** (estimated model probabilities: 84.65% A, 15.35% B). The true label is not supplied, so correctness cannot be checked.

## Files
- `main.py` - downloads RefSeq genomes, creates the dataset, extracts features, trains/evaluates the model, and predicts the unknown sequence.
- `requirements.txt` - Python dependencies.
- `results/metrics.json` - recorded metrics from the supplied CSV and fixed model configuration.
- `dna_sequence_dataset.csv` - dataset used for the reported metrics.
- `results.pdf` - academic report supplied with the project submission.

## Run
Install dependencies and run:

```bash
pip install -r requirements.txt
python main.py
```

An internet connection is required for the first run because the script downloads reference FASTA records from NCBI E-utilities.

## Limitations
1. Only one reference genome represents each group.
2. Ten-base fragments lose sequence order and biological context.
3. GC percentage is derived from G and C counts, so features are correlated.
4. Random fragment splitting does not test generalisation to independent genomes.
5. This educational model is not suitable for clinical diagnosis or definitive organism identification.

## Genomics application
Composition-based classification can be a basic exploratory step when comparing sequence fragments with labelled references. Practical genomic identification requires broader datasets, sequence-aware methods, and independent validation.
