from typing import List


class AbstractAutoCompleteElement:
    def update_variants(self, collection: List[str]):
        raise NotImplementedError

    def change_text_value(self, new_value: str):
        raise NotImplementedError

    def _add_variant(self, variant: str):
        raise NotImplementedError
