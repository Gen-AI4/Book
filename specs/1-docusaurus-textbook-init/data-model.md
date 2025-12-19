# Data Model: Docusaurus Textbook Frontend

## Entities

### Curriculum Module
- **id**: String (unique identifier)
- **title**: String (module title)
- **description**: String (module description)
- **order**: Integer (sequence in curriculum)
- **learningOutcomes**: Array<String> (what students will learn)
- **hardwareRequirements**: Array<String> (specific hardware needed)
- **relatedModules**: Array<String> (links to other modules)

### Textbook Page
- **id**: String (unique identifier)
- **title**: String (page title)
- **content**: String (markdown content)
- **module**: String (parent module id)
- **order**: Integer (sequence in module)
- **codeExamples**: Array<CodeExample> (code snippets in the page)
- **mathFormulas**: Array<String> (LaTeX formulas)
- **diagrams**: Array<String> (Mermaid diagrams)

### Code Example
- **id**: String (unique identifier)
- **language**: String (python, c++, etc.)
- **code**: String (the actual code)
- **description**: String (what the code demonstrates)
- **hardwareConstraints**: Array<String> (specific hardware notes)

### User Interaction
- **id**: String (unique identifier)
- **userId**: String (user identifier)
- **sessionId**: String (session identifier)
- **actionType**: String (navigation, chat, etc.)
- **timestamp**: DateTime (when action occurred)
- **pageId**: String (which page the action occurred on)
- **details**: Object (specific action details)

### Chat Message
- **id**: String (unique identifier)
- **sessionId**: String (chat session identifier)
- **sender**: String (user or bot)
- **content**: String (message content)
- **timestamp**: DateTime (when message was sent)
- **context**: String (text selection or page context)
- **sourceDocuments**: Array<String> (documents referenced in response)