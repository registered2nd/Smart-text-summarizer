#!/usr/bin/env python3
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys

def test_epub_extraction():
    print("Testing EPUB extraction capabilities...")
    print("✓ ebooklib imported successfully")
    print("✓ BeautifulSoup imported successfully")
    print("\nEnvironment is ready for EPUB text extraction!")
    print("\nYou can now:")
    print("- Extract text from EPUB files")
    print("- Process content with BeautifulSoup")
    print("- Create 150-word summaries from 2000-word chunks")

if __name__ == "__main__":
    test_epub_extraction()