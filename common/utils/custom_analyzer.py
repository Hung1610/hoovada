from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer, tokenizer

vn_text_analyzer = analyzer('vn_text_analyzer',
    tokenizer=tokenizer('vi_tokenizer'),
    filter=['icu_folding']
)