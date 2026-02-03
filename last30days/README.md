# /last30days

**The AI world reinvents itself every month. This Claude Code skill keeps you current.**

/last30days researches your topic across Reddit, X, and the web from the last 30 days, finds what the community is actually upvoting and sharing, and writes you a prompt that works today, not six months ago.

## Installation

```bash
# Clone the repo
git clone https://github.com/mvanhorn/last30days-skill.git ~/.claude/skills/last30days

# Add your API keys (optional but recommended)
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'EOF'
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
EOF
chmod 600 ~/.config/last30days/.env
```

## Usage

```
/last30days [topic]
/last30days [topic] for [tool]
```

Examples:
- `/last30days prompting techniques for ChatGPT for legal questions`
- `/last30days iOS app mockups for Nano Banana Pro`
- `/last30days What are the best rap songs lately`
- `/last30days remotion animations for Claude Code`

## What It Does

1. **Researches** - Scans Reddit and X for discussions from the last 30 days
2. **Synthesizes** - Identifies patterns, best practices, and what actually works
3. **Delivers** - Either writes copy-paste-ready prompts for your target tool, or gives you a curated expert-level answer

### Use it for:
- **Prompt research** - "What prompting techniques work for legal questions in ChatGPT?"
- **Tool best practices** - "How are people using Remotion with Claude Code?"
- **Trend discovery** - "What are the best rap songs right now?"
- **Product research** - "What do people think of the new M4 MacBook?"
- **Viral content** - "What's the dog-as-human trend on ChatGPT?"

## Options

| Flag | Description |
|------|-------------|
| `--quick` | Faster research, fewer sources (8-12 each) |
| `--deep` | Comprehensive research (50-70 Reddit, 40-60 X) |
| `--debug` | Verbose logging for troubleshooting |
| `--sources=reddit` | Reddit only |
| `--sources=x` | X only |

## Requirements

- **OpenAI API key** - For Reddit research (uses web search)
- **xAI API key** - For X research (optional but recommended)

At least one key is required for full functionality, but the skill works in web-only mode without any keys.

## How It Works

The skill uses:
- OpenAI's Responses API with web search to find Reddit discussions
- xAI's API with live X search to find posts
- Real Reddit thread enrichment for engagement metrics
- Scoring algorithm that weighs recency, relevance, and engagement

---

*30 days of research. 30 seconds of work.*

*Prompt research. Trend discovery. Expert answers.*

## Credits

Created by [Matt Van Horn](https://github.com/mvanhorn)
