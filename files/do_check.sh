#!/bin/bash

URL=https://github.com
PATTERN="Contact GitHub"
echo "checking url: $URL containing '$PATTERN'"
curl -s -XPOST http://localhost:8080/check -d '{"url": "'$URL'", "pattern": "Terms & Conditions", "insecure": false, "timeout": 20}' | jq '.'
