from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer, char_filter

special_character_filter = char_filter(
    "special_character_filter", type="pattern_replace", pattern="[^A-Za-z0-9]", replacement="")

vn_text_analyzer = analyzer('vn_text_analyzer',
    tokenizer=tokenizer('vi_tokenizer'),
    char_filter=[special_character_filter],
    filter=['icu_folding']
)

vn_html_analyzer = analyzer('vn_html_analyzer',
    tokenizer=tokenizer('vi_tokenizer'),
    char_filter=["html_strip"],
    filter=['icu_folding']
)