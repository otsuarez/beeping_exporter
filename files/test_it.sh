#!/bin/bash
export BEEPING_INSTANCE=beeping.local
export BEEPING_METRICS_PORT=9118
export BEEPING_SERVER=http://localhost:8088
export BEEPING_CHECKS='{"example.org":{"url": "https://example.org","pattern": "used for illustrative examples","timeout": 10},"example.net": {"url": "https://example.net","pattern": "Example Domain", "timeout": 10}}'
export DEBUG=1
files/beeping_exporter.py
