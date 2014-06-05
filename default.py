"""LEXOR to LATEX DEFAULT Converter Style

Converts a lexor file to a valid latex file. Note that when using
python embeddings, everything outputed by the print statement will be
parsed in html (should be in latex but the parser is not yet
available).

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'final', 1),
    lang='lexor',
    to_lang='latex',
    type='converter',
    description='Convert lexor files to latex.',
    url='http://jmlopez-rod.github.io/'
        'lexor-lang/lexor-converter-latex-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'error': 'on',
    'exec': 'on',
}
MOD = load_aux(INFO)
REPOSITORY = [
    MOD['define'].DefineNC,
    MOD['define'].MacroNC,
    MOD['define'].UndefineNC,
    MOD['document'].DocumentClassNC,
    MOD['document'].DocumentBodyNC,
    MOD['document'].BibliographyNC,
    MOD['entity'].EntityNC,
    MOD['figure'].FigureNC,
    MOD['include'].IncludeNC,
    MOD['inline'].StrongEmNC,
    MOD['latex'].LatexNC,
    MOD['latex'].LatexEnvironNC,
    MOD['list'].ListNC,
    MOD['meta'].MetaNC,
    MOD['paragraph'].ParagraphNC,
    MOD['python'].PythonNC,
    MOD['quote'].QuoteNC,
    MOD['reference'].ReferenceBlockNC,
    MOD['reference'].ReferenceInlineNC,
]
MAPPING = {
    'lexor-meta': 'MetaNC',
    'latex': 'LatexNC',
    'bibliography': 'BibliographyNC',
    'body': 'DocumentBodyNC',
    'documentclass': 'DocumentClassNC',
    'quoted': 'QuoteNC',
    '#entity': 'EntityNC',
    '?python': 'PythonNC',
    'strong_em': 'StrongEmNC',
    'em_strong': 'StrongEmNC',
    'p': 'ParagraphNC',
    'list': 'ListNC',
    'address_reference': 'ReferenceBlockNC',
    'reference': 'ReferenceInlineNC',
    'equation': 'LatexEnvironNC',
    'subequations': 'LatexEnvironNC',
    'align': 'LatexEnvironNC',
    'figure': 'FigureNC',
    'define': 'DefineNC',
    'undef': 'UndefineNC',
    'macro': 'MacroNC',
    'include': 'IncludeNC',
}


def init_conversion(_, doc):
    """Initialiazing the conversion of a document. """
    doc.namespace['inline_ref'] = list()
    doc.namespace['math_environ'] = list()


def convert(converter, _):
    """Evaluate the python embeddings. """
    converter['ReferenceInlineNC'].convert()
    converter['LatexEnvironNC'].convert()
