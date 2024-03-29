## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')', '‘': '’'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `/,`
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `['---', '- (?)']`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[(' ̈', '̈'), ('mə̯ ɨ³³', 'mə̯ɨ³³'), ('Ɂa¹¹ko̯ u⁵⁵', 'Ɂa¹¹ko̯u⁵⁵'), ('thə̃ɨ̯ ³³', 'thə̃ɨ̯³³'), ('sɛ³̃ ⁵', 'sɛ³̃⁵'), ('pu¹¹khɛ⁵̃ ⁵', 'pu¹¹khɛ⁵̃⁵'), ('nə̯ u¹¹̈', 'nə̯u¹¹̈'), ('pə̯ ɨ³³', 'pə̯ɨ³³'), ('ɣəɨ̯ ¹¹̈', 'ɣəɨ̯¹¹̈'), ('mu̯ əm⁵³', 'mu̯əm⁵³'), ('mɛĩ ³¹̈', 'mɛĩ³¹̈'), ('ruə̯ n³¹̈', 'ruə̯n³¹̈'), ('su̯ ən³³', 'su̯ən³³'), ('chuə̯ m³¹̈', 'chuə̯m³¹̈'), ('jɔ¹¹ ẗ hu³³', 'jɔ¹¹ thü³³'), ('lɛ⁵̃ ⁵', 'lɛ⁵̃⁵'), (' ', '_')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `False`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')

### Replacement of invalid lexemes

Source lexemes may be impossible to interpret correctly. 34 such lexemes are listed
in [`etc/lexemes.csv`](etc/lexemes.csv) and replaced as specified in this file.
