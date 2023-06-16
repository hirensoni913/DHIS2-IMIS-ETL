from enum import Enum


class Strategy(Enum):
    INSERT = 1
    UPDATE = 2
    INSERT_UPDATE = 3


def prepare_hf_payload(hfs: list, existing_ous: list, strategy: Strategy):
    if strategy == Strategy.INSERT:
        print("We will only insert new ones")
    elif strategy == Strategy.UPDATE:
        print("We will only update existing records")
    elif strategy == Strategy.INSERT_UPDATE:
        print("We will add new ones and update the existing ones")
