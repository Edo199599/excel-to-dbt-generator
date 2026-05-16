# Excel to dbt Generator

A Python tool that reads technical Excel specifications and generates structured artifacts for dbt and data engineering workflows.

The goal of this project is to make Excel-based mapping documents easier to inspect, validate and convert into reusable outputs such as contracts, dbt models and warning reports.

This is not an AI-first project.  
The core logic is deterministic and based on explicit parsing rules.

## Why this project exists

In many data projects, technical specifications are still shared as Excel files.

These files often contain important information such as:

- source fields
- target fields
- data types
- transformation rules
- mandatory flags
- notes and comments
- sheet-level metadata

The problem is that Excel files are flexible, but not always easy to validate or reuse in automated pipelines.

This project explores how to convert those semi-structured specifications into clean, versionable and machine-readable artifacts.

## Project goals

The project aims to generate:

- a JSON contract
- a dbt `schema.yml`
- a dbt SQL skeleton
- a structured warning report
- an `override_template.yml` file for manual corrections

The Excel source file is never modified.

Any correction or clarification should be handled through overrides, so that the original business specification remains untouched.

## Current focus

The first module of the project is `excel_inspector.py`.

Its goal is to inspect a multi-sheet Excel file and make its structure observable before generating any final output.

At this stage, the module focuses on:

- reading workbook sheet names
- identifying candidate sheets
- detecting possible header rows
- recognizing known columns
- extracting basic metadata
- producing initial warnings

This step is intentionally separated from the generation phase.

Before generating JSON, YAML or SQL, the project needs to understand how reliable the Excel structure is.

## High-level flow

```text
Excel file
   ↓
Excel inspector
   ↓
Canonical schema / mapping
   ↓
Structured warnings
   ↓
User-approved overrides
   ↓
Python generators
   ↓
JSON contract / dbt YAML / SQL skeleton / reports