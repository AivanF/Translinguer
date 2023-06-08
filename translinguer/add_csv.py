import io
import csv
from .base import TranslinguerBase
from .utils import dict_get_reversed


class TranslinguerCsv:
    def to_csv(
        self: TranslinguerBase, page=None, sections=False, delimiter='\t',
    ) -> str:
        output = io.StringIO()
        writer = csv.writer(output, delimiter=delimiter)
        header = ["key"] + [
            dict_get_reversed(self.lang_mapper, lng) for lng in self.languages
        ]
        writer.writerow(header)
        if page is None:
            for page in self.texts.values():
                for section_name, section in page.items():
                    if len(section_name) > 0:
                        writer.writerow([f'[{section_name}]'])
                    writer.writerows([
                        [key] + [entry.get(lng) for lng in self.languages]
                        for key, entry in section.items()
                    ])
        else:
            page = self.texts[page]
            for section_name, section in page.items():
                if len(section_name) > 0:
                    writer.writerow([f'[{section_name}]'])
                writer.writerows([
                    [key] + [entry.get(lng) for lng in self.languages]
                    for key, entry in section.items()
                ])
        return output.getvalue()
