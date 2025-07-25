REGISTRY = [
    {
        "name": "Entity",
        "plural_name": "Entities",
        "fields": [
            {
                "name": "xml_id",
                "label": "XML ID",
                "indexed": False,
                "unique": True,
                "multiple": False,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "entity_type",
                "label": "Type",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "name",
                "label": "Name",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "text",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "uris",
                "label": "URIs",
                "indexed": False,
                "unique": False,
                "multiple": True,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            }
        ],
        "show_in_nav": True,
        "autocomplete_labels": False,
        "proxy_field": "",
        "templates": {
            "Label": {
                "template": "{{ Entity.name }} ({{ Entity.entity_type }})",
                "mime_type": "text/html"
            }
        },
        "view_widget_url": None,
        "edit_widget_url": None,
        "inherited_from_module": None,
        "inherited_from_class": None,
        "base_mongo_indexes": None,
        "has_file_field": False,
        "invalid_field_names": [
            "uri",
            "last_updated",
            "content_type",
            "field_intensities",
            "provenance",
            "corpus_id",
            "path",
            "label"
        ]
    },
    {
        "name": "Letter",
        "plural_name": "Letters",
        "fields": [
            {
                "name": "identifier",
                "label": "Identifier",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "title",
                "label": "Title",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "text",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "date_composed",
                "label": "Date Composed",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "date",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "author",
                "label": "Author",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "cross_reference",
                "choices": [],
                "cross_reference_type": "Entity",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "recipient",
                "label": "Recipient",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "cross_reference",
                "choices": [],
                "cross_reference_type": "Entity",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "repository",
                "label": "Repository",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "cross_reference",
                "choices": [],
                "cross_reference_type": "Entity",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "collection",
                "label": "Collection",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "text",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": "english",
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "images",
                "label": "Images",
                "indexed": False,
                "unique": False,
                "multiple": True,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "entities_mentioned",
                "label": "Entities Mentioned",
                "indexed": False,
                "unique": False,
                "multiple": True,
                "in_lists": True,
                "type": "cross_reference",
                "choices": [],
                "cross_reference_type": "Entity",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "html",
                "label": "HTML",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "html",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "transcriber",
                "label": "Transcriber",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "text",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": "english",
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "date_transcribed",
                "label": "Date Transcribed",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "date",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "general_editors",
                "label": "General Editors",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "text",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": "english",
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "featured",
                "label": "Featured?",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "boolean",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            }
        ],
        "show_in_nav": True,
        "autocomplete_labels": False,
        "proxy_field": "",
        "templates": {
            "Label": {
                "template": "{{ Letter.identifier }}",
                "mime_type": "text/html"
            },
            "DefaultCSS": {
                "template": "div.dateline {\n    margin-bottom: 10px;\n}\n\ndiv.closer {\n    margin-bottom: 10px;\n}\n\nspan.underline, span.rend-underline {\n    text-decoration: underline;\n}\n\nspan.rend-superscript {\n    vertical-align: super;\n    font-size: smaller;\n    line-height: normal;\n}\n\nspan.regularized {\n    font-weight: bold;\n}\n\nspan.deletion {\n    text-decoration: line-through;\n}\n\nspan.entity {\n    color: orange;\n}\n\nspan.addition {\n    color: green;\n}\n\nspan.unclear {\n    color: gray;\n}",
                "mime_type": "text/css"
            }
        },
        "view_widget_url": None,
        "edit_widget_url": None,
        "inherited_from_module": None,
        "inherited_from_class": None,
        "base_mongo_indexes": None,
        "has_file_field": False,
        "invalid_field_names": [
            "uri",
            "last_updated",
            "content_type",
            "field_intensities",
            "provenance",
            "corpus_id",
            "path",
            "label"
        ]
    },
    {
        "name": "SitePage",
        "plural_name": "Site Pages",
        "fields": [
            {
                "name": "title",
                "label": "Title",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "url",
                "label": "URL",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "keyword",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            },
            {
                "name": "order",
                "label": "Order",
                "indexed": False,
                "unique": False,
                "multiple": False,
                "in_lists": True,
                "type": "number",
                "choices": [],
                "cross_reference_type": "",
                "has_intensity": False,
                "language": None,
                "autocomplete": False,
                "synonym_file": None,
                "indexed_with": [],
                "unique_with": [],
                "stats": {},
                "inherited": False
            }
        ],
        "show_in_nav": True,
        "autocomplete_labels": False,
        "proxy_field": "",
        "templates": {
            "Label": {
                "template": "{{ SitePage.title }}",
                "mime_type": "text/html"
            }
        },
        "view_widget_url": None,
        "edit_widget_url": None,
        "inherited_from_module": None,
        "inherited_from_class": None,
        "base_mongo_indexes": None,
        "has_file_field": False,
        "invalid_field_names": [
            "corpus_id",
            "content_type",
            "last_updated",
            "provenance",
            "field_intensities",
            "path",
            "label",
            "uri"
        ]
    }
]