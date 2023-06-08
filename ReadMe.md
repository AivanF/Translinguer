# Translinguer
Allows writing simple scripts to manage locale/translation files.

The core idea behind this project is to provide a powerful yet flexible, extensible tool able to support arbitrary text types/formats to allow writing short and easy-to-use scripts.

# Origin
As a startuper and indi gamedev, I developed lots of apps with several languages support, constantly meeting a problem of platform/os/framework specific text files formats and a need of manual dealing with (which is especially painful for [cross-platform games with multiple languages support like TacticToy](https://www.aivanf.com/en/tactictoy)). I found no universal tool that can support many formats, so I wrote separate scripts before I finally got enough experience of understanding (and pain) to create a comprehensive tool.

Originally developed for [the Destiny Garden game](https://www.aivanf.com/en/destiny-garden-1) and widely enhanced while developing [Factorio mods](https://mods.factorio.com/user/AivanF), now I hope it can benefit other developers on various platforms!


# Workflow
My typical translating process consists of these steps:

- (Optionally) import existing raw locale files (json, ini, cfg, csv) and upload to Google Sheets
- Write/update texts in a Google Sheet (with myself, friends and volunteers, or Google Translate and ChatGPT)
- Download and parse texts from the Google Sheet
- (Optionally) Save into local cache
- Export texts to a required format (json, ini, cfg, csv)

# Usage
This is a simple example:
```py
from translinguer import Translinguer
trans = Translinguer()
trans.load_from_gsheets(key="__XYZ__")
trans.validate(raise_error=True)
trans.save_cfg("__file_path__")
```

[Here is a more powerful usage](https://github.com/AivanF/factorio-Mining-Drones-Remastered/blob/main/scripts/locales.py).

You can easily extend Translinguer with your own formats for reading/writing or validation
(e.g. to check that all entries from your source code are present or ensure some project-specific consistency).


# ToDo List
General:
- Describe data structure
- Describe existing methods and supported formats
- Publish to PyPI

Core:
- Replace dicts in dicts with lists of dedicated classes
- Allow to have separate languages for pages
- Add unit-tests
- Add Google Translate / ChatGPT API usage
- Allow import multiple files with different languages (get rid of `self.texts =` outside of base init)

Formats:
- Allow saving to Google Sheets
- Allow parsing CSV files
- Export to iOS / Android locale files. With multiple mappings from key to components?


# Contributing
Please follow this guide.

### New formats

On adding new formats support, keep existing mixin classes typing approach and methods naming convention described below.

"Private" methods should have file type in their names to avoid collisions.

Type-specific settings must be passed as method arguments (see `...` in the naming convention), not into base's properties (cache is the only except).

### Naming convention

Public methods naming convention for new file types:

- `from_TYPE...(content: str, ...)` – parse content of a format
- `to_TYPE...(output_path, ...) -> str` – save file of a format

- `load_TYPE...(input_path: str, ...)` – load file of a format
- `save_TYPE...(output_path: str, ...)` – save file of a format

- `load_from_TYPE...(...)` – load from external resource (like google cloud)
- `save_to_TYPE...(...)` – load from external resource (like google cloud)
