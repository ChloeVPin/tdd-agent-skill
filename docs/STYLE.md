# Writing Style

All documents in this repository use ASD-STE100 Simplified Technical English.

ASD-STE100 is a controlled natural language and an international standard for technical
documentation. ASD, the Aerospace, Security and Defence Industries Association of Europe, owns
it. The standard started in the late 1970s, for aircraft maintenance manuals that persons with
a basic command of English must read correctly. The current issue is Issue 9, January 2025.

Official site: <https://www.asd-ste100.org/>

## Why This Repository Uses It

An agent reads these documents as instructions. Ambiguous text produces ambiguous behaviour.

A person reads "you should generally verify that the test fails" as a strong recommendation. An
agent can read the same sentence as an option that it can decline. The controlled form removes
the ambiguity: "Run the focused command. Read the output."

The rules of ASD-STE100 also help a reader whose first language is not English. A skill of this
type gets copied into many repositories in many countries.

## The Rules

### Write Short Sentences

Use a maximum of 20 words in a procedural sentence. Use a maximum of 25 words in a descriptive
sentence.

| Do not write | Write |
|---|---|
| Because the agent cannot know which command the repository uses, and because a wrong command can silently pass, you must examine the CI configuration before you start. | Examine the CI configuration first. A wrong command can pass and test nothing. |

### Use the Active Voice

The active voice names the actor. The passive voice hides the actor. An agent needs to know who
performs the action.

| Do not write | Write |
|---|---|
| The test must be run before the code is written. | Run the test before you write the code. |
| Coverage was found to be weakly correlated with fault detection. | Inozemtseva and Holmes found a weak correlation between coverage and fault detection. |

### Give One Instruction in One Sentence

| Do not write | Write |
|---|---|
| Run the focused test, check the failure message, and then write the implementation. | Run the focused test. Check the failure message. Then write the implementation. |

### Use One Word for One Meaning

Select one term and use it everywhere. Do not use synonyms for variety.

| Approved term | Do not use |
|---|---|
| test | check, spec, assertion suite |
| defect | bug, issue, problem |
| decrease | reduce, lower, cut, drop |
| examine | look at, inspect, review, check out |
| repository | repo, project, codebase |
| command | invocation, call, script |

### Use Simple Verb Forms

Use the present tense, the simple past, and the simple future. Do not use the present perfect
or complex conditional forms.

| Do not write | Write |
|---|---|
| The agent will have run the tests by that point. | The agent runs the tests first. |
| Had the test been written first, the defect would have been caught. | A test written first finds this defect. |

### Write Instructions as Commands

Start a procedural sentence with the verb.

| Do not write | Write |
|---|---|
| The test command should be found in the manifest. | Find the test command in the manifest. |
| It is recommended that you delete the code. | Delete the code. |

### Do Not Use Noun Clusters of More Than Three Words

| Do not write | Write |
|---|---|
| test suite effectiveness measurement method | the method that measures the effectiveness of a test suite |
| agent skill installation directory path | the path of the directory that contains the skill |

### Write Numbers and Units Clearly

Write "40 to 90 per cent". Do not write "40-90%" in prose. A table can use the short form.

Write "approximately 30 seconds". Do not write "~30s".

### Punctuation

- Do not use em dashes. Use a full stop, a comma, or a colon.
- Do not use semicolons in procedural text. Use two sentences.
- Do not use parentheses for essential information. Put it in its own sentence.
- Do not use emoji.
- Do not use ampersands in prose. Write "and".

### Spelling

Use international English spelling.

| Write | Do not write |
|---|---|
| behaviour | behavior |
| randomised | randomized |
| organisation | organization |
| licence (noun) | license (noun) |
| artefact | artifact |

Keep the American spelling inside code, in file names, and in quoted material. Examples:
`LICENSE`, `color: red`, and the title of a cited paper.

## What Stays Outside the Standard

Code samples keep the conventions of their language. Do not rewrite code to match prose rules.

Quoted titles of papers keep their original spelling and punctuation.

File names and command names are exact. Do not change them.

## Check Your Text

Ask these questions before you commit a document.

- Is each procedural sentence 20 words or fewer?
- Does each sentence give one instruction?
- Is the actor named in each sentence?
- Did you use the same term for the same idea everywhere?
- Are there em dashes? Remove them.
- Are there emoji? Remove them.
- Does each instruction start with a verb?
- Did you use international spelling outside code?
