# Sapien Phase 2 — Quick Start Guide

## One-Minute Setup

```bash
# Navigate to Phase 2 folder
cd Phase\ 2

# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux

# Install dependencies (if not already done)
pip install -r requirements.txt

# Create a local .env file from the example
copy .env.example .env

# Run the MVP demo
python main.py
```

## What You'll See

A didactic episode where:
1. **Episode initialization** → loads axiomatic floor nodes
2. **Chunk processing** → teacher provides 3 conceptual chunks
3. **Question generation** → learner asks 3 questions from gaps
4. **Answer integration** → teacher provides answers with WHY chains
5. **Epistemic closure** → all gaps are filled, learning completes

Expected output: **"✓ Epistemic closure reached"**

## What This MVP Demonstrates

✓ **Knowledge Graph (DAG):** Concepts stored with full provenance  
✓ **Epistemology:** Four states tracked (Known, Known Unknown, SEED, Pending)  
✓ **Curiosity-driven Learning:** Questions generated from identified gaps  
✓ **Causal Reasoning:** WHY chains stored with certainty values  
✓ **Learning Completion:** Epistemic closure when all gaps filled  

## Key Files

- **main.py** — Entry point
- **src/graph/dag.py** — Knowledge graph implementation (SQLite)
- **src/episode/episode_loop.py** — Main learning loop
- **src/agents/learner.py** — Learner agent (gap identification & integration)
- **src/agents/teacher.py** — Teacher interface (ready for real LLM)
- **README.md** — Full documentation
- **PHASE_2_SUMMARY.md** — Completion report

## Next Steps

1. **Customize the topic:** Edit `main.py` line 62
   ```python
   config = EpisodeConfig(
       topic="YOUR_TOPIC_HERE",  # ← change this
       domain="category",         # ← and this
   )
   ```

2. **Integrate real teacher:** Replace `MockTeacher` in `main.py` line 52
   ```python
   teacher = YourLLMTeacher()  # ← connect to OpenAI, Claude, etc.
   ```

3. **Add verifier:** Create `V` agent for hallucination detection

4. **Implement reward gates:** Uncomment logic in REWARD_SPEC.md §4

## Architecture Overview

```
Episode Loop:
  1. Teacher provides chunks on topic
  2. Learner creates KNOWN_UNKNOWN nodes for gaps
  3. Learner generates question from gap
  4. Teacher answers with WHY chain
  5. Learner integrates answer, marks gap as KNOWN
  6. Repeat until no gaps remain (epistemic closure)
```

## Database

SQLite database automatically created: `knowledge_graph.db`

Contains:
- **nodes table:** Concepts with status, WHY chain, provenance
- **edges table:** Relations between concepts (IS_TYPE_OF, CAUSES, etc.)

## Debugging

Check `PHASE_2_SUMMARY.md` for:
- Complete component list
- Spec compliance matrix
- Known limitations
- Next steps

---

**Ready to explore?** Run `python main.py` now!
