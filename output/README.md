# Text Summaries Output Structure

This folder contains processed outputs for all books.

## Structure

```
output/
└── books/
    ├── quicksilver/
    │   ├── book_one/
    │   │   ├── chunks/
    │   │   ├── summaries/
    │   │   └── formatted/
    │   ├── book_two/
    │   └── book_three/
    ├── cryptonomicon/
    │   ├── chunks/
    │   ├── summaries/
    │   └── formatted/
    └── [other_books]/
```

## Format

Each book follows this structure:
- `chunks/` - Original text divided into 2000-word chunks
- `summaries/` - 140-160 word summaries for each chunk
- `formatted/` - Final outputs in HTML, Markdown, and plain text

Books with multiple volumes (like Quicksilver) have subdirectories for each volume.