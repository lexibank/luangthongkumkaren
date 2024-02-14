from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from clldutils.misc import slug
from pylexibank import FormSpec, Lexeme, Cognate
from pyedictor import fetch
import attr
from lingpy import Wordlist

@attr.s
class CustomCognate(Cognate):
    Morpheme_Index = attr.ib(default=None)

@attr.s
class CustomLexeme(Lexeme):
    Partial_Cognacy = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "luangthongkumkaren"
    cognate_class = CustomCognate
    lexeme_class = CustomLexeme
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
    
    def cmd_download(self, args):
        with open(self.raw_dir / "luangthongkumkaren.tsv", "w",  encoding="utf-8") as f:
            f.write(fetch(
                "ltkkaren", 
                base_url="http://lingulist.de/edev", 
                languages=[
                    "Kayah", "Kayan", "Kayaw", "NorthernPao", "NorthernPwo",
                    "NorthernSgaw", "ProtoKaren", "SouthernPao", "SouthernPwo",
                    "SouthernSgaw", "WesternBwe"],

                ))

    def cmd_makecldf(self, args):
        # Write sources
        args.writer.add_sources()

        # Write languages
        languages = args.writer.add_languages(lookup_factory="Name")

        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )
        
        def desegment(seq):
            out = []
            for itm in seq:
                out += [x.split("/")[1] if "/" in x else x for x in itm.split(".")]
            return out

        wl = Wordlist(str(self.raw_dir / "luangthongkumkaren.tsv"))
        for (idx, doculect, concept, value, form, tokens, 
                cogids, cogid) in progressbar(wl.iter_rows(
                        "doculect", "concept", "value", "form", "tokens",
                        "cogids", "cogid")):
            #print(idx, doculect, concept, value, form, tokens,
            #        desegment(tokens), cogids)
            lex = args.writer.add_form_with_segments(
                    Language_ID=doculect,
                    Parameter_ID=concepts[concept],
                    Value=value or form or "".join(tokens), 
                    Form=form or value or "".join(tokens), 
                    Segments=desegment(tokens),
                    Cognacy=cogid or "",
                    Partial_Cognacy=" ".join([str(x) for x in cogids])
                    )
            for i, (tks, cogid) in enumerate(zip(
                " ".join(desegment(tokens)).split(" + "),
                cogids)):
                args.writer.add_cognate(
                        lexeme=lex,
                        Morpheme_Index=i+1,
                        Cognateset_ID=cogid
                        )


    def old_cmd_makecldf(self, args):
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

            for i, (concept, value) in enumerate(row.items()):
                for lex in args.writer.add_forms_from_value(
                    Language_ID=languages[lang],
                    Parameter_ID=concepts[concept],
                    Value=value,
                    Source="luangthongkum2019",
                    Cognacy=str(i+1)):
                    args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=str(i+1),
                            Source="luangthongkum2019"
                            )

