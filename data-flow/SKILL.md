---
name: data-flow
description: Design data pipeline architecture for a given data flow scenario
allowed-tools: Read, Glob, Grep, Task
argument-hint: "<description>"
---

# Data Flow Design Command

Design a data pipeline architecture based on requirements description.

## Usage

```text
/sd:data-flow <description>
```

## Arguments

- `description` (required): Natural language description of data flow requirements
  - Include: data sources, destinations, transformations, latency needs
  - Mention any constraints: cost, team expertise, existing infrastructure

## Examples

```text
/sd:data-flow Real-time customer activity tracking from web and mobile to analytics dashboard

/sd:data-flow Batch ETL from 5 PostgreSQL databases to Snowflake for BI reporting

/sd:data-flow Event streaming from IoT sensors with 10ms latency requirement for anomaly detection

/sd:data-flow Migrate legacy Oracle data warehouse to cloud lakehouse architecture
```

## Workflow

1. **Parse Requirements**
   Extract from description:
   - Data sources and types
   - Volume and velocity estimates
   - Latency requirements
   - Transformation complexity
   - Target systems/use cases

2. **Spawn Data Architect Agent**
   Use the `data-architect` agent to design the pipeline. The agent will:
   - Recommend appropriate architecture (lake/lakehouse/warehouse/mesh)
   - Select pipeline pattern (batch/stream/hybrid)
   - Propose technology stack
   - Design data flow stages

3. **Present Architecture**
   Display the design including:
   - Architecture diagram (ASCII)
   - Technology recommendations with rationale
   - Pipeline stage breakdown
   - Data quality strategy
   - Cost and risk considerations

## Architecture Patterns

The command may recommend:

### Data Platform Types

- **Data Warehouse**: For structured BI/reporting
- **Data Lake**: For ML and diverse data types
- **Data Lakehouse**: For unified BI and ML
- **Data Mesh**: For decentralized domain ownership

### Pipeline Patterns

- **Batch ETL/ELT**: Scheduled bulk processing
- **Stream Processing**: Real-time event handling
- **Lambda**: Batch + speed layers
- **Kappa**: Stream-only with replay

### Processing Frameworks

- **Spark**: Large-scale batch and streaming
- **Flink**: Low-latency streaming
- **dbt**: SQL-based transformations
- **Kafka**: Event streaming backbone

## Output

The command produces a comprehensive design document with:

- Requirements summary
- Recommended architecture with rationale
- Architecture diagram
- Technology stack recommendations
- Pipeline design (stages, transformations)
- Data quality strategy
- Migration path (if applicable)
- Cost considerations
- Risk analysis
