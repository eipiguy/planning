---
author: eipiguy
project: planning
title: Title
tags: [log, planning, template]
date: 2023-07-24
---

All things change, and all things in this document and its template will evolve over time. Keep records when things go unexpectedly.

## Method

[How does it work?](#goals) [What depends on what?](#constraints) What gets done in what order? Change this as necessary.

<div class="mermaid">
flowchart LR
  A[Sharp Corner Box] -->|Arrow Text| B(Rounded Box);
  B --> C{Decision Diamond};
  C -->|Option 1| D[Result 1];
  C -->|Option 2| E[Result 2];
</div>

## Metrics

Tests just pass or fail, but metrics are your details. Can you know what needs to be tested without first knowing what you care about? What are the parts of the project, and how do you measure each of them?

| Metric \\ Cost  |  1  |  2  |  3  |
|:---             |:---:|:---:|:---:|
| Excitement      |  😄  |  🫤  |  😓  |
| Cost            |  🥩  |  🍞  |  💍  |
| Complexity      |  🐁  |  🐉  |  ☠️  |
| Duration        |  🚀  |  ✈️  |  🚌  |
| Maintenance     |  🎄  |  📆  |  ⏰  |

### Legend Standard

For automatic parsing purposes, use the format:

- metric names in a dashed list
  1. desired outcomes first in a numbered sub-list using any of the following formats:
  2. :emoji: emoji key = description of evaluation
  3. 😛 stuck_out_tongue = I'm giving an example
  4. ([box style]) = description of evaluation

All formats should be consistent, ie. the same, per metric. Don't mix emojis with box style in the same metric for instance: keep those as separate metrics.

### Legend

- Excitement
  1. 😄 smile = passionate
  2. 🫤 face_with_diagonal_mouth = meh
  3. 😓 sweat = chore
- Cost
  1. 🥩 cut_of_meat = profitable
  2. 🍞 bread = cheap
  3. 💍 ring = expensive
- Complexity
  1. 🐁 mouse2 = easy
  2. 🐉 dragon = challenging
  3. ☠️ skull_and_crossbones = extreme
- Duration
  1. 🚀 rocket = less than weeks up front
  2. ✈️ airplane = months up front
  3. 🚌 bus = years up front
- Progress
  1. ([rounded box]) = working deliverable
  2. {{angled box}} = making progress
  3. [square box] = new idea
- Maintenance
  1. 🎄 christmas_tree = up to yearly maintenance
  2. 📆 calendar = monthly maintenance
  3. ⏰ alarm_clock = more than weekly maintenance

## Records

A table of the "health records" of the project's components

|Date         |Metric 1 | Metric 2  |
|-            |-        |-          |
|2023-07-08   |Purple   |85%        |
|2023-07-15   |Blue     |85%        |
|-            |-        |-          |

## Testing

How do we run [tests](#testing)? Tests should just pass or fail. How do we interpret failures and file an item? Where do we track bugs?

1. Where is the main test file?
2. Test names reflect what failed and why
3. More details available in a [log somewhere](#records)
