---
author: eipiguy
project: planning
title: Title
tags: [log, readme, template]
date: 2023-07-14
---

## Current Intent

What's the idea? What are you currently trying to do?

What are you trying to get out of the whole thing?

What do you think it will take at the most general levels?

### Record of Past Intents

All things change, and all things in this document and its template will evolve over time.

## Influences

You'll be reinventing the wheel if you don't go to the market and see what other people have already done.

- A
- B

## Current Understandings

What do you think you know? What have you learned as you've been working? Current mental model doesn't have to be perfect, but it should be there. Refine rather than re-build.

## Questions

What do we want to figure out? What do we need to learn to continue working?

## Goals

Start with [big concepts](#summary) and [break them down](#influences) into [progressively smaller bits](#distinctions) until you have [things that seem manageable](#goals).

This is an evolving list. It will change based on obstacles and requirements that arise, and will grow and shrink as tasks are completed, added, and learning makes bigger tasks easier.

- [ ] Main thing to do
  - [ ] There are always parts to it
  - [ ] More than one thing makes a list
- [ ] Make a follow up task

> Tasks age like milk, not like wine. Only plan what is necessary. "Pie in the sky" ideas go in separate documents.

### Constraints?

## Method

[How does it work?](#goals) [What depends on what?](#constraints) What gets done in what order? Change this as necessary.

```mermaid
flowchart LR
  A[Sharp Corner Box] -->|Arrow Text| B(Rounded Box);
  B --> C{Decision Diamond};
  C -->|Option 1| D[Result 1];
  C -->|Option 2| E[Result 2];
```

## Metrics

Tests just pass or fail, but metrics are your details. Can you know what needs to be tested without first knowing what you care about? What are the parts of the project, and how do you measure each of them?

| Metric \\ Cost  |  1  |  2  |  3  |
|:---             |:---:|:---:|:---:|
| Excitement      |  😄  |  🫤  |  😓  |
| Cost            |  🥩  |  🍞  |  💍  |
| Complexity      |  🐁  |  🐉  |  ☠️  |
| Duration        |  🚀  |  ✈️  |  🚌  |
| Maintenance     |  🎄  |  📆  |  ⏰  |

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


### Records

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
