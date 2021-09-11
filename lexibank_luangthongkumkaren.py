from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from clldutils.misc import slug
from pylexibank import FormSpec


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "luangthongkumkaren"
    form_spec = FormSpec(
        separators="/,",
        missing_data=["---", "- (?)"],
        brackets={"(": ")", "‘": "’"},
        # fix spaces before diacritics
        replacements=[
            (" ̈", "\u0308"),
            ("mə̯ ɨ³³", "mə̯ɨ³³"),
            ("Ɂa¹¹ko̯ u⁵⁵", "Ɂa¹¹ko̯u⁵⁵"),
            ("thə̃ɨ̯ ³³", "thə̃ɨ̯³³"),
            ("sɛ³̃ ⁵", "sɛ³̃⁵"),
            ("pu¹¹khɛ⁵̃ ⁵", "pu¹¹khɛ⁵̃⁵"),
            ("nə̯ u¹¹̈", "nə̯u¹¹̈"),
            ("pə̯ ɨ³³", "pə̯ɨ³³"),
            ("ɣəɨ̯ ¹¹̈", "ɣəɨ̯¹¹̈"),
            ("mu̯ əm⁵³", "mu̯əm⁵³"),
            ("mɛĩ ³¹̈", "mɛĩ³¹̈"),
            ("ruə̯ n³¹̈", "ruə̯n³¹̈"),
            ("su̯ ən³³", "su̯ən³³"),
            ("chuə̯ m³¹̈", "chuə̯m³¹̈"),
            ("jɔ¹¹ ẗ hu³³", "jɔ¹¹ thü³³"),
            ("lɛ⁵̃ ⁵", "lɛ⁵̃⁵"),
            (" ", "_"),
        ],
    )

    def cmd_makecldf(self, args):
        # Write sources
        args.writer.add_sources()

        # Write languages
        languages = args.writer.add_languages(lookup_factory="Name")

        # Write concepts
        concepts = args.writer.add_concepts(
            lookup_factory="Name",
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
        )

        # read raw wordlist and lexemes
        for row in progressbar(
            self.raw_dir.read_csv(
                "luangthongkumkaren.tsv", delimiter="\t", dicts=True
            )
        ):
            # Extract the `language`, so that we only have lexemes in `row`,
            # and skip over the "Notes" field
            lang = row.pop("Language")
            if lang == "Notes":
                continue

            for concept, value in row.items():
                args.writer.add_lexemes(
                    Language_ID=languages[lang],
                    Parameter_ID=concepts[concept],
                    Value=value,
                    Source="luangthongkum2019",
                )
