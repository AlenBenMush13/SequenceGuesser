# Project Report: DNA Sequence Classification Using Machine Learning

## 1. Introduction and objective
DNA sequences consist of four nucleotide bases: adenine (A), thymine (T), guanine (G), and cytosine (C). This project trains a supervised classifier to recognise composition patterns in labelled short DNA fragments and predict the group of an unknown sequence, `ATGCGCGATC`.

## 2. Dataset source and preparation
A balanced dataset of 2,000 fragments was created using two NCBI RefSeq reference genomes:

| Group | Reference organism | Accession | Samples |
|---|---|---|---:|
| A | *Escherichia coli* K-12 MG1655 | NC_000913.3 | 1,000 |
| B | *Mycoplasma genitalium* G37 | NC_000908.2 | 1,000 |

Each fragment is 10 bases long. Fragments containing ambiguous symbols were excluded. Sources: [NCBI NC_000913.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3) and [NCBI NC_000908.2](https://www.ncbi.nlm.nih.gov/nuccore/NC_000908.2).

## 3. Feature extraction
For every sequence, six numerical features were extracted: A count, T count, G count, C count, length, and GC percentage.

`GC% = ((G count + C count) / sequence length) * 100`

Example rows from the dataset:

| Sequence ID | DNA sequence | Group | A | T | G | C | Length | GC% |
|---|---|---|---:|---:|---:|---:|---:|---:|
| GroupB_0861 | AAACTGTTCA | B | 4 | 3 | 1 | 2 | 10 | 30 |
| GroupA_0354 | TTCACCACGC | A | 2 | 2 | 1 | 5 | 10 | 60 |
| GroupB_0334 | GGGGTTAAAA | B | 4 | 2 | 4 | 0 | 10 | 40 |
| GroupA_0906 | TGGGGGGGAC | A | 1 | 1 | 7 | 1 | 10 | 80 |

The full dataset is generated as `dna_sequence_dataset.csv` when `main.py` or the Colab notebook runs.

## 4. Model training and evaluation
A scikit-learn Decision Tree classifier was selected, with maximum depth 4 and random state 42. A stratified 80/20 split was used: 1,600 training examples and 400 test examples.

**Measured test accuracy: 73.75% (295 / 400 correct).** A majority-class baseline gives 50%.

### Confusion matrix
Rows are actual labels and columns are predicted labels:

| Actual / Predicted | Group A | Group B |
|---|---:|---:|
| Group A | 146 | 54 |
| Group B | 51 | 149 |

### Feature importance
GC percentage was the most important feature in the fitted tree (approximately 91.0%). A count and C count made smaller contributions. Length had zero importance because all fragments were 10 bases long. GC percentage is derived from G and C counts, so these features contain overlapping information.

## 5. Prediction of the unknown sequence
Unknown sequence: `ATGCGCGATC`

| Feature | Value |
|---|---:|
| A count | 2 |
| T count | 2 |
| G count | 3 |
| C count | 3 |
| Length | 10 |
| GC content | 60% |

**Predicted group: Group A.** Model probability estimate: 84.65% Group A and 15.35% Group B. The true label is not supplied, so prediction correctness cannot be independently checked.

## 6. Genomics application
Composition-based classification can be an exploratory step when comparing short DNA fragments against labelled reference groups. Practical genomic identification requires larger and more diverse reference datasets, sequence-aware methods, and independent validation.

## 7. Limitations and critical discussion

**Which features were most useful?** GC percentage was most influential in this fitted model. A and C counts contributed less. Length was not useful because all fragments were the same length.

**Did the model predict correctly?** It predicted Group A, but the unknown sequence has no known label in the task, so correctness cannot be verified.

**What if a sequence is very different from the training data?** The model may make an unreliable prediction because its learned decision rules are based on patterns represented in the training examples.

**What are the limitations of AI/ML in genomics?** Results depend on training-data quality and diversity. Short fragments lose sequence order and biological context. This dataset contains fragments from only one reference genome per group and may reflect genome composition rather than general biological signals.

**Validation caveat:** A random fragment-level split puts fragments from the same two source genomes into both training and testing sets. The 73.75% result therefore measures performance on held-out fragments from these two genomes, not generalisation to entirely unseen genomes. A stronger evaluation would hold out independent genomes.

## 8. Conclusion
This project demonstrated a basic supervised-learning workflow: obtaining reference sequences, creating a labelled dataset, extracting features, training and evaluating a Decision Tree, and predicting an unknown fragment. The test accuracy was 73.75%, and the unknown sequence was predicted as Group A. The model is an educational demonstration and should not be treated as a validated tool for definitive organism identification or clinical use.

## References
1. [NCBI RefSeq NC_000913.3](https://www.ncbi.nlm.nih.gov/nuccore/NC_000913.3)
2. [NCBI RefSeq NC_000908.2](https://www.ncbi.nlm.nih.gov/nuccore/NC_000908.2)
3. [scikit-learn DecisionTreeClassifier documentation](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
