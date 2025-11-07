#!/usr/bin/env python
"""Test that PDFs have the correct number of pages."""

import subprocess
import sys

def get_pdf_pages(pdf_path):
    """Get number of pages using macOS mdls command."""
    try:
        result = subprocess.run(
            ['mdls', '-name', 'kMDItemNumberOfPages', pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse output like "kMDItemNumberOfPages = 1"
        pages = int(result.stdout.split('=')[1].strip())
        return pages
    except Exception as e:
        print(f"✗ ERROR reading {pdf_path}: {e}")
        return None

def test_pdfs():
    """Test all PDFs have expected page counts."""
    tests = {
        'docs/resume.pdf': 1,           # 1-page ATS resume
        'docs/resume-ats.pdf': 1,       # Same as resume.pdf
        'docs/resume-projects.pdf': 2,  # ATS + projects (can be 2)
        'docs/cv.pdf': None,            # Full CV (variable length, just check it exists)
    }
    
    all_pass = True
    
    for pdf_path, expected_pages in tests.items():
        actual_pages = get_pdf_pages(pdf_path)
        
        if actual_pages is None:
            all_pass = False
            continue
            
        if expected_pages is None:
            print(f"✓ {pdf_path}: {actual_pages} pages (full CV)")
        elif actual_pages == expected_pages:
            print(f"✓ PASS: {pdf_path} has {actual_pages} page(s) as expected")
        else:
            print(f"✗ FAIL: {pdf_path} has {actual_pages} pages (expected {expected_pages})")
            all_pass = False
    
    return 0 if all_pass else 1

if __name__ == '__main__':
    sys.exit(test_pdfs())


