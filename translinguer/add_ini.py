from typing import Optional
import os
import codecs
from .base import TranslinguerBase


class TranslinguerIni:
    def save_ini_page(
        self: TranslinguerBase,
        output_path: str, only_page: Optional[str] = None,
    ):
        # Sections from pages
        print('-- Saving to INI files...')

        done_pages = 0
        for lng in self.languages:
            lines = []
            for page_name, page in self.texts.items():
                if only_page and page_name != only_page:
                    continue
                for section_name, section in page.items():
                    lines.append(f'\n[{section_name}]')
                    for key, entry in section.items():
                        value = entry[lng]
                        value = value.replace('"', '\\"')
                        lines.append(f'{key}="{value}"')

            fname = os.path.join(
                output_path,
                f'{self.lang_mapper[lng]}.lng'
            )
            with codecs.open(fname, 'w', encoding='utf8') as file:
                file.write('\n'.join(lines))
            done_pages += 1
            print('- Done', lng)
