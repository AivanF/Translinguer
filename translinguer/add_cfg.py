from typing import Optional
import os
import codecs
from .base import TranslinguerBase as base, Page, Section
from .utils import dict_get, dict_get_reversed


class TranslinguerCfg:
    def save_cfg(
        self: base, output_path: str, only_page: Optional[str] = None,
    ):
        # Sections from embedded sections
        print('-- Saving to CFG files...')

        done_pages = 0
        for lng in self.languages:
            lines = []
            for page_name, page in self.texts.items():
                if only_page and page_name != only_page:
                    continue
                for section_name, section in page.items():
                    if len(section_name) > 0:
                        lines.append(f'\n[{section_name}]')
                    for key, entry in section.items():
                        lines.append(f'{key}={entry[lng]}')
                fname = os.path.join(
                    output_path,
                    f'{self.lang_mapper[lng]}/{page_name}.cfg'
                )
                with codecs.open(fname, 'w', encoding='utf8') as file:
                    file.write('\n'.join(lines))
                done_pages += 1
            print('- Done', lng)
        if done_pages == 0:
            raise ValueError('Nothing is written')

    def _parse_cfg(self: base, page, lng, data):
        result = 0
        page: Page = dict_get(self.texts, page)
        section: Section = dict_get(page, '')

        lines = data.split('\n')
        for ln in lines:
            ln = ln.strip()
            if ln.startswith('#'):
                continue
            if ln.startswith('['):
                ln = ln[1:-1]
                ln = ln.strip()
                section = dict_get(page, ln)
                continue
            eq = ln.find('=')
            if eq > 0:
                key = ln[:eq]
                key = key.strip()
                value = ln[eq + 1:]
                value = value.strip()
                entry = dict_get(section, key)
                entry[dict_get_reversed(self.lang_mapper, lng)] = value
                result += 1
        return result

    def load_cfg(self: base, input_path):
        print('-- Parsing CFG files...')
        result = 0
        self.texts = {}
        add_languages = len(self.languages) == 0
        for root, dirs, files in os.walk(input_path):
            for fl in files:
                if not fl.endswith('.cfg'):
                    continue
                with codecs.open(
                    os.path.join(root, fl), 'r', encoding='utf8'
                ) as file:
                    lng = os.path.split(root)[-1]
                    if add_languages:
                        self.languages.append(lng)
                    elif lng not in self.languages:
                        raise ValueError(f'Unexpected language {lng}')
                    result += self._parse_cfg(
                        page=fl[:-4],
                        lng=lng,
                        data=file.read(),
                    )
                    print(f'- {lng} done')

        self._set_update('Parsed CFG')
        print('- Loaded', result, 'entries')
