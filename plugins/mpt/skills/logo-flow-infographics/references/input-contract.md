# Graph and asset inputs

Graph JSON fields: title; status (synthetic, proposed, implemented); basis (user flow or inspected source/commit); description (relationships and branch meaning); width/height (default 800×510); asset_manifest (relative to graph); nodes (id, asset, x, y); edges (source, target); optional disclaimer outside graph.

Manifest: object keyed by asset ID. Each entry requires name, path, sha256, source and license_note. Paths resolve relative to the manifest and must stay inside its directory after symlink resolution. Use the exact approved local file hash. Identity, usage permission and semantic truth still require review; hashes are not licenses.

Each node's label comes from its asset's accurate name. The helper supports local SVGs, 1–60 nodes, up to 120 forward left-to-right edges, 100px cards, fitted 64px logos and 16px labels. Leave at least 28px below cards. For loops, backward edges, long names or crowded layouts, choose another renderer or deliberately revise layout; never silently change topology.

Examples: add only the correct names under existing logos; draw a synthetic three-service flow from supplied local assets; visualize an inspected extraction/review pipeline using technologies actually evidenced. Related product names are not interchangeable.
