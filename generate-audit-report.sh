#!/bin/bash
pnpm audit --json > audit.json 2>/dev/null || true
if [ -s audit.json ]; then
    npm-audit-html --input audit.json --output audit-report.html
    echo "Report generated: audit-report.html"
    # Only try to open browser if not in CI environment
    if [ -z "$CI" ] && [ -z "$GITHUB_ACTIONS" ]; then
        open audit-report.html
    fi
    rm audit.json
else
    echo "No audit data to process"
fi
