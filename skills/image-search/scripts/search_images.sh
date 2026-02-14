#!/bin/bash

# DDGS Image Search Script with image downloading
# Usage: ./search_images.sh "query" [max_results]
# Example: ./search_images.sh "anime girl happy" 5

if [ -z "$1" ]; then
    echo "Usage: $0 \"search query\" [max_results]"
    exit 1
fi

QUERY=$(echo "$1" | sed 's/ /+/g')
MAX=${2:-5}

URL="http://localhost:8000/search/images?query=${QUERY}&region=us-en&safesearch=moderate&max_results=${MAX}"

RESULTS=$(curl -s -X 'GET' "$URL" -H 'accept: application/json')

if [ -z "$RESULTS" ] || ! echo "$RESULTS" | jq -e '.results // []' >/dev/null 2>&1; then
    echo "No images found"
    exit 1
fi

# Create temp directory for downloaded images
IMG_DIR="/tmp/clawko-images"
rm -rf "$IMG_DIR"
mkdir -p "$IMG_DIR"

# Parse results and download images
INDEX=0
echo "$RESULTS" | jq -c '.results[]' | while read -r ITEM; do
    TITLE=$(echo "$ITEM" | jq -r '.title')
    IMAGE_URL=$(echo "$ITEM" | jq -r '.image')
    INDEX=$((INDEX + 1))

    # Determine file extension from URL, default to .jpg
    EXT=$(echo "$IMAGE_URL" | grep -oP '\.(jpe?g|png|gif|webp)' | head -1)
    EXT="${EXT:-.jpg}"
    FILENAME="${INDEX}${EXT}"
    FILEPATH="${IMG_DIR}/${FILENAME}"

    # Download image (timeout 10s, silent, follow redirects)
    curl -sL --max-time 10 -o "$FILEPATH" "$IMAGE_URL" 2>/dev/null

    # Check if download succeeded and file is non-empty
    if [ -s "$FILEPATH" ]; then
        echo "[${INDEX}] ${TITLE}"
        echo "    URL: ${IMAGE_URL}"
        echo "    File: ${FILEPATH}"
        echo ""
    else
        rm -f "$FILEPATH"
        echo "[${INDEX}] ${TITLE}"
        echo "    URL: ${IMAGE_URL}"
        echo "    File: DOWNLOAD FAILED"
        echo ""
    fi
done
