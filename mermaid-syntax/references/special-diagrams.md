# Special Diagram Types

## Gantt Chart Syntax

Gantt charts show project timelines and dependencies.

### Basic Syntax

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 7d
    Design          :a2, after a1, 14d

    section Development
    Backend         :b1, after a2, 21d
    Frontend        :b2, after a2, 21d

    section Testing
    Integration     :c1, after b1, 7d
    UAT             :c2, after c1, 7d
```

### Task States

```mermaid
gantt
    title Task States
    dateFormat YYYY-MM-DD

    Completed   :done, t1, 2024-01-01, 5d
    Active      :active, t2, after t1, 5d
    Future      :t3, after t2, 5d
    Critical    :crit, t4, after t3, 5d
    Milestone   :milestone, m1, after t4, 0d
```

---

## Git Graph Syntax

Git graphs visualize branching and merge strategies.

```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature A start"
    commit id: "Feature A done"
    checkout main
    merge develop id: "Release v1.0"
    branch hotfix
    commit id: "Critical fix"
    checkout main
    merge hotfix id: "v1.0.1"
    checkout develop
    merge main
    commit id: "Feature B"
```

---

## C4 Diagram Syntax (Experimental)

C4 diagrams show software architecture at different levels.

**Note:** C4 support in Mermaid is experimental and has rendering limitations. For production C4 diagrams, consider PlantUML.

### C4 Context

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "A user of the system")
    System(system, "My System", "The system being designed")
    System_Ext(email, "Email System", "External email provider")

    Rel(user, system, "Uses")
    Rel(system, email, "Sends emails via")
```

### C4 Container

```mermaid
C4Container
    title Container Diagram

    Person(user, "User", "End user")

    Container_Boundary(c1, "My System") {
        Container(web, "Web App", "React", "Frontend")
        Container(api, "API", "Node.js", "Backend")
        ContainerDb(db, "Database", "PostgreSQL", "Stores data")
    }

    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "Calls", "REST/JSON")
    Rel(api, db, "Reads/Writes", "SQL")
```

---

## Styling and Theming

### Inline Styling

```mermaid
flowchart LR
    A[Start]:::green --> B[Process]:::blue --> C[End]:::red

    classDef green fill:#9f6,stroke:#333,stroke-width:2px
    classDef blue fill:#69f,stroke:#333,stroke-width:2px
    classDef red fill:#f66,stroke:#333,stroke-width:2px
```

### Theme Configuration

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A --> B --> C
```

Available themes: `default`, `dark`, `forest`, `neutral`, `base`

---

## Common Gotchas

1. **Special characters in labels**: Use quotes for labels with special characters

   ```mermaid
   flowchart LR
       A["Label with (parentheses)"]
   ```

2. **Subgraph direction**: Subgraphs inherit parent direction unless specified

   ```mermaid
   flowchart TB
       subgraph sub [Left to Right]
           direction LR
           A --> B
       end
   ```

3. **Node ID restrictions**: IDs cannot start with numbers or contain certain characters
   - Valid: `nodeA`, `node_1`, `myNode`
   - Invalid: `1node`, `my-node` (use `my_node` instead)

4. **Line breaks in labels**: Use `<br/>` for line breaks

   ```mermaid
   flowchart TD
       A["Line 1<br/>Line 2"]
   ```
