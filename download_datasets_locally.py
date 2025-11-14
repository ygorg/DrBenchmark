import os
import aiohttp
import logging

from datasets import load_dataset


ds = [
    ["CLISTER", None],
    ["DEFT2020", "task_1"],
    ["DEFT2020", "task_2"],
    ["E3C", "French_clinical"],
    ["E3C", "French_temporal"],
    ["E3C", "French_clinical_long"],
    ["E3C", "French_temporal_long"],
    ["FrenchMedMCQA", None],
    ["MANTRAGSC", "fr_emea"],
    ["MANTRAGSC", "fr_medline"],
    ["MANTRAGSC", "fr_patents"],
    ["MORFITT", "source"],
    ["QUAERO", "emea"],
    ["QUAERO", "emea_long"],
    ["QUAERO", "medline"],
    ["PxCorpus", None],
    ["DiaMED", None],
    # ["DEFT2019", None],
    ["DEFT2021", "cls"],
    ["DEFT2021", "ner"],
    ["DEFT2021", "ner_long"],

    ["CAS", "pos"],
    ["CAS", "cls"],
    ["CAS", "ner_neg"],
    ["CAS", "ner_spec"],

    ["ESSAI", "pos"],
    ["ESSAI", "cls"],
    ["ESSAI", "ner_neg"],
    ["ESSAI", "ner_spec"],
]


def save_locally(arr):
    corpus, subset = arr

    logging.info(f">> Downloading {corpus}{' - '+subset if subset else ''}")

    data_loader_path = f"DrBenchmark/{corpus}"
    if subset and 'long' in subset:
        data_loader_path = f"{os.path.dirname(__file__)}/data_loaders_hf/{corpus}_long.py"

    dataset = load_dataset(
        data_loader_path,
        subset,
        trust_remote_code=True,
        storage_options={
            'client_kwargs': {'timeout': aiohttp.ClientTimeout(20 * 60)}
        }
    )
    dataset.save_to_disk(f"./recipes/{corpus.lower()}/data/local_hf_{subset}/")


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )

    for d in ds:
        save_locally(d)
