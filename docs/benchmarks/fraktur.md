# Metadata and Textual Extraction of classified ads in the Basler Avisblatt (1729--1844)

## Table of Contents
- [Overview](#overview)
- [Creator](#creator)
- [Basler Avisblatt](#basler-avisblatt)
- [Ground Truth](#ground-truth)
  - [Guidelines for creating the ground truth](#guidelines-for-creating-the-ground-truth)
  - [Metadata schema](#metadata-schema)
- [Scoring](#scoring)
  - [Scoring an ad](#scoring-an-ad)
  - [Scoring the collection](#scoring-the-collection)
- [To Dos](#to-dos)

## Overview

This benchmark focuses on the extraction of metadata and text of classified ads in an early modern advertisement newspaper, the Basler Avisblatt (1729--1844). It provides a ground truth for the metadata categories `date`, `tags_section` and `ntokens` (number of tokens) for a collection of classified ads from the newspaper. It also extracts the text of the ads.

## Creator

This benchmark was created by the University of Basel's Research and Infrastructure Support RISE (rise@unibas.ch) in 2025.

## Basler Avisblatt

This benchmark uses as input the digital collection of the "Basler Avisblatt" (shelf mark: `UBH Ztg 1`, digitial collection: https://avisblatt.dg-basel.hasdai.org/search?q=&l=list&p=1&s=10&sort=newest) of the University Library Basel.

The collection consists of 116 yearbooks for every year of its appearance, each year containing ~ 52 issues, with more issues per year during the 1840s. The length of the issues varies over the years, from 1 up to 16 pages. The content is mainly classified ads, with some news-like articles or price lists or announcements, and it's printed in Gothic type.

## Ground Truth



#### Metadata schema
                                               
                                               



## Scoring

### Scoring an ad

#### Example

### Scoring the collection

With scores for each ad in place, we can calculate the overall performance of an LLM on the collection. We calculate F1-micro and F1-macro:

- F1 is the harmonic mean of precision and recall, where precision is TP / (TP + FP) and recall is TP / (TP + FN).
- F1-micro is the harmonic mean of precision and recall across all categories.
- F1-macro is the average of F1 scores across all categories.

## To Dos

Entity extraction: Persons, Places

## Test Results

