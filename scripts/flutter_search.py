#!/usr/bin/env python3
"""
Flutter Pro Max Search - Intelligent search for Flutter knowledge base.

Features:
- BM25 semantic search using rank_bm25
- Widget weight boosting (double score for exact name match)
- Package category filtering
- Stack recognition (--stack flag to exclude conflicting packages)

Usage:
    python flutter_search.py "ListView pagination" --top 5
    python flutter_search.py "Network HTTP" --top 5
    python flutter_search.py "state management" --stack riverpod --top 5
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from typing import Optional

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    print("Error: rank_bm25 not installed. Run: pip install rank-bm25")
    sys.exit(1)


# Stack exclusion mapping
STACK_EXCLUSIONS = {
    "riverpod": ["bloc", "flutter_bloc", "provider", "hydrated_bloc"],
    "bloc": ["riverpod", "flutter_riverpod", "provider"],
    "provider": ["riverpod", "flutter_riverpod", "bloc", "flutter_bloc"],
}

# Category keyword mapping for package filtering
CATEGORY_KEYWORDS = {
    "network": ["Networking"],
    "http": ["Networking"],
    "api": ["Networking"],
    "database": ["Database"],
    "storage": ["Database", "Data"],
    "chart": ["Visualization"],
    "graph": ["Visualization"],
    "animation": ["Animation", "UI"],
    "state": ["State Management"],
    "di": ["Dependency Injection"],
    "security": ["Security"],
    "media": ["Media"],
    "test": ["Testing"],
}


class FlutterSearchEngine:
    """Intelligent search engine for Flutter knowledge base."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.documents = []
        self.metadata = []
        self.widget_names = set()
        self.package_categories = {}
        self.bm25 = None

    def load_csv(self, filename: str) -> list[dict]:
        """Load a CSV file and return list of dicts."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def build_index(self):
        """Build search index from all CSV files."""
        # Load widgets
        widgets = self.load_csv("widget.csv")
        for widget in widgets:
            name = widget.get("Widget Name", "")
            self.widget_names.add(name.lower())
            doc_text = " ".join(
                [
                    widget.get("Widget Name", ""),
                    widget.get("Category", ""),
                    widget.get("Description", ""),
                    widget.get("Key Properties", ""),
                    widget.get("Usage Context & Pro-Tips", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "widget", "name": name, "data": widget}
            )

        # Load packages
        packages = self.load_csv("package.csv")
        for pkg in packages:
            pkg_name = pkg.get("pkg_name", "")
            category = pkg.get("category", "")
            self.package_categories[pkg_name.lower()] = category
            doc_text = " ".join(
                [
                    pkg.get("pkg_name", ""),
                    pkg.get("category", ""),
                    pkg.get("description", ""),
                    pkg.get("best_practice_snippet", ""),
                    pkg.get("pro_tip", ""),
                    pkg.get("alternatives", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "package", "name": pkg_name, "category": category, "data": pkg}
            )

        # Load patterns
        patterns = self.load_csv("patterns.csv")
        for pattern in patterns:
            name = pattern.get("pattern_name", "")
            doc_text = " ".join(
                [
                    pattern.get("pattern_name", ""),
                    pattern.get("category", ""),
                    pattern.get("problem_tags", ""),
                    pattern.get("description", ""),
                    pattern.get("key_widgets", ""),
                    pattern.get("code_snippet", ""),
                    pattern.get("anti_pattern", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "pattern", "name": name, "data": pattern}
            )

        # Load architecture
        architect = self.load_csv("architect.csv")
        for arch in architect:
            path = arch.get("path_pattern", "")
            doc_text = " ".join(
                [
                    arch.get("path_pattern", ""),
                    arch.get("layer", ""),
                    arch.get("responsibility_description", ""),
                    arch.get("allowed_dependencies", ""),
                    arch.get("tech_stack_note", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "architecture", "name": path, "data": arch}
            )

        # Load charts
        charts = self.load_csv("charts.csv")
        for chart in charts:
            name = chart.get("Best Chart Type", "")
            doc_text = " ".join(
                [
                    chart.get("Data Type", ""),
                    chart.get("Keywords", ""),
                    chart.get("Best Chart Type", ""),
                    chart.get("Secondary Options", ""),
                    chart.get("Color Guidance", ""),
                    chart.get("Accessibility Notes", ""),
                    chart.get("Library Recommendation", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "chart", "name": name, "data": chart}
            )

        # Load colors
        colors = self.load_csv("colors.csv")
        for color in colors:
            name = color.get("Product Type", "")
            doc_text = " ".join(
                [
                    color.get("Product Type", ""),
                    color.get("Keywords", ""),
                    color.get("Primary (Hex)", ""),
                    color.get("Secondary (Hex)", ""),
                    color.get("CTA (Hex)", ""),
                    color.get("Notes", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "color", "name": name, "data": color}
            )

        # Load typography
        typography = self.load_csv("typography.csv")
        for typo in typography:
            name = typo.get("Font Pairing Name", "")
            doc_text = " ".join(
                [
                    typo.get("Font Pairing Name", ""),
                    typo.get("Category", ""),
                    typo.get("Heading Font", ""),
                    typo.get("Body Font", ""),
                    typo.get("Mood/Style Keywords", ""),
                    typo.get("Best For", ""),
                    typo.get("Notes", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "typography", "name": name, "data": typo}
            )

        # Load styles
        styles = self.load_csv("styles.csv")
        for style in styles:
            name = style.get("Style Category", "")
            doc_text = " ".join(
                [
                    style.get("Style Category", ""),
                    style.get("Type", ""),
                    style.get("Keywords", ""),
                    style.get("Primary Colors", ""),
                    style.get("Effects & Animation", ""),
                    style.get("Best For", ""),
                    style.get("Do Not Use For", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "style", "name": name, "data": style}
            )

        # Load UX guidelines
        ux_guidelines = self.load_csv("ux-guidelines.csv")
        for ux in ux_guidelines:
            name = ux.get("Issue", "")
            doc_text = " ".join(
                [
                    ux.get("Category", ""),
                    ux.get("Issue", ""),
                    ux.get("Platform", ""),
                    ux.get("Description", ""),
                    ux.get("Do", ""),
                    ux.get("Don't", ""),
                ]
            )
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "ux-guideline", "name": name, "data": ux}
            )

        # Load icons
        icons = self.load_csv("icons.csv")
        for icon in icons:
            name = icon.get("Icon Name", icon.get("Name", ""))
            doc_text = " ".join([str(v) for v in icon.values() if v])
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "icon", "name": name, "data": icon}
            )

        # Load landing page recommendations
        landing = self.load_csv("landing.csv")
        for land in landing:
            name = land.get("Section", land.get("Name", ""))
            doc_text = " ".join([str(v) for v in land.values() if v])
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "landing", "name": name, "data": land}
            )

        # Load naming conventions
        name_convention = self.load_csv("name_convention.csv")
        for conv in name_convention:
            name = conv.get("Convention", conv.get("Name", ""))
            doc_text = " ".join([str(v) for v in conv.values() if v])
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "naming", "name": name, "data": conv}
            )

        # Load products
        products = self.load_csv("products.csv")
        for prod in products:
            name = prod.get("Product Type", prod.get("Name", ""))
            doc_text = " ".join([str(v) for v in prod.values() if v])
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "product", "name": name, "data": prod}
            )

        # Load prompts
        prompts = self.load_csv("prompts.csv")
        for prompt in prompts:
            name = prompt.get("Prompt Name", prompt.get("Name", ""))
            doc_text = " ".join([str(v) for v in prompt.values() if v])
            self.documents.append(doc_text)
            self.metadata.append(
                {"type": "prompt", "name": name, "data": prompt}
            )

        # Build BM25 index
        tokenized_docs = [self._tokenize(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text for BM25."""
        text = text.lower()
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r"[^\w\s]", " ", text)
        tokens = text.split()
        return [t for t in tokens if len(t) > 1]

    def _detect_category_preference(self, query: str) -> list[str]:
        """Detect preferred categories from query keywords."""
        query_lower = query.lower()
        preferred = []
        for keyword, categories in CATEGORY_KEYWORDS.items():
            if keyword in query_lower:
                preferred.extend(categories)
        return list(set(preferred))

    def search(
        self,
        query: str,
        top_k: int = 10,
        stack: Optional[str] = None,
    ) -> list[dict]:
        """
        Search the knowledge base.

        Args:
            query: Search query string
            top_k: Number of results to return
            stack: Stack preference (riverpod, bloc, provider) to exclude conflicts

        Returns:
            List of search results with scores
        """
        if not self.bm25:
            raise RuntimeError("Index not built. Call build_index() first.")

        # Tokenize query
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Get BM25 scores
        scores = self.bm25.get_scores(query_tokens)

        # Apply widget weight boosting
        query_lower = query.lower()
        for i, meta in enumerate(self.metadata):
            if meta["type"] == "widget":
                widget_name = meta["name"].lower()
                # Exact match or query contains widget name
                if widget_name in query_lower or query_lower in widget_name:
                    scores[i] *= 2.0  # Double the score

        # Apply category preference boosting
        preferred_categories = self._detect_category_preference(query)
        if preferred_categories:
            for i, meta in enumerate(self.metadata):
                if meta["type"] == "package":
                    if meta.get("category") in preferred_categories:
                        scores[i] *= 1.5  # 50% boost

        # Get top results with metadata
        results = []
        for i, score in enumerate(scores):
            if score > 0:
                results.append(
                    {
                        "score": score,
                        "type": self.metadata[i]["type"],
                        "name": self.metadata[i]["name"],
                        "data": self.metadata[i]["data"],
                    }
                )

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        # Apply stack exclusion filter
        if stack and stack.lower() in STACK_EXCLUSIONS:
            excluded = STACK_EXCLUSIONS[stack.lower()]
            results = [
                r
                for r in results
                if r["name"].lower() not in excluded
            ]

        return results[:top_k]


def format_result(result: dict, index: int) -> str:
    """Format a single search result for display."""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"[{index}] {result['type'].upper()}: {result['name']}")
    output.append(f"    Score: {result['score']:.4f}")

    data = result["data"]
    if result["type"] == "widget":
        output.append(f"    Category: {data.get('Category', 'N/A')}")
        output.append(f"    Description: {data.get('Description', 'N/A')[:100]}...")
        output.append(f"    Pro-Tip: {data.get('Usage Context & Pro-Tips', 'N/A')[:150]}...")
    elif result["type"] == "package":
        output.append(f"    Category: {data.get('category', 'N/A')}")
        output.append(f"    Description: {data.get('description', 'N/A')[:100]}...")
        output.append(f"    Pro-Tip: {data.get('pro_tip', 'N/A')[:150]}...")
    elif result["type"] == "pattern":
        output.append(f"    Category: {data.get('category', 'N/A')}")
        output.append(f"    Tags: {data.get('problem_tags', 'N/A')}")
        output.append(f"    Description: {data.get('description', 'N/A')[:150]}...")
    elif result["type"] == "architecture":
        output.append(f"    Layer: {data.get('layer', 'N/A')}")
        output.append(f"    Responsibility: {data.get('responsibility_description', 'N/A')[:150]}...")
    elif result["type"] == "chart":
        output.append(f"    Data Type: {data.get('Data Type', 'N/A')}")
        output.append(f"    Chart Type: {data.get('Best Chart Type', 'N/A')}")
        output.append(f"    Library: {data.get('Library Recommendation', 'N/A')}")
    elif result["type"] == "color":
        output.append(f"    Product Type: {data.get('Product Type', 'N/A')}")
        output.append(f"    Primary: {data.get('Primary (Hex)', 'N/A')}")
        output.append(f"    CTA: {data.get('CTA (Hex)', 'N/A')}")
    elif result["type"] == "typography":
        output.append(f"    Category: {data.get('Category', 'N/A')}")
        output.append(f"    Heading: {data.get('Heading Font', 'N/A')}")
        output.append(f"    Body: {data.get('Body Font', 'N/A')}")
    elif result["type"] == "style":
        output.append(f"    Type: {data.get('Type', 'N/A')}")
        output.append(f"    Best For: {data.get('Best For', 'N/A')[:100]}...")
    elif result["type"] == "ux-guideline":
        output.append(f"    Category: {data.get('Category', 'N/A')}")
        output.append(f"    Do: {data.get('Do', 'N/A')[:100]}...")
        dont_val = data.get("Don't", "N/A")
        output.append(f"    Don't: {dont_val[:100] if dont_val else 'N/A'}...")
    else:
        # Generic format for icon, landing, naming, product, prompt
        for key, value in list(data.items())[:3]:
            if value:
                output.append(f"    {key}: {str(value)[:100]}...")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Flutter Pro Max Search - Intelligent search for Flutter knowledge base"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Search query string",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of results to return (default: 5)",
    )
    parser.add_argument(
        "--stack",
        type=str,
        choices=["riverpod", "bloc", "provider"],
        help="Stack preference to exclude conflicting packages",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Path to data directory (default: auto-detect)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    # Auto-detect data directory
    if args.data_dir:
        data_dir = args.data_dir
    else:
        # Try relative paths
        script_dir = Path(__file__).parent
        possible_paths = [
            script_dir.parent / ".shared" / "data",
            script_dir / ".." / ".shared" / "data",
            Path.cwd() / ".shared" / "data",
        ]
        data_dir = None
        for p in possible_paths:
            if p.exists():
                data_dir = str(p.resolve())
                break

        if not data_dir:
            print("Error: Could not find data directory. Use --data-dir to specify.")
            sys.exit(1)

    # Initialize and build index
    engine = FlutterSearchEngine(data_dir)
    engine.build_index()

    # Perform search
    results = engine.search(
        query=args.query,
        top_k=args.top,
        stack=args.stack,
    )

    if not results:
        print(f"No results found for: {args.query}")
        sys.exit(0)

    # Output results
    if args.json:
        import json

        # Clean results for JSON serialization
        json_results = []
        for r in results:
            json_results.append(
                {
                    "score": r["score"],
                    "type": r["type"],
                    "name": r["name"],
                    "data": r["data"],
                }
            )
        print(json.dumps(json_results, ensure_ascii=False, indent=2))
    else:
        print(f"\n🔍 Search Results for: '{args.query}'")
        if args.stack:
            print(f"   Stack filter: {args.stack} (excluding: {', '.join(STACK_EXCLUSIONS[args.stack])})")
        print(f"   Found {len(results)} results\n")

        for i, result in enumerate(results, 1):
            print(format_result(result, i))


if __name__ == "__main__":
    main()
