---
description: Use this skill when writing presenter notes and video scripts for course presentations. Provides techniques for conversational delivery, visual cue integration, pacing, and engagement. Trigger phrases include "video script", "presenter notes", "narration", "video delivery".
---

# Video Scripts - Presenter Notes for Developer Education

Techniques for writing effective presenter notes that enable natural, engaging video delivery.

## Script Philosophy

### Conversational, Not Robotic

**Don't write:**
> "In this slide, we will examine the concept of pointers. A pointer is a variable that stores the memory address of another variable."

**Do write:**
> "So what exactly is a pointer? Think of it like a sticky note with an address written on it. It doesn't hold the actual data - it just tells you where to find it."

### Talking Points, Not Teleprompter

Presenter notes should guide, not dictate. Write key points and transitions, letting the presenter fill in naturally.

```markdown
<!--
Main idea: Pointers store addresses, not values

Key analogy: Sticky note with house address
- The note isn't the house
- It tells you where to find the house
- You can have multiple notes to the same address

[click] Show the diagram - reinforce the mental model
-->
```

---

## Script Structure

### Opening Hook (30-60 seconds)

Every video needs a hook in the first 30 seconds:

**Problem Hook:**
```markdown
<!--
[HOOK] Have you ever had your program crash with a mysterious "segmentation fault"?

You're not alone. Memory errors are one of the most frustrating bugs to track down.

Today, we're going to demystify what's happening under the hood...
-->
```

**Question Hook:**
```markdown
<!--
[HOOK] Quick question: What do you think happens when you write `int x = 5;`?

Most people say "it stores 5 in x" - and that's partially right.

But there's actually a lot more going on...
-->
```

**Curiosity Hook:**
```markdown
<!--
[HOOK] There's a feature in modern C++ that eliminates an entire category of bugs.

And most codebases still aren't using it correctly.

Let's fix that today...
-->
```

### Core Teaching Section

Structure content in digestible chunks:

```markdown
<!--
SECTION: What is a Smart Pointer?

First, let's understand the problem it solves...

[click] Show the manual memory example

This is how we used to do it. Notice we have to remember to delete.

[click] Show what happens when we forget

Memory leak! The program keeps consuming memory until...

[PAUSE] Let this sink in

[click] Now show the smart pointer version

See how the cleanup happens automatically?

[TRANSITION] Now let's look at the different types...
-->
```

### Summary Section

Reinforce learning with clear takeaways:

```markdown
<!--
SUMMARY: Let's recap what we learned

[click] First takeaway - make sure they got this

This is the most important point. If you remember nothing else...

[click] Second takeaway - practical application

You'll use this pattern constantly in real code.

[click] Third takeaway - common mistake to avoid

I see this error in code reviews all the time.

[PAUSE] Give them a moment

[TRANSITION] Now for some practice...
-->
```

---

## Visual Cue Markers

### Animation Cues

| Marker | Usage |
|--------|-------|
| `[click]` | Trigger next Slidev animation |
| `[click:2]` | Skip 2 clicks worth of content |
| `[ANIMATE]` | Complex animation is occurring |

```markdown
<!--
Introduce the concept of ownership...

[click] First bullet appears

Ownership means one thing is responsible for cleanup.

[click] Second bullet

Only the owner can delete the resource.

[click:2] Skip to the code example

Now let's see this in action...
-->
```

### Visual Attention Cues

| Marker | Usage |
|--------|-------|
| `[SHOW CODE]` | Direct attention to code block |
| `[VISUAL CUE]` | Point to diagram or image |
| `[HIGHLIGHT]` | Something is being highlighted |

```markdown
<!--
[SHOW CODE] Look at line 5

Notice how we're using make_unique here.

[VISUAL CUE] The diagram on the right shows memory layout

See how the pointer and the data are in different locations?

[HIGHLIGHT] This line is the key insight
-->
```

### Pacing Cues

| Marker | Usage |
|--------|-------|
| `[PAUSE]` | Brief pause for emphasis |
| `[SLOW]` | Slow down delivery |
| `[TRANSITION]` | Moving to new topic |

```markdown
<!--
And this is the critical insight...

[PAUSE] Let that sink in

[SLOW] Memory. Is. Not. Automatic. In. C++.

[TRANSITION] Now that we understand the problem, let's look at the solution...
-->
```

### Audience Engagement Cues

| Marker | Usage |
|--------|-------|
| `[QUESTION]` | Rhetorical question |
| `[THINK]` | Prompt viewer to think |
| `[EXAMPLE]` | Real-world example coming |

```markdown
<!--
[QUESTION] So what happens when this function returns?

Take a moment to think about it...

[THINK] Where does the memory go?

[EXAMPLE] Let me show you a real bug I found in production code...
-->
```

---

## Writing Techniques

### The Explain-Show-Explain Pattern

1. **Explain** the concept verbally
2. **Show** the code/diagram
3. **Explain** what they're seeing

```markdown
<!--
First, let me explain what we're trying to do.

We want to allocate memory that automatically cleans up.

[click] Show the code

Now look at this code. See how we use make_unique?

The key here is that we never call delete ourselves.
When ptr goes out of scope, cleanup happens automatically.
-->
```

### The Problem-Solution Pattern

Present the pain before the cure:

```markdown
<!--
Here's the old way - manual memory management.

[click] Show problematic code

See all these delete calls? Every single one is a potential bug.

Miss one? Memory leak.
Delete twice? Crash.
Exception thrown? Memory leak.

[PAUSE]

[click] Now the modern way

One line. Automatic cleanup. Exception safe.

This is why smart pointers exist.
-->
```

### The Build-Up Pattern

Start simple, add complexity:

```markdown
<!--
Let's start with the simplest case.

[click] Basic example

Just creating a single integer. Nothing fancy.

[click] Add a function call

Now we're passing it to a function. Still straightforward.

[click] Add exception handling

Here's where it gets interesting. What if process() throws?

[click] Show the problem

See the leak? The delete never runs!

[click] Show the solution

Smart pointer handles this automatically.
-->
```

---

## Tone Guidelines

### Be Conversational

| Instead of... | Say... |
|---------------|--------|
| "We will now examine..." | "Let's look at..." |
| "It should be noted that..." | "Here's the thing..." |
| "The implementation details..." | "Under the hood..." |
| "In conclusion..." | "So what's the takeaway?" |

### Be Empathetic

Acknowledge difficulty:
```markdown
<!--
This part trips up a lot of people, so don't worry if it doesn't click immediately.

Let me show you a different way to think about it...
-->
```

Celebrate progress:
```markdown
<!--
If you understood that, you've already grasped the hardest part.

The rest is just variations on this theme.
-->
```

### Be Direct

Get to the point:
```markdown
<!--
Three rules for smart pointers:

One: Use unique_ptr by default.
Two: Use shared_ptr when you need shared ownership.
Three: Never use raw new.

That's it. Those three rules will prevent most memory bugs.
-->
```

---

## Pacing Guidelines

### Target Video Length: 10-15 minutes

| Section | Time | Slides |
|---------|------|--------|
| Hook/Intro | 30-60s | 1-2 |
| Main Content | 8-12min | 10-20 |
| Summary | 1-2min | 2-3 |
| Call to Action | 30s | 1 |

### Words Per Slide

- **Concept slides:** 100-150 words of notes
- **Code slides:** 50-100 words (code speaks)
- **Summary slides:** 75-100 words

### Clicks Per Slide

- **Aim for:** 2-4 clicks per content slide
- **Maximum:** 6-7 clicks (more gets confusing)
- **Code reveals:** 3-5 steps typically

---

## Common Patterns

### The "Before We Start" Setup

```markdown
<!--
Before we dive in, let me set some context.

We're assuming you know basic C++ syntax.
If terms like "stack" and "heap" are new, check out our memory basics video first.

Ready? Let's go.
-->
```

### The "Common Mistake" Warning

```markdown
<!--
[QUESTION] Now here's where most people go wrong.

[click] Show the bad code

This looks reasonable, right? But there's a subtle bug.

[PAUSE]

Can you spot it?

[click] Highlight the problem

The issue is ownership. Who's responsible for deleting this?

[click] Show the fix

Here's how to fix it...
-->
```

### The "Real World" Connection

```markdown
<!--
[EXAMPLE] I see this pattern in production code all the time.

Just last week, I was reviewing code that looked exactly like this.

[click] Show the code

See the problem? They're storing raw pointers in a vector.

When the function returns, all those pointers are invalid.

This bug made it to production and caused intermittent crashes.

Smart pointers would have prevented it entirely.
-->
```

### The "Pause and Think" Moment

```markdown
<!--
[THINK] Before I show you the answer, try to figure it out yourself.

What do you think happens when we call this function?

[PAUSE] Give them 3-4 seconds

[click] Reveal the answer

If you said "undefined behavior" - you're right!
-->
```

---

## Quality Checklist

Before finalizing presenter notes:

- [ ] Opening has a clear hook
- [ ] Every `[click]` has an explanation
- [ ] Transitions between topics are smooth
- [ ] Pacing allows for natural pauses
- [ ] Technical terms are explained
- [ ] Real-world connections are made
- [ ] Summary reinforces key points
- [ ] Call to action is clear
- [ ] Tone is conversational throughout
- [ ] Visual cues guide attention appropriately
