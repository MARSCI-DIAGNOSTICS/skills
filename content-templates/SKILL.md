---
description: Use this skill when creating structured educational content. Provides templates for chapters, exercises, projects, labs, slides, and assessments. Trigger phrases include "content template", "chapter structure", "exercise format", "lab template", "slide template", "quiz format".
---

# Content Templates

Structural templates for different types of programming educational content.

## Chapter Template

```markdown
# Chapter [X]: [Topic Name]

## Learning Objectives
By the end of this chapter, you will be able to:
- [Objective 1 - action verb + specific skill]
- [Objective 2]
- [Objective 3]

## Prerequisites
Before starting this chapter, you should understand:
- [Prerequisite 1]
- [Prerequisite 2]

## Introduction
[1-2 paragraphs motivating the topic]
- Why does a developer need to know this?
- What problems does it solve?
- How does it connect to previous chapters?

## [Section 1: Core Concept]

### The Problem
[What situation or challenge leads us to need this concept?]

### A First Look
```[language]
// Working code example showing the concept in action
```

**Output:**
```
[Actual output from running the code]
```

### How It Works
[Break down the code piece by piece]

### Key Points
- [Important point 1]
- [Important point 2]

### Common Mistakes

```[language]
// Code that demonstrates a common error
```

**Error:**
```
[Compiler or runtime error message]
```

**Why this happens:** [Explanation]

**The fix:**
```[language]
// Corrected code
```

## [Section 2: Deeper Understanding]
[Build on the basics with more detail]

## [Section 3: Practical Application]
[Real-world use case with full implementation]

## Exercises

### Exercise 1: [Name] (Beginner)
[Clear problem statement]

**Starter code:**
```[language]
// Scaffolded code for student to complete
```

**Expected behavior:**
```
[Sample input/output or test cases]
```

### Exercise 2: [Name] (Intermediate)
[Problem requiring synthesis of concepts]

### Exercise 3: [Name] (Challenge)
[Open-ended problem for advanced students]

## Summary
- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

## What's Next
[Preview of next chapter and how it builds on this]

## Further Reading
- [Resource 1 - official documentation]
- [Resource 2 - deeper dive]
```

## Coding Exercise Template

```markdown
# Exercise: [Name]

**Difficulty:** [Beginner/Intermediate/Advanced]
**Estimated Time:** [X minutes]
**Concepts Practiced:** [Concept 1, Concept 2]

## Problem Statement

[Clear, unambiguous description of what to build]

## Requirements

1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

## Starter Code

```[language]
// Provided structure for student to complete
// TODO comments indicate where students should write code
```

## Test Cases

```[language]
// Tests to verify the solution
// Students can run these to check their work
```

**Expected Output:**
```
Test 1: PASS
Test 2: PASS
...
```

## Hints (Use sparingly!)

<details>
<summary>Hint 1</summary>
[First gentle nudge]
</details>

<details>
<summary>Hint 2</summary>
[More specific guidance]
</details>

## Solution

<details>
<summary>Click to reveal solution</summary>

```[language]
// Complete working solution
```

**Explanation:**
[Why this approach works]

</details>

## Extension Challenges

For students who finish early:
1. [Additional challenge 1]
2. [Additional challenge 2]
```

## Project Template

```markdown
# Project: [Name]

**Duration:** [X hours/days]
**Difficulty:** [Intermediate/Advanced]
**Technologies:** [Language, libraries, tools]

## Overview

[1-2 paragraphs describing what students will build]

## Learning Goals

By completing this project, you will:
- [Goal 1]
- [Goal 2]
- [Goal 3]

## Project Specification

### Requirements

**Core Features (Required):**
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

**Stretch Goals (Optional):**
1. [Enhancement 1]
2. [Enhancement 2]

### Technical Constraints

- [Constraint 1 - e.g., must use standard library only]
- [Constraint 2 - e.g., no external dependencies]

## Getting Started

### Step 1: Project Setup
[Instructions for creating the project structure]

```bash
# Commands to set up the project
```

### Step 2: [First Milestone]
[Guidance for first working piece]

### Step 3: [Second Milestone]
[Building on the first piece]

### Step 4: [Integration]
[Bringing pieces together]

## Testing Your Project

```[language]
// Test cases or testing instructions
```

## Submission Requirements

1. [What to submit]
2. [Format requirements]
3. [Documentation requirements]

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | X% | Code works as specified |
| Code Quality | X% | Readable, well-organized |
| Testing | X% | Adequate test coverage |
| Documentation | X% | Clear comments and README |
```

## Lab/Workshop Template

```markdown
# Lab [X]: [Topic Name]

**Duration:** [X minutes/hours]
**Format:** [Individual/Pair/Group]
**Environment:** [IDE, online compiler, etc.]

## Learning Objectives
- [Objective 1]
- [Objective 2]

---

## Part A: Guided Practice ([X minutes])

### Setup
```[language]
// Initial code to start with
```

### Step 1: [First Concept]
[Explanation of what to do]

```[language]
// Code to write or modify
```

**Try it:** Run the code and observe [specific output]

### Step 2: [Building On]
[Next step in the progression]

### Checkpoint
At this point, your code should:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Part B: Independent Challenges ([X minutes])

Work on these challenges independently or with a partner.

### Challenge 1: [Name] (5-10 min)
[Problem statement]

### Challenge 2: [Name] (10-15 min)
[Problem statement building on Challenge 1]

### Challenge 3: [Name] (15-20 min)
[More complex integration challenge]

### Challenge 4: [Name] (Extension)
[For students who finish early]

---

## Wrap-up

### Reflection Questions
1. What was the most challenging part?
2. What would you do differently next time?
3. How could you extend what you built?

### Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
```

## Slides Template (Quarto RevealJS)

```markdown
---
title: "[Topic Name]"
author: "[Instructor Name]"
format:
  revealjs:
    theme: default
    code-line-numbers: true
    highlight-style: github
---

## Learning Objectives

- Objective 1
- Objective 2
- Objective 3

::: notes
Set expectations for what students will learn
:::

---

## Why This Matters

[Real-world motivation]

**In practice:** [Concrete example from industry]

::: notes
Hook students with relevant context
:::

---

## [Concept]: First Look

```{.[language]}
// Simple example code
```

::: {.fragment}
**Output:**
```
[What this produces]
```
:::

::: notes
Walk through each line
:::

---

## Let's Build It Up

:::: {.columns}
::: {.column width="50%"}
**Step 1:**
```{.[language]}
// First piece
```
:::
::: {.column width="50%"}
**Step 2:**
```{.[language]}
// Adding to it
```
:::
::::

::: notes
Incremental code building
:::

---

## Common Mistake

```{.[language]}
// Code with a bug
```

::: {.fragment}
**Error:**
```
[Error message]
```
:::

::: {.fragment}
**How to fix it:** [Explanation]
:::

---

## Your Turn

Given this code:
```{.[language]}
// Code to analyze
```

**Question:** What will this output?

::: {.fragment}
**Answer:** [Revealed answer]
:::

::: notes
Give students 1-2 minutes to think
:::

---

## Live Coding: [Task]

Let's build [feature] together.

[Space for live demonstration]

::: notes
Key points to hit during live coding:
- Point 1
- Point 2
:::

---

## Key Takeaways

1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

**Next time:** [Preview]

---

## Questions?

[Contact info or office hours]
```

## Quiz/Assessment Template

```markdown
# Assessment: [Topic Name]

**Time Limit:** [X minutes]
**Open/Closed:** [Book, notes, IDE?]
**Total Points:** [XX]

---

## Part 1: Code Reading ([X points])

### Question 1 ([X points])
What does the following code output?

```[language]
// Code to trace
```

**Answer:** ____________

### Question 2 ([X points])
This code has a bug. Identify it and explain how to fix it.

```[language]
// Buggy code
```

**Bug:** ____________
**Fix:** ____________

---

## Part 2: Code Writing ([X points])

### Question 3 ([X points])
Write a function that [specification].

**Function signature:**
```[language]
// Provided signature
```

**Your code:**
```[language]
// Space for answer
```

### Question 4 ([X points])
Implement [more complex task].

**Requirements:**
- [Requirement 1]
- [Requirement 2]

---

## Part 3: Conceptual ([X points])

### Question 5 ([X points])
Explain why [concept] is important in [context].

### Question 6 ([X points])
Compare and contrast [approach A] and [approach B].

---

## Answer Key (Instructor Only)

[Detailed answers and grading rubric]
```

## Usage Guidelines

### When to Use Each Template

- **Chapter**: Comprehensive coverage of a topic for self-study or reference
- **Coding Exercise**: Focused practice on specific skills
- **Project**: Larger, integrative work combining multiple concepts
- **Lab/Workshop**: Structured in-class hands-on session
- **Slides**: Support for lecture or live demonstration
- **Quiz/Assessment**: Evaluate student understanding

### Customization

These templates should be adapted based on:
- Target audience experience level
- Programming language and toolchain
- Course philosophy (framework vs. no-framework)
- Time available
- Prerequisites
- Learning environment (IDE, online, etc.)

Always reference the specific course profile for customization guidance.
