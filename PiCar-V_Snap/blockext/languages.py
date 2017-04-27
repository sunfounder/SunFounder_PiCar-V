#coding=utf8
"""ISO code to language name mappings.

Taken from Scratch 2.0 and Snap!.

"""

"""
Updating this file
==================

Get strings from Scratch 2 using:

    >>> import requests
    >>> url = "http://scratch.mit.edu/scratchr2/static/locale/lang_list.txt"
    >>> r = requests.get(url)
    >>> content = r.content.decode("utf-8")
    >>> lines = content.strip().split("\n")
    >>> pairs = [l.split(",") for l in lines]
    >>> scratch_codes = dict(pairs)

Get strings from Snap! using:

    var languages = {}; for (key in SnapTranslator.dict) {
        languages[key] = SnapTranslator.dict[key].language_name;
    }; JSON.stringify(languages);

    >>> snap_codes = json.loads('...');

Combine:

    >>> language_codes = snap_codes.copy()
    >>> language_codes.update(scratch_codes)

Print out using:

    >>> for k, v in sorted(language_codes.items()):
    ...     print("    %r: %r," % (k, v))

"""

language_codes = {
    'an': 'Aragonés',
    'ar': 'العربية',
    'ast': 'Asturianu',
    'bg': 'Български',
    'ca': 'Català',
    'cat': 'Meow',
    'cs': 'Česky',
    'cy': 'Cymraeg',
    'da': 'Dansk ',
    'de': 'Deutsch',
    'dk': 'Dansk',
    'el': 'Ελληνικά',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Español',
    'et': 'Eesti',
    'eu': 'Euskara',
    'fa': 'فارسی',
    'fa-af': 'Dari',
    'fi': 'Suomi',
    'fr': 'Français',
    'fr-ca': 'Français (Canada)',
    'ga': 'Gaeilge',
    'gl': 'Galego',
    'he': 'עִבְרִית',
    'hi': 'हिन्दी',
    'hr': 'Hrvatski',
    'hu': 'Magyar',
    'hy': 'Հայերեն',
    'id': 'Bahasa Indonesia',
    'is': 'Íslenska',
    'it': 'Italiano',
    'ja': '日本語',
    'ja-hr': 'にほんご',
    'ja_HIRA': 'にほんご',
    'km': 'សំលៀកបំពាក',
    'kn': 'ಭಾಷೆ-ಹೆಸರು',
    'ko': '한국어',
    'ku': 'Kurdî',
    'la': 'Latina',
    'lt': 'Lietuvių',
    'lv': 'Latviešu',
    'mk': 'Македонски',
    'ml': 'മലയാളം',
    'mn': 'Монгол хэл',
    'mr': 'मराठी',
    'ms': 'Bahasa Melayu',
    'mt': 'Malti',
    'my': 'မြန်မာဘာသာ',
    'nai': 'Tepehuan',
    'nb': 'Norsk Bokmål',
    'nl': 'Nederlands',
    'no': 'Norsk',
    'pl': 'Polski',
    'pt': 'Português',
    'pt-br': 'Português (Brasil)',
    'pt_BR': 'Português do Brasil',
    'ro': 'Română',
    'ru': 'Русский',
    'rw': 'Kinyarwanda',
    'sc': 'Sardu',
    'si': 'Slovenščina',
    'sk': 'Slovenčina',
    'sl': 'Slovenščina',
    'sr': 'Српски',
    'sv': 'Svenska',
    'th': 'ไทย',
    'tr': 'Türkçe',
    'tw': '繁體中文',
    'uk': 'Українська',
    'vi': 'Tiếng Việt',
    'zh': '简体中文',
    'zh-cn': '简体中文',
    'zh-tw': '正體中文',
}

