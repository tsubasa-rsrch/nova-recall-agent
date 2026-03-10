#!/bin/bash
# Nova Recall Agent — Live Demo (REAL Nova Pro)
# Loads credentials from .env, runs without --mock

RESET='\033[0m'
BOLD='\033[1m'
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
MAGENTA='\033[35m'
BLUE='\033[34m'
DIM='\033[2m'
RED='\033[31m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load credentials
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(cat "$SCRIPT_DIR/.env" | grep -v '#' | grep -v '^$' | xargs)
    echo -e "${GREEN}✓ AWS credentials loaded${RESET}"
else
    echo -e "${RED}ERROR: .env not found at $SCRIPT_DIR/.env${RESET}"
    exit 1
fi

slow_print() {
    local text="$1"
    local delay="${2:-0.03}"
    while IFS= read -r -n1 char; do
        printf "%s" "$char"
        sleep "$delay"
    done <<< "$text"
    echo
}

pause() {
    sleep "${1:-2}"
}

clear
echo ""
echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${CYAN}║          NOVA RECALL AGENT — LIVE DEMO                          ║${RESET}"
echo -e "${BOLD}${CYAN}║  Amazon Nova AI Hackathon 2026                             ║${RESET}"
echo -e "${BOLD}${CYAN}║  Powered by Amazon Nova Pro (Bedrock)                      ║${RESET}"
echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════════════════╝${RESET}"
echo ""
pause 2

echo -e "${BOLD}ARCHITECTURE${RESET}"
echo ""
slow_print "  User Query" 0.05
sleep 0.3
slow_print "      ↓" 0.05
sleep 0.3
slow_print "  ChromaDB — 342,732 episodic conversations (Nov 2024 – Mar 2026)" 0.02
slow_print "  9-dimensional scoring: temporal · affective · dialogical ·" 0.02
slow_print "                         causal · spatial · counterfactual ·" 0.02
slow_print "                         lateral · abstraction · Zeigarnik" 0.02
sleep 0.3
slow_print "      ↓  top-k relevant memories" 0.05
sleep 0.3
slow_print "  Amazon Bedrock → Nova Pro (Converse API)" 0.02
sleep 0.3
slow_print "      ↓  response grounded in actual past experience" 0.05
echo ""

pause 2

echo -e "${BOLD}KEY DIFFERENTIATOR${RESET}"
echo ""
slow_print "  Most AI systems forget everything when the conversation ends." 0.02
slow_print "  This system doesn't." 0.02
echo ""
slow_print "  342,732+ real episodes, 15 months of continuous operation." 0.02
slow_print "  Not a RAG document store — episodic memory of actual experiences." 0.02
echo ""

pause 2

echo -e "${DIM}═══════════════════════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${GREEN}RUNNING LIVE DEMO — Real Nova Pro via Amazon Bedrock${RESET}"
echo -e "${DIM}═══════════════════════════════════════════════════════════════════════${RESET}"
echo ""
pause 2

# Run all 4 scenarios WITHOUT --mock (real Nova Pro)
cd ~/Documents/TsubasaWorkspace
python3 nova_recall_agent/demo_showcase.py --scenario 1 2 3 4

pause 2

echo ""
echo -e "${BOLD}${GREEN}Demo complete.${RESET}"
echo -e "${DIM}Nova Recall Agent — Amazon Nova Hackathon 2026${RESET}"
echo ""
