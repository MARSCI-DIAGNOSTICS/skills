# Diagram Best Practices

## General Guidelines

1. **Keep it simple**: Start with the minimum needed to convey the concept
2. **Use consistent naming**: Same entity = same name across diagrams
3. **Label relationships**: Arrows without labels are ambiguous
4. **Use direction thoughtfully**: TD for hierarchies, LR for flows
5. **Group related elements**: Use subgraphs/packages to organize
6. **Add legends**: For complex diagrams with many relationship types

---

## Diagram-Specific Tips

### Sequence Diagrams

- Order participants left-to-right by typical flow
- Use activation bars to show processing time
- Group related interactions with boxes (alt, loop, opt)
- Add autonumber for complex sequences

### Class Diagrams

- Show only relevant attributes/methods
- Use stereotypes to clarify roles (`<<Entity>>`, `<<Service>>`)
- Keep inheritance hierarchies shallow (2-3 levels)
- Position parent classes above children

### ER Diagrams

- Always show primary keys (PK)
- Mark foreign keys (FK)
- Use relationship verbs ("places", "contains")
- Show cardinality on all relationships

### State Diagrams

- Start from [*] initial state
- End at [*] terminal state
- Label all transitions with events
- Use composite states for complex machines

### Flowcharts

- Use consistent shapes (rectangles for actions, diamonds for decisions)
- Flow generally top-to-bottom or left-to-right
- Avoid crossing lines when possible
- Label decision branches clearly (Yes/No, True/False)

---

## Anti-Patterns to Avoid

### Too Much Detail

- **Problem**: Diagram is cluttered and hard to read
- **Solution**: Create multiple focused diagrams at different abstraction levels

### Missing Context

- **Problem**: Diagram shows internal structure but not external interactions
- **Solution**: Start with context diagram, then zoom in

### Inconsistent Abstraction

- **Problem**: Mixing high-level and low-level concepts
- **Solution**: Keep consistent abstraction level per diagram

### Unlabeled Relationships

- **Problem**: Arrows connect things but meaning is unclear
- **Solution**: Always label with verb phrases (e.g., "uses", "contains", "sends")

### Missing Legend

- **Problem**: Custom shapes/colors without explanation
- **Solution**: Add legend for non-standard notation
