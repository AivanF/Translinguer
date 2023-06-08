from typing import Dict, List, Optional
import datetime
from .utils import ProxyDict

DEFAULT_CACHE_FILE = 'texts.json'
UNKNOWN = '?'

Entry = Dict[str, str]  # lng => text
Section = Dict[str, Entry]  # entry key => lng => text
Page = Dict[str, Section]  # section name =>  entry key => entry
Locales = Dict[str, Page]  # sheet page name => sections
LangRenamer = Optional[Dict[str, str]]


class TranslinguerBase:
    texts: Locales
    languages: List[str]

    def __init__(
        self,
        languages: Optional[List[str]] = None,
        lang_mapper: LangRenamer = None,
        cache: str = DEFAULT_CACHE_FILE,
    ):
        self.texts = {}
        self.languages = languages if languages else []
        self.cache = cache
        self.lang_mapper = lang_mapper if lang_mapper else ProxyDict()
        self.last_update = UNKNOWN
        self.source = UNKNOWN

    @property
    def texts_number(self):
        return sum((
            1
            for page in self.texts.values()
            for section in page.values()
            for entry in section.values()
            for locale in entry.values()
        ))

    @property
    def entries_number(self):
        return sum((
            1
            for page in self.texts.values()
            for section in page.values()
            for entry in section.values()
        ))

    def stats(self):
        print(
            f'-- {self.entries_number} entries'
            f', {len(self.languages)} languages'
            f', {len(self.texts)} pages'
            f'\nFrom {self.source} of {self.last_update}'
        )

    def validate(self, raise_error=False):
        print('-- Validating texts...')
        problems = 0
        for page_name, page in self.texts.items():
            for section_name, section in page.items():
                for key, entry in section.items():
                    for lng in self.languages:
                        if not entry.get(lng):
                            problems += 1
                            path = ' -> '.join((page_name, section_name, key))
                            print(f'- Missing lng {lng} for {path}')
        if problems > 0 and raise_error:
            raise ValueError('Found {problems} problems')
        if problems == 0:
            print('- All right!')
        return problems

    def _set_update(self, source):
        self.last_update = str(datetime.datetime.now())
        self.source = source
