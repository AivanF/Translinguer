import codecs
import json
from .base import TranslinguerBase as base, UNKNOWN

SYSTEM_KEY = '_sys_'


class TranslinguerCache:
    def serialize(self: base, sort: bool):
        target = {}
        target.update(self.texts)
        target[SYSTEM_KEY] = dict(
            languages=self.languages,
            last_update=self.last_update,
            source=self.source,
        )
        return json.dumps(target, indent=4, sort_keys=True, ensure_ascii=False)

    def deserialize(self: base, data):
        texts = json.loads(data)
        sys = texts[SYSTEM_KEY]
        del texts[SYSTEM_KEY]
        self.source = sys.get('source', UNKNOWN)
        self.last_update = sys['last_update']
        if len(sys['languages']) > len(self.languages):
            self.languages = sys['languages']
        self.texts = texts

    def save_cache(self: base, sort: bool = False):
        with codecs.open(self.cache, 'w', encoding='utf8') as file:
            file.write(self.serialize(sort=sort))
        print('-- JSON cache saved.')

    def load_cache(self: base):
        print('-- Loading from JSON cache...')
        with codecs.open(self.cache, 'r', encoding='utf8') as file:
            self.deserialize(file.read())
