from typing import Optional
import io
import csv
from .base import TranslinguerBase
from .utils import dict_get_reversed


class TranslinguerCsv:
    def to_csv(
        self: TranslinguerBase, only_page: Optional[str] = None,
        sections=False, delimiter='\t',
    ) -> str:
        output = io.StringIO()
        writer = csv.writer(output, delimiter=delimiter)
        header = ["key"] + [
            dict_get_reversed(self.lang_mapper, lng) for lng in self.languages
        ]
        writer.writerow(header)
        for page_name, page in self.texts.items():
            if only_page and page_name != only_page:
                continue
            for section_name, section in page.items():
                if sections and len(section_name) > 0:
                    writer.writerow([f'[{section_name}]'])
                writer.writerows([
                    [key] + [entry.get(lng) for lng in self.languages]
                    for key, entry in section.items()
                ])
        return output.getvalue()
