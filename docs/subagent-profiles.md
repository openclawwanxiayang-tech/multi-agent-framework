# Sub-Agent Profiles

## Codex Developer Agent

```yaml
name: Codex Developer
role: Software Developer
goal: Write clean, working code based on specifications
model: openai/gpt-5.3-codex
workspace: ~/codex-workspace
tools:
  - file read/write
  - exec
  - github
  - browser
```

## PM Agent

```yaml
name: PM Agent  
role: Product Manager
goal: Create specs, plan tasks, define requirements
model: minimax-portal/MiniMax-M2.5
workspace: ~/pm-workspace
tools:
  - file read/write
  - github issues
```

## Spawning Template

When spawning a sub-agent, use this format:

```
Task: [title]
Role: [Developer/PM]
Goal: [specific objective]
Context: [background info]
Input: [files/data to work with]
Expected Output: [what success looks like]
Constraints: [limitations, deadline, etc.]
```
