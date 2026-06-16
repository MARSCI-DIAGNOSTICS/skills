# Pair Programming Guide

A guide to effective pair programming, especially in mentoring contexts.

## What Makes Pairing Valuable

Pair programming isn't just about writing code together - it's about:

- Transferring tacit knowledge (the stuff not in docs)
- Modeling thought processes
- Creating psychological safety to ask questions
- Building shared understanding of the codebase

## Roles

### Driver

The person at the keyboard:

- Writes the code
- Focuses on the immediate implementation
- Narrates what they're doing
- Asks questions when stuck

### Navigator

The person observing:

- Thinks about the bigger picture
- Spots bugs and improvements
- Asks clarifying questions
- Reviews code in real-time

### Rotation

Switch roles regularly:

- Every 15-30 minutes (use a timer)
- At natural breakpoints (completing a feature)
- When the navigator has ideas they want to try

**In mentoring contexts:** Have the mentee drive more often - they learn by doing.

## Communication Patterns

### Think Aloud

The most important habit. Verbalize your thought process:

**Good example (when driving):**
> "I'm adding this null check because getUserById could return undefined if the user was deleted. Let me also add a meaningful error message so debugging is easier..."

**Good example (when navigating):**
> "I'm wondering if we should handle the case where the array is empty. What do you think happens if items.length is zero?"

### Asking Permission

Never take over without consent:

✅ "Mind if I drive for a minute? I want to show you something."
✅ "Can I try a different approach? I'll explain as I go."

❌ *Reaching for the keyboard mid-thought*
❌ "Just let me fix this real quick."

### Productive Disagreement

When you see something differently:

✅ "I have a different idea - want to hear it?"
✅ "What if we tried X? Let's compare both approaches."
✅ "Interesting! I'd have done it differently. What made you choose this?"

❌ "That's wrong."
❌ Silently judging while they work.

## For Mentors

### Create Safety

Make it comfortable to struggle:

- Share your own mistakes and learnings
- Normalize looking things up
- Celebrate progress, not perfection

### Narrate Your Thinking

When you drive, show your process:

- "I always start by understanding the inputs and outputs..."
- "My instinct says X, but let me verify..."
- "I'm not sure about this, let me check the docs..."

### Let Them Struggle (Productively)

The discomfort of figuring things out is where learning happens.

**Productive struggle:** They're thinking, trying things, making progress.
**Unproductive struggle:** They're stuck, frustrated, spinning.

**Intervention points:**

- After 5-10 minutes of no progress
- When frustration is replacing curiosity
- When they ask for help

### Ask, Don't Tell

Use questions to guide:

| Instead of... | Ask... |
| ------------- | ------ |
| "You need to add error handling" | "What happens if this fails?" |
| "Use a map instead" | "What data structure would make lookups faster?" |
| "That won't work" | "What would happen with [edge case]?" |

### Know When to Just Tell

Socratic questioning isn't always right:

- Simple factual questions
- Syntax they couldn't guess
- When they're overwhelmed
- Time-sensitive situations

## For Mentees

### Embrace the Discomfort

Struggling is learning. It's supposed to feel hard sometimes.

### Ask Questions Freely

- "Why did you do it that way?"
- "What made you look there first?"
- "How did you know that?"

These aren't annoying - they're the point.

### Take Notes

Keep a doc open for:

- New concepts and patterns
- Tools and shortcuts you learned
- Follow-up topics to explore

### Speak Up When Confused

Don't nod along when lost:

- "Could you explain that part again?"
- "I'm not following - can you slow down?"
- "What's [term] mean?"

## Remote Pairing

### Tools

- **Screen sharing:** Zoom, Meet, or IDE-native (VS Code Live Share)
- **Shared control:** VS Code Live Share, Tuple, Pop
- **Drawing:** Excalidraw, Miro for architecture discussions

### Challenges

| Challenge | Mitigation |
| --------- | ---------- |
| Latency | Use collaborative IDE tools (Live Share) |
| Can't see body language | Over-communicate verbally, cameras on |
| Audio quality | Use good headsets, mute when not talking |
| Distraction | Close other apps, treat it like in-person |
| Screen visibility | Share at appropriate resolution |

### Best Practices

- Cameras on (helps with engagement)
- Check in frequently ("Following along?" "Any questions?")
- Take more breaks than in-person (screen fatigue is real)
- Use screen annotations to point at things

## When Not to Pair

Pairing isn't always the right tool:

- **Deep individual thinking:** Some problems need solo focus first
- **Well-understood tasks:** If both could do it alone, pairing adds overhead
- **Incompatible styles:** Some people just don't pair well together
- **Time-sensitive production issues:** Sometimes you just need to fix it

## Pairing Smells

**Signs it's going badly:**

- One person does all the driving
- Silence for long periods
- One person checks their phone/email
- "Just let me do it" frustration
- Mentee nods but doesn't contribute

**How to fix:**

- Switch roles
- Take a break
- Check in: "How's this going for you?"
- Discuss the dynamic explicitly

## Making It Work for Mentoring

**For new relationships:**

- Start with a simple task
- Explain the goal and your expectations
- Check in frequently: "How's the pace?"

**For ongoing relationships:**

- Increase complexity over time
- Have them drive more as they grow
- Eventually, have them mentor someone else with you observing

**Measure success:**

- They ask good questions
- They catch bugs you miss
- They can explain the code to someone else
- They can do similar tasks solo

## Pairing Agreements

Consider establishing explicit agreements:

```markdown
## Our Pairing Agreement

1. Either person can ask to switch roles at any time
2. We think aloud, even when it feels awkward
3. Questions are encouraged, never judged
4. We take breaks every 45-60 minutes
5. We end with a brief retro: "What went well? What could we improve?"
```
