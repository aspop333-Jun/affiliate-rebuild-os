import os
import sys
import argparse
import shutil
from pathlib import Path

# Configuration
TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "docs" / "03_templates"
SITES_DIR = Path(__file__).resolve().parent.parent.parent / "sites"

def create_article_folder(site_name, article_id):
    """
    Creates a new article folder structure.
    """
    site_path = SITES_DIR / site_name
    if not site_path.exists():
        print(f"Error: Site directory '{site_name}' does not exist.")
        return

    article_dir = site_path / "articles" / article_id
    if article_dir.exists():
        print(f"Error: Article directory '{article_id}' already exists in {site_name}.")
        return

    # Create directory
    article_dir.mkdir(parents=True)
    print(f"Created directory: {article_dir}")

    # Copy templates
    files_to_copy = {
        "source.md": None, # Create empty file
        "outline.md": TEMPLATE_DIR / "article_outline.md",
        "draft.md": TEMPLATE_DIR / "article_draft.md",
        "internal_link_map.md": TEMPLATE_DIR / "internal_link_map.md",
        "publish_log.md": TEMPLATE_DIR / "publish_log.md",
        "review.md": None # Create empty file
    }

    for filename, source_path in files_to_copy.items():
        dest_path = article_dir / filename
        if source_path:
            shutil.copy(source_path, dest_path)
            print(f"  Created {filename} (from template)")
        else:
            dest_path.touch()
            print(f"  Created {filename} (empty)")

    print("\nDone! Next steps:")
    print(f"1. Paste original content into {site_name}/articles/{article_id}/source.md")
    print(f"2. Generate outline in outline.md")

def main():
    parser = argparse.ArgumentParser(description="Scaffold a new article folder.")
    parser.add_argument("site", help="Site name (e.g., site01)")
    parser.add_argument("id", help="Article ID (e.g., 0001)")

    args = parser.parse_args()
    create_article_folder(args.site, args.id)

if __name__ == "__main__":
    main()
