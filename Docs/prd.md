# Product Requirements Document (PRD)

## Project Name

Student Sticker Tracker Telegram Bot

## Overview

A Telegram bot designed for a math teacher to digitally manage student reward stickers. Instead of manually recording sticker totals and notes in Telegram Saved Messages, the teacher can award stickers directly through Telegram and maintain a live leaderboard.

## Problem Statement

Currently, the teacher gives physical stickers to students at the end of class. Many students forget their folders or binders, forcing the teacher to manually record earned stickers in Telegram Saved Messages. This process is inconvenient, error-prone, and difficult to organize as the number of students grows.

## Goal

Create a Telegram bot that allows the teacher to:

1. Add students to the system.
2. Assign stickers to students quickly during or after class.
3. View sticker standings for all students.

## Target User

* Primary User: Math Teacher
* Secondary Users: Students (view-only access may be added later)

## Core Features (MVP)

### 1. Add New Student

#### Command

`/addstudent`

#### Description

Allows the teacher to add a new student to the database.

#### Flow

1. Teacher enters command.
2. Bot asks for student name.
3. Teacher submits name.
4. Bot confirms successful creation.

#### Example

Teacher:
`/addstudent`

Bot:
`Enter student name:`

Teacher:
`John Smith`

Bot:
`Student John Smith added successfully.`

---

### 2. Assign Stickers

#### Command

`/award`

#### Description

Allows the teacher to award stickers interactively.

#### Flow

1. Teacher enters command.
2. Bot displays list of students.
3. Teacher selects a student.
4. Bot asks how many stickers to add.
5. Teacher selects quantity.
6. Bot updates total and confirms.

#### Example

Teacher:
`/award`

Bot:
Select student:

* John Smith
* Emma Jones
* Alex Brown

Teacher:
Selects John Smith

Bot:
How many stickers?

Teacher:
2

Bot:
John Smith now has 14 stickers.

---

### 3. Sticker Standings

#### Command

`/leaderboard`

#### Description

Displays all students and their current sticker totals.

#### Example

1. Emma Jones — 18 stickers
2. John Smith — 14 stickers
3. Alex Brown — 11 stickers

#### Requirements

* Sorted by highest sticker count.
* Display total stickers next to each student.

---

### 4. Clear Student Stickers

#### Command

`/clear`

#### Description

Reset a student's sticker count to zero.

#### Flow

1. Teacher enters command.
2. Bot displays a list of students.
3. Teacher selects a student.
4. Bot resets that student's sticker count and confirms.

#### Example

Teacher:
`/clear`

Bot:
`Which student?`

Teacher:
Selects John Smith

Bot:
`John Smith's sticker count is now 0.`

## Data Model

### Student

| Field         | Type    |
| ------------- | ------- |
| id            | Integer |
| name          | String  |
| sticker_count | Integer |

## Non-Functional Requirements

### Usability

* Commands should require minimal typing.
* Interactive buttons should be used whenever possible.

### Reliability

* Sticker counts must persist after bot restarts.
* Data should be stored in a database.

### Security

* Only the teacher can use management commands.
* Unauthorized users cannot modify data.

## Future Features (Out of Scope for MVP)

### Sticker History

Track when and why stickers were awarded.

### Sticker Removal

Remove incorrectly assigned stickers.

### Multiple Classes

Support several classes and groups.

### Student Accounts

Allow students to check their own sticker totals.

### Analytics

* Weekly sticker reports
* Most improved student
* Class statistics

## Success Metrics

* Teacher can award a sticker in under 10 seconds.
* No manual tracking in Telegram Saved Messages required.
* All sticker records stored digitally and retrievable at any time.

## Technical Suggestions

* Platform: Telegram Bot
* Backend: Python
* Framework: aiogram or python-telegram-bot
* Database: SQLite (MVP), PostgreSQL (future)
* Hosting: Railway, Render, or VPS

## MVP Definition

The project is considered complete when:

1. Students can be added.
2. Stickers can be assigned interactively.
3. A leaderboard can be displayed.
4. Data persists between restarts.
5. Only the teacher has admin access.
