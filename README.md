# DNA Sequence Classification Using Machine Learning

An educational supervised-learning project that classifies short DNA fragments into two groups using nucleotide-composition features and a Decision Tree.

## Objective
Train a model on labelled DNA fragments and predict the group of the unknown sequence `ATGCGCGATC`.

## Dataset
A balanced dataset of 2,000 non-overlapping 10-base fragments was generated from two NCBI RefSeq reference genomes:

| Label | Organism | RefSeq accession | Samples |
|---|---|---|---:|
| Group A | Escherichia coli K-12 MG1655 | NC_000913.3 | 1,000 |
| Group B | Mycoplasma genitalium G37 | NC_000908.2 | 1,000 |

Sources: [NCBI NC_000913.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3) and [NCBI NC_000908.2](https://www.ncbi.nlm.nih.gov/nuccore/NC_000908.2).

Each fragment is represented by A, T, G, C counts, sequence length, and GC percentage. Ambiguous-base fragments are excluded. The generated CSV is saved as `dna_sequence_dataset.csv` when the script or notebook is run. The exact CSV used for the report is also available as a separate project attachment.

**Scientific caveat:** fragments come from only one reference genome per group. A random fragment-level split is not independent-genome validation; performance may reflect genome-specific GC composition rather than general biological signals.

## Model and measured results
- Model: scikit-learn Decision Tree, `max_depth=4`, `random_state=42`
- Split: stratified 80% train / 20% test, `random_state=42`
- Test accuracy on the supplied CSV: **73.75%** (295 / 400 correct)
- Majority-class baseline: 50.00%

Confusion matrix (rows = actual; columns = predicted; order A, B):

| | Predicted A | Predicted B |
|---|---:|---:|
| Actual A | 146 | 54 |
| Actual B | 51 | 149 |

Unknown sequence `ATGCGCGATC` is predicted as **Group A** (estimated model probabilities: 84.65% A, 15.35% B). The true label is not supplied, so correctness cannot be checked.

## Repository contents
- `main.py` - downloads RefSeq genomes, creates the dataset, extracts features, trains/evaluates the model, and predicts the unknown sequence.
- `DNA_Classification.ipynb` - Google Colab/Jupyter launcher notebook for the full workflow.
- `requirements.txt` - Python dependencies.
- `results/metrics.json` - recorded metrics from the exact uploaded CSV and fixed model configuration.
- `results/REPORT.md` - report text and interpretation. The formatted four-page PDF is supplied separately with the project deliverables.

## Download the committed dataset
The exact dataset used for the reported metrics is stored in `data/dna_sequence_dataset.csv.gz`. Download it from the repository and decompress it to recover `dna_sequence_dataset.csv`:

```bash
gunzip -k data/dna_sequence_dataset.csv.gz
```

On Windows, 7-Zip can extract the `.gz` file. The decompressed file is the original CSV with 2,000 rows and six extracted features.

## Run locally
Install dependencies and run:

```bash
pip install -r requirements.txt
python main.py
```

An internet connection is required for the first run because the script downloads reference FASTA records from NCBI E-utilities.

## Run in Google Colab
Open `DNA_Classification.ipynb` in Google Colab and run all cells. The notebook clones this repository, installs dependencies, and runs `main.py`. The script creates `dna_sequence_dataset.csv` in the runtime.

## Limitations
1. Only one reference genome represents each group.
2. Ten-base fragments lose sequence order and biological context.
3. GC percentage is derived from G and C counts, so features are correlated.
4. Random fragment splitting does not test generalisation to independent genomes.
5. This educational model is not suitable for clinical diagnosis or definitive organism identification.

## Genomics application
Composition-based classification can be a basic exploratory step when comparing sequence fragments with labelled references. Practical genomic identification requires broader datasets, sequence-aware methods, and independent validation.
