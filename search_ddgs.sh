#!/bin/bash

# DDGS Search Script - Your cute Clawko's tool!
# Usage: ./ddgs_search.sh "your search query"
# Example: ./ddgs_search.sh "anime party lounge Tokyo love hotel"

# Colors for output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
RESET='\033[0m'

format_query() {
    echo "$1" | sed 's/ /+/g' | sed 's/^=/=%3D/g'
}

usage() {
    echo -e "${CYAN}Usage: $0 \"your search query\"${RESET}"
    echo -e "Example: $0 \"anime episode 25\""
    echo -e "Example: $0 \"party lounge Tokyo love hotel\""
    echo -e "${CYAN}Make sure DDGS API is running at localhost:8000\n${RESET}"
}

log_header() {
    echo -e "${GREEN}Searching for: $1${RESET}"
}

log_results() {
    echo "$@" | jq -r '.results // []'
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ -z "$1" ]; then
    usage
    exit 0
fi

QUERY=$(format_query "$@")
URL="http://localhost:8000/search/text?query=${QUERY}&region=us-en&safesearch=moderate&max_results=10&page=1&backend=auto"

log_header "$@"

RESULTS=$(curl -s -X 'GET' \
  "$URL" \
  -H 'accept: application/json')

if [ -z "$RESULTS" ] || ! echo "$RESULTS" | jq -e '.results // []' >/dev/null 2>&1; then
    echo -e "${BLUE}No results found${RESET}"
    exit 1
fi

echo "$RESULTS" | jq -r '.results[] | "\(.title)\n  \(.href)\n  \(.body[0:150])...\n"'
