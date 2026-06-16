# Live Demo Playbook

A comprehensive guide to planning, preparing, and executing live demonstrations that enhance your technical presentations without becoming disasters.

## The Demo Paradox

Live demos are simultaneously:

- The most engaging part of a technical presentation
- The most likely thing to go wrong
- The best way to build credibility
- The fastest way to lose credibility

**The solution:** Meticulous preparation that makes the demo look effortless.

## When to Demo (and When Not To)

### Demo When

- The product/feature is best understood by seeing it work
- Static slides can't capture the experience
- Interactivity is a key differentiator
- You've had time to prepare properly
- The environment is controllable

### Don't Demo When

- Time is very limited (5-minute lightning talk)
- Network/environment is unreliable
- The feature is too complex to show quickly
- A video would serve the same purpose
- You haven't had time to practice

### Alternative: Recorded Demo

**Consider pre-recorded demos when:**

- Network dependency is high risk
- Setup time would eat into presentation
- The demo is identical every time
- You need to show multiple scenarios

**Recording best practices:**

- Record at 1080p minimum
- Use screen recording software (OBS, ScreenFlow)
- Add subtle zoom/pan to guide attention
- Keep under 2-3 minutes per video
- Have live fallback prepared anyway

## Pre-Demo Preparation

### The 10x Rule

Whatever time you think you need to prepare, multiply by 10.

- **Estimated prep time:** 30 minutes
- **Actual prep time:** 5 hours

This includes: environment setup, scripting, practicing, backup planning, and troubleshooting.

### Environment Checklist

**One week before:**

- [ ] Identify all dependencies (APIs, databases, services)
- [ ] Create isolated demo environment
- [ ] Populate with realistic but safe data
- [ ] Test complete demo flow end-to-end
- [ ] Identify potential failure points
- [ ] Create backup plans for each failure point

**Day before:**

- [ ] Full run-through in demo environment
- [ ] Verify all services are running
- [ ] Check API keys, tokens, credentials
- [ ] Clear caches that might cause issues
- [ ] Pre-stage all browser tabs and windows
- [ ] Test on presentation equipment if possible

**Day of:**

- [ ] Another full run-through
- [ ] Verify network connectivity
- [ ] Check all services still running
- [ ] Close unnecessary applications
- [ ] Disable notifications (ALL of them)
- [ ] Set up screen for presentation (resolution, font size)
- [ ] Have backup ready to activate

### Demo Data Guidelines

**Use realistic but safe data:**

- Real-looking names, emails, content
- Avoid embarrassing or controversial content
- Never use actual customer data
- Never use data that could be offensive

**Data preparation:**

- Create demo users with memorable names
- Pre-populate with enough data to be realistic
- Avoid "test123" or obviously fake data
- Consider cultural sensitivity if global audience

**Examples:**

- Good: "Alex Chen, `alex.chen@example.com`"
- Bad: "`test@test.com`, Password123"
- Good: "Acme Corp" with realistic product data
- Bad: Empty database or "Lorem ipsum" content

### Screen Setup

**Resolution and font size:**

- Present at lower resolution (1280x720 or 1920x1080)
- Increase terminal font to 18-24pt
- Increase IDE/editor font to 16-20pt
- Zoom browser to 125-150%

**Window arrangement:**

- Pre-position all windows you'll need
- Use virtual desktops/spaces if available
- Know your window switching shortcuts
- Consider presentation tools (KeyCastr for Mac)

**Clean your visible areas:**

- Clear desktop of unnecessary icons
- Close irrelevant browser tabs
- Hide personal bookmarks bar
- Clear terminal history if sensitive

## The Demo Script

### Write It Down

Create a detailed script with:

1. **Narration:** What you'll say at each step
2. **Actions:** Exactly what you'll type/click
3. **Checkpoints:** What you expect to see
4. **Recovery:** What to do if something goes wrong

### Script Template

```markdown
## Demo Section: [Name]

### Setup
- Browser tab: [URL]
- Terminal: [directory, commands run]
- State: [what should be true before starting]

### Flow

1. **Narration:** "Let me show you how we..."
   **Action:** Click on [element]
   **Expect:** [Page/modal should appear]
   **Recovery:** If not, [backup action]

2. **Narration:** "Now I'll enter..."
   **Action:** Type: [exact text]
   **Expect:** [autocomplete/validation]
   **Recovery:** If API slow, "Sometimes this takes a moment..."

3. ...
```

### Timing Landmarks

Build in checkpoints:

- At 2 minutes: Should have shown [X]
- At 5 minutes: Should be at [Y]
- At 8 minutes: Should be wrapping up

**If behind:** Skip optional sections (mark them in advance)

**If ahead:** Have optional deep-dives ready

## Execution Techniques

### The Narration Layer

**Narrate continuously:**

- Explain what you're about to do
- Describe what's happening on screen
- Point out what the audience should notice
- Fill loading/transition time with context

**Example narration flow:**

"Now I'm going to show you the search feature. I'll type in a product name here... notice how the autocomplete is showing suggestions from our catalog... and when I select this one, you'll see the detail page load with all the product information."

### Pacing

**Slow down:**

- Type slower than normal
- Pause after important actions
- Let the audience absorb what they're seeing
- Give them time to read what's on screen

**Navigate deliberately:**

- Don't frantically click around
- Explain why you're clicking each thing
- If you make a wrong click, acknowledge and correct calmly

### Pointer and Focus

**Guide attention:**

- Use mouse cursor to point at key elements
- Consider annotation tools (Zoom, OBS)
- Verbally direct: "Look at the top right corner..."
- Highlight code blocks as you discuss them

**Avoid:**

- Moving cursor aimlessly
- Pointing at one thing while talking about another
- Assuming audience knows where to look

### Handling Delays

**When things are loading:**

- "This usually takes just a moment..."
- Fill with context: "While this loads, let me explain..."
- Have a planned tangent ready
- Stay calm - don't apologize excessively

**When things are slow:**

- "Looks like we might be hitting some network latency..."
- Offer context without panic
- Switch to backup if it's taking too long

## When Things Go Wrong

### The 30-Second Rule

If something breaks:

1. **Acknowledge briefly:** "Hmm, that's not what we expected"
2. **Try ONE quick fix:** Refresh, retry, check obvious issue
3. **Time limit: 30 seconds maximum**
4. **If still broken:** Switch to backup immediately
5. **Continue with confidence**

### Backup Strategies

#### Tier 1: Alternative path

Different way to show the same thing:

- Different user account
- Different data set
- Different endpoint

#### Tier 2: Pre-recorded video

Recorded version of the demo:

- "Let me show you a recording of this working..."
- Narrate over the video
- Continue with presentation

#### Tier 3: Screenshots/slides

Static images of the working demo:

- "I have some screenshots here..."
- Walk through step by step
- Still valuable, just not live

#### Tier 4: Verbal description

Describe what would happen:

- "What you would see here is..."
- Keep brief, move on
- Acknowledge and continue

### Language for Recovery

**Stay calm and professional:**

- "Interesting - this isn't behaving as expected"
- "Let me try an alternative approach"
- "This sometimes happens - let me show you another way"
- "I'll switch to my backup for this section"

**Avoid:**

- Excessive apologies
- Visible frustration
- Blaming technology
- "This always works in practice..."
- Long debugging attempts

### Post-Failure Recovery

After switching to backup:

1. **Move on quickly** - Don't dwell on what failed
2. **Maintain energy** - Don't let it deflate you
3. **Complete the demo story** - Finish what you started
4. **Optional: Circle back** - "I'll debug that offline"

## Demo Types

### Interactive UI Demo

**Best practices:**

- Larger font/zoom than you think
- Clear, deliberate actions
- Narrate every click
- Avoid hover-dependent interactions (hard to see)

**Common issues:**

- Authentication expiring mid-demo
- Session timeouts
- Data changing between setups

### Command Line Demo

**Best practices:**

- Large terminal font (20pt+)
- Clear prompt that shows context
- Pre-stage commands (but type key ones live)
- Use aliases for long commands
- Clear terminal between sections

**Techniques:**

- `history` to recall pre-staged commands
- Store commands in a file, copy-paste key ones
- Use tmux/screen for multiple panes
- Consider terminal recording (asciinema)

**Common issues:**

- Commands too long for screen
- Output scrolling too fast
- Errors from typos
- Environment variable issues

### API Demo

**Best practices:**

- Use Postman, Insomnia, or similar (not raw curl)
- Pre-save all requests
- Show request AND response
- Highlight key parts of response

**Techniques:**

- Environment variables for secrets
- Pre-authorized tokens
- Saved example responses as backup

**Common issues:**

- Rate limiting
- Token expiration
- CORS issues (if browser-based)
- API changes since you practiced

### Code/IDE Demo

**Best practices:**

- Increase editor font size
- Minimize visible UI (focus on code)
- Pre-position at starting point
- Use code folding to hide irrelevant sections

**Techniques:**

- Multiple pre-staged branches (git checkout demo-step-1)
- Live coding only for small, impactful changes
- Snippets for boilerplate
- Split screen (code left, result right)

**Common issues:**

- Linter errors distracting
- Autocomplete popups obscuring view
- Build errors from dependencies
- Test failures from environment issues

## Demo Checklist

### One Week Before

- [ ] Create isolated demo environment
- [ ] Write complete demo script
- [ ] Practice full demo 3x
- [ ] Create all backup materials
- [ ] Identify all dependencies
- [ ] Test backup recovery scenarios

### Day Before

- [ ] Full run-through in actual environment
- [ ] Test on presentation equipment (if possible)
- [ ] Verify all services running
- [ ] Charge all devices
- [ ] Export/upload backup to multiple locations

### Morning Of

- [ ] Full run-through
- [ ] Verify network connectivity
- [ ] Clear notifications (phone, laptop)
- [ ] Close unnecessary apps
- [ ] Pre-stage all windows/tabs
- [ ] Test screen sharing (if remote)
- [ ] Verify audio/video (if remote)

### Right Before

- [ ] Final quick test of demo path
- [ ] Verify backup is accessible
- [ ] Deep breath
- [ ] Remember: if it breaks, you have a plan

## Remote Demo Considerations

### Screen Sharing

**Before sharing:**

- Close personal/sensitive windows
- Clean up desktop
- Set appropriate resolution (720p often better for bandwidth)
- Test screen share before starting

**During sharing:**

- Share specific window, not entire screen
- Announce what you're sharing
- Confirm audience can see: "Can everyone see my browser?"
- Check chat for issues

### Network Dependencies

**Mitigations:**

- Use wired connection if possible
- Close bandwidth-heavy applications
- Have mobile hotspot as backup
- Consider VPN impact on latency
- Pre-load resources before demo

### Audio Considerations

- Mute notifications
- Use headphones to prevent feedback
- Test microphone levels before starting
- Have backup audio device available

## Example Demo Flow

### Setup

- Browser with app open, logged in as demo user
- Terminal with project directory open
- Slides in presenter mode on second display
- Backup video on accessible drive
- Phone silenced and face-down

### Transition from Slides

"Now let me show you this in action. I'm going to switch to my browser where I have our application running..."

[Switch to browser]

"So here we are in the dashboard. You can see we have our demo user Alex logged in, and they've got a few projects already set up."

### Demo Core

[Follow scripted flow]

- Narrate continuously
- Pause at key moments
- Check timing landmarks
- Watch for warning signs

### Recovery Example

"Hmm, it looks like the API is being slow today. Let me show you a recording of this - it's the same flow you'd see live..."

[Switch to backup video]

[Narrate over video]

### Return to Slides

"So that's the core functionality in action. Let me switch back to my slides to talk about what this means for your workflow..."

---

**Related:** Return to `technical-presentations` skill for the complete framework, or see `presentation-checklist.md` for preparation lists.
