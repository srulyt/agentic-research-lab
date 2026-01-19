# Agentic Research Lab

**Course Module 3: Autonomous Agentic Development**

A hands-on laboratory for learning multi-agent orchestration patterns using Roo Code. This lab demonstrates how to build autonomous AI systems where specialized agents collaborate to solve complex research tasks.

---

## 🎯 What You'll Learn

This lab teaches advanced agentic coding concepts through a working multi-agent research system:

- **Multi-agent orchestration**: How a central orchestrator coordinates specialized agents
- **Agent autonomy**: Agents make their own decisions about research methodology and execution
- **Dynamic agent discovery**: Orchestrators automatically find and utilize available agents
- **Extending agent capabilities**: Adding tools via skills (MCP-compatible agent extensions)
- **Consensus mechanisms**: Aggregating results from multiple perspectives
- **File-based agent communication**: Agents coordinate through shared output files

---

## 📚 Course Context

This lab is part of **Module 3: Autonomous Agentic Development** in the course *"Agentic Architectures: From Autocomplete to Autonomy"*.

**Course Philosophy:**
> "We treat the Agent not as a tool, but as a junior engineer with infinite stamina but zero long-term memory. Your job isn't to write code; it's to curate the Context, define the Constraints (Tests), and architect the Feedback Loop."

This lab demonstrates that philosophy in action: you define agent personalities and orchestration rules, then watch autonomous agents execute complex research tasks without detailed step-by-step instructions.

---

## 🏗️ System Architecture

### Orchestrator + Agents Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Research Orchestrator                        │
│         (Coordinates, Spawns Tasks, Synthesizes Results)        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Scholar │    │Pragmatist│    │ Explorer │
    │    📚    │    │    🔧    │    │    🔮    │
    └──────────┘    └──────────┘    └──────────┘
         │               │               │
         └───────────────┴───────────────┘
                         │
                    ┌────▼────┐
                    │ Skills  │
                    │ bing-   │
                    │ search  │
                    │ webpage │
                    └─────────┘
```

### Key Patterns Demonstrated

| Pattern | Implementation | Purpose |
|---------|---------------|---------|
| **Dynamic Discovery** | Orchestrator searches for `research-agent-*` modes | Extensibility without code changes |
| **Boomerang Tasks** | `new_task` tool spawns autonomous sub-tasks | Parallel agent execution |
| **Agent Personalities** | Each agent has distinct rules and search strategies | Diverse perspectives on same query |
| **Skills Extension** | Python scripts in `.roo/skills/` extend capabilities | Tool use without API integration |
| **Consensus Algorithm** | Orchestrator aggregates results with confidence scoring | Multi-perspective synthesis |

---

## 🎭 Available Agent Modes

### 🔬 Research Orchestrator
**Role**: Coordinates research across multiple specialized agents

**Autonomy**: Dynamically discovers available agents, spawns parallel tasks, waits for completion, aggregates results using consensus algorithm

**When to use**: Any research query requiring comprehensive, multi-perspective analysis

---

### 📚 Research Agent - Scholar
**Personality**: Academic, analytical, rigorous

**Focus**: Peer-reviewed sources, academic papers, authoritative documentation, proper citations

**Search strategy**: Targets .edu domains, research institutions, scholarly databases

**Output emphasis**: Deep analysis, theoretical frameworks, methodological rigor

---

### 🔧 Research Agent - Pragmatist
**Personality**: Practical, results-oriented, hands-on

**Focus**: Tutorials, working code examples, Stack Overflow solutions, GitHub repositories

**Search strategy**: Targets dev.to, GitHub, technical blogs, how-to guides

**Output emphasis**: Step-by-step instructions, code examples, implementation guides

---

### 🔮 Research Agent - Explorer
**Personality**: Creative, curious, unconventional

**Focus**: Emerging trends, alternative viewpoints, cross-disciplinary connections, contrarian takes

**Search strategy**: Targets blogs, Reddit, Hacker News, niche communities, future predictions

**Output emphasis**: Diverse perspectives, edge cases, unexpected insights

---

## 🛠️ Skills (Agent Tools)

Agents extend their capabilities using **skills** - executable Python scripts that provide specific functionality:

### `bing-search`
**Purpose**: Web search capability for finding information

**Usage**: `python .roo/skills/bing-search/bing_search.py <query>`

**Returns**: Structured markdown with titles, URLs, and snippets

---

### `webpage-to-markdown`
**Purpose**: Extract clean content from web pages

**Usage**: `python .roo/skills/webpage-to-markdown/webpage_to_markdown.py <URL>`

**Returns**: Clean markdown content with headers, links, and formatting preserved

---

## 📖 Lab Instructions

**👉 See [docs/lab-instructions.md](docs/lab-instructions.md) for detailed step-by-step exercises.**

The lab includes:
1. Understanding the existing multi-agent system
2. Creating your own research agent with a unique personality
3. Running the orchestrator and observing agent coordination
4. (Bonus) Building domain-specific agents with intelligent routing

---

## 🚀 Quick Start

1. **Install Roo Code** (see lab instructions)
2. **Open this workspace** in VS Code with Roo Code installed
3. **Switch to Research Orchestrator mode** in the Roo Code interface
4. **Ask a research question**: "What are the best practices for Python async programming?"
5. **Watch the magic**: The orchestrator will spawn Scholar, Pragmatist, and Explorer agents, who will each conduct research from their unique perspective
6. **Review results**: Check the `results/` directory for individual agent reports and the orchestrator's synthesized consensus

---

## 📁 Project Structure

```
.roomodes                                    # Mode definitions (agent personalities)
.roo/
  rules-research-orchestrator/
    instructions.md                          # Orchestrator behavior rules
  rules-research-agent-scholar/
    instructions.md                          # Scholar agent rules
  rules-research-agent-pragmatist/
    instructions.md                          # Pragmatist agent rules
  rules-research-agent-explorer/
    instructions.md                          # Explorer agent rules
  skills/
    bing-search/                             # Web search skill
      bing_search.py
      SKILL.md
    webpage-to-markdown/                     # Content extraction skill
      webpage_to_markdown.py
      SKILL.md
results/                                     # Agent output directory
  scholar-results.md
  pragmatist-results.md
  explorer-results.md
docs/
  lab-instructions.md                        # Detailed lab exercises
```

---

## 🎓 Learning Outcomes

After completing this lab, you will understand:

1. **Agent Autonomy vs Automation**
   - Automation: Predefined steps, no decision-making
   - Autonomy: Agents choose their own paths to accomplish goals

2. **Multi-Agent Orchestration Patterns**
   - Centralized orchestrator vs distributed coordination
   - Dynamic agent discovery and registration
   - Task delegation and result aggregation

3. **Agent Design Principles**
   - Personality-driven behavior (rules define character)
   - Tool use and skill extension
   - Communication protocols (file-based, API-based, message-passing)

4. **Extensibility Without Code Changes**
   - Naming conventions enable discovery
   - Configuration-driven agent creation
   - Modular skill addition

---

## 🔗 Additional Resources

- **Roo Code Documentation**: https://github.com/RooCodeInc/Roo-Code-Docs
- **Custom Modes Guide**: https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/features/custom-modes.mdx
- **Agent Skills Specification**: https://agentskills.io/specification
- **Course Repository**: *(Add your course repo link)*

---

## 📝 License

This project is provided as an educational resource for the course *"Agentic Architectures: From Autocomplete to Autonomy"*.

---

**Ready to start?** Head to [docs/lab-instructions.md](docs/lab-instructions.md) for step-by-step exercises!
