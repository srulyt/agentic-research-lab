# Lab: Multi-Agent Orchestration

**Module 3: Autonomous Agentic Development**  
**Time**: 45 minutes

---

## Setup

1. Install Roo Code extension in VS Code
2. Open this workspace in VS Code
3. Install Python packages: `pip install requests beautifulsoup4 html2text`
4. Configure Roo Code with your LLM (Settings → VS Code LM API or direct API key)

---

## Exercise 1: Explore the System (5 min)

**Goal**: Understand how agents are defined through configuration, not code.

**Do**:

1. **Open `.roomodes`** - See how 4 agents are defined (orchestrator + 3 research agents)
2. **Notice the pattern**: All research agents use slug `research-agent-*`
3. **Open `.roo/rules-research-orchestrator/instructions.md`** - See how orchestrator discovers agents by pattern matching
4. **Open any agent rules** (e.g., `.roo/rules-research-agent-scholar/instructions.md`) - See how personality is defined through instructions

**Key Insight**: Agent behavior = instructions + naming conventions. No code required.

---

## Exercise 2: Create Your Agent (15 min)

**Goal**: Add a 4th research agent with unique personality.

### Step 1: Choose Personality

Pick one:
- **📊 Analyst**: Data-driven, focuses on metrics and statistics
- **🔍 Skeptic**: Critical thinker, focuses on fact-checking
- **📜 Historian**: Temporal focus, traces evolution over time

### Step 2: Add to `.roomodes`

Add after `research-agent-explorer`:

```yaml
  - slug: research-agent-analyst
    name: "📊 Research Agent - Analyst"
    roleDefinition: |
      Data-driven researcher prioritizing statistics, benchmarks, and quantitative evidence.
      Focus on measurable outcomes and comparative analysis.
    whenToUse: |
      Use for data-driven research with statistics and metrics.
    customInstructions: |
      See detailed instructions in .roo/rules-research-agent-analyst/
    groups:
      - read
      - - edit
        - fileRegex: "\\.(md)$"
      - command
      - mcp
```

### Step 3: Create Instructions

1. Create directory: `mkdir .roo/rules-research-agent-analyst`
2. Copy template from `docs/templates/research-agent-analyst.md` to `.roo/rules-research-agent-analyst/instructions.md`

**That's it.** The orchestrator will auto-discover your agent because the slug matches `research-agent-*`.

---

## Exercise 3: Run Orchestration (5 min)

**Goal**: See multi-agent coordination in action.

**Do**:

1. Click Roo Code icon (🦘) in sidebar
2. Switch mode to "🔬 Research Orchestrator"
3. Ask: `"What are the best programming fonts in 2024?"`

**Observe**:

- Orchestrator discovers 4 agents (your new one included!)
- Spawns 4 parallel tasks using `new_task` tool
- Each agent searches with different strategy (Scholar = academic, Pragmatist = tutorials, Explorer = blogs, Analyst = data)
- Results written to `results/` directory
- Orchestrator synthesizes with consensus algorithm
- Final response shows high/medium/low confidence findings

**Open `results/`** to see each agent's unique perspective on the same query.

---

## Bonus: Domain-Specific Agent (Optional, 20 min)

**Challenge**: Create a domain specialist (finance, health, security, ML) and modify orchestrator to route queries intelligently.

**Example**: Finance agent only activates for queries containing "stock", "market", "investment", etc.

**Hint**: Add "Intelligent Agent Selection" section to orchestrator instructions with keyword detection logic.

---

## What You Learned

**Multi-Agent Patterns**:
- Dynamic discovery via naming conventions (`research-agent-*`)
- Boomerang tasks (spawn → execute → return results)
- Consensus aggregation (multiple perspectives → confidence levels)

**Agent Design**:
- Configuration over code (`.roomodes` + instructions)
- Personality through natural language
- Skills as terminal commands (flexible, language-agnostic)

You just built a multi-agent system without writing code.

---

## Quick Reference

**Files**:
- `.roomodes` - Agent registry
- `.roo/rules-{mode}/instructions.md` - Agent behavior
- `.roo/skills/` - Agent capabilities (Python scripts)
- `results/` - Agent outputs

**Pattern**:
```
Orchestrator discovers agents → Spawns parallel tasks → 
Agents execute autonomously → Write results → 
Orchestrator aggregates → Present synthesis
```

**Templates**: `docs/templates/research-agent-{analyst|skeptic|historian}.md`

**Roo Code Docs**: https://github.com/RooCodeInc/Roo-Code-Docs
