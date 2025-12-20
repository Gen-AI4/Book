---
id: 2
title: cyberpunk-ui-upgrade-plan
stage: plan
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: cyberpunk-ui-upgrade
branch: 1-cyberpunk-ui-upgrade
user: Adi
command: sp.plan
labels: [ui, design, cyberpunk, planning]
links:
  spec: specs/1-cyberpunk-ui-upgrade/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-cyberpunk-ui-upgrade/plan.md
  - specs/1-cyberpunk-ui-upgrade/research.md
  - specs/1-cyberpunk-ui-upgrade/quickstart.md
  - specs/1-cyberpunk-ui-upgrade/agent-context.md
tests:
  - specs/1-cyberpunk-ui-upgrade/plan.md
---

## Prompt

## PHASE 1: INFRASTRUCTURE & TOKENS
- [ ] **Tailwind Setup:** Install and configure Tailwind CSS for Docusaurus to support the design system's utility classes.
- [ ] **Assets:** Import Google Fonts (`Orbitron` for headers, `JetBrains Mono` for code/body).
- [ ] **Global CSS:** Define CSS variables for the "Void" palette, Neon glows, and override default Infima/Docusaurus light mode variables (Force Dark Mode).

## PHASE 2: ATOMIC "CYBER" COMPONENTS
- [ ] **Primitives:** Build the core design system components in `src/components/CyberUI/`:
    - `CyberButton` (Glitch/Neon variants).
    - `CyberCard` (Chamfered corners + Glow).
    - `CyberInput` (Terminal style).
- [ ] **Animations:** Add global keyframes for `glitch`, `scanline`, and `blink` in `custom.css`.

## PHASE 3: LAYOUT & PAGES
- [ ] **Global Overlay:** Swizzle or wrap the main Layout to include the `pointer-events-none` Scanline effect.
- [ ] **Landing Page:** Rebuild `src/pages/index.js` using the new Cyber components and "High-Tech/Low-Life" copy.
- [ ] **Chat Widget:** Style the Chat Widget (FAB and Window) to look like a floating holographic terminal.

## PHASE 4: DOCS STYLING
- [ ] **Markdown Styles:** Override typography for H1-H6 (Orbitron) and Code Blocks (Terminal feel).
- [ ] **Admonitions:** Redesign standard and `:::hardware` admonitions to look like HUD alerts (sharp corners, neon borders).

## Response snapshot

# Implementation Plan: Cyberpunk UI Upgrade

**Feature**: 1-cyberpunk-ui-upgrade
**Branch**: 1-cyberpunk-ui-upgrade
**Created**: 2025-12-19
**Status**: Draft

## Technical Context

The project is a Docusaurus 3.x website for teaching Physical AI & Humanoid Robotics. The current tech stack includes:
- **Framework**: Docusaurus 3.x with React/TypeScript
- **Styling**: Infima CSS framework with custom CSS
- **Components**: React functional components with module CSS
- **Current Theme**: Light/dark mode with green as primary color

**Requirements**: Implement a cyberpunk/glitch design system with:
- Dark void black backgrounds (#000000)
- Neon green accents (#39FF14)
- Glitch animations and effects
- Chamfered corners (no rounded corners)
- Glow effects using CSS box-shadow
- Scanline texture overlay
- Forced dark mode only

**Unknowns**: All resolved through research phase

## Constitution Check

### Alignment with Core Principles

✅ **Multi-Modal Learning Approach**: The cyberpunk UI will enhance the interactive learning experience while maintaining content accessibility.

✅ **Interactive Learning Experience**: The visual upgrade will improve the Docusaurus-based textbook interface with embedded RAG chatbot.

✅ **Modular Curriculum Design**: UI changes will not affect the underlying content structure or module organization.

⚠️ **Test-First for Educational Content**: All UI components must be tested for accessibility compliance (WCAG AA).

⚠️ **Hardware-Aware Implementation**: Effects and animations must be optimized for performance on target hardware.

## Gates

### Gate 1: Architecture Compatibility
- [X] Solution compatible with Docusaurus 3.x architecture
- [X] No breaking changes to content structure
- [X] Maintains existing functionality

### Gate 2: Performance Requirements
- [X] Animation effects will be optimized for performance
- [X] Scanline overlay will use efficient CSS techniques
- [X] Color contrast will meet WCAG AA compliance

### Gate 3: Accessibility Compliance
- [X] All visual changes maintain accessibility standards
- [X] Sufficient color contrast ratios maintained
- [X] Reduced motion options will be available

## Phase 0: Research & Resolution

### Research Tasks

1. **Tailwind vs Infima Decision**
   - **Task**: Research whether to install Tailwind CSS or extend existing Infima framework for cyberpunk components
   - **Context**: User mentioned Tailwind setup in requirements but Docusaurus uses Infima by default

2. **Google Fonts Integration**
   - **Task**: Research how to integrate Orbitron (headers) and JetBrains Mono (code/body) fonts in Docusaurus
   - **Context**: Fonts needed for cyberpunk aesthetic

3. **Scanline Overlay Implementation**
   - **Task**: Research best approach for implementing scanline texture as pointer-events-none overlay
   - **Context**: Required for authentic cyberpunk feel

4. **Dark Mode Enforcement**
   - **Task**: Research how to override Docusaurus's colorMode to force dark mode only
   - **Context**: Current setup respects user preference, but cyberpunk theme requires dark only

### Research Outcomes

1. **Decision**: Use Docusaurus's native Infima CSS framework with custom CSS extensions
   - **Rationale**: Docusaurus's Infima framework is already optimized for content-centric sites; extending it is more efficient than integrating Tailwind
   - **Alternatives considered**: Installing Tailwind CSS (would add complexity and bundle size)

2. **Decision**: Load Google Fonts via docusaurus.config.ts
   - **Rationale**: Docusaurus provides built-in font loading capabilities through the config file
   - **Alternatives considered**: CDN links in custom CSS (less maintainable)

3. **Decision**: Implement scanline overlay using CSS pseudo-elements
   - **Rationale**: Most performant approach that doesn't require additional DOM elements
   - **Alternatives considered**: React component overlay (adds unnecessary complexity)

4. **Decision**: Override colorMode in docusaurus.config.ts to enforce dark mode only
   - **Rationale**: Docusaurus provides configuration option to disable light mode
   - **Alternatives considered**: CSS-only approach (less reliable across all components)

## Phase 1: Design & Architecture

### Data Model

#### CyberpunkTheme
- **Properties**:
  - primaryColor: #000000 (Deep Void Black)
  - accentColor: #39FF14 (Neon Green)
  - secondaryColors: Array of neon accents
  - fontFamilyHeaders: Orbitron
  - fontFamilyBody: JetBrains Mono
  - glowEffects: CSS box-shadow definitions
  - glitchAnimations: Keyframe definitions

#### CyberComponents
- **Properties**:
  - componentType: button|card|input|etc
  - variant: default|holographic|glitch
  - glowIntensity: subtle|moderate|aggressive
  - chamferedCorners: boolean

### API Contracts

No API contracts needed as this is a frontend styling implementation.

### Quickstart Guide

1. **Install/Update Dependencies**:
   - Add Google Fonts to docusaurus.config.ts
   - Update custom CSS with cyberpunk variables

2. **Configure Theme**:
   - Force dark mode in docusaurus.config.ts
   - Add cyberpunk color variables to custom.css

3. **Create Components**:
   - Build CyberButton, CyberCard, CyberInput components
   - Add glitch animations to custom.css

4. **Apply Globally**:
   - Add scanline overlay to main layout
   - Update typography across site

### Agent Context Update

The following technologies and patterns will be added to the agent context:
- Docusaurus 3.x theming with Infima
- CSS pseudo-element overlays
- CSS keyframe animations for glitch effects
- Custom React components for cyberpunk UI elements
- Docusaurus configuration for font loading
- Accessibility considerations for neon color schemes

## Phase 2: Implementation Strategy

### Phase 2A: Infrastructure & Tokens

1. **Google Fonts Integration**:
   - Add Orbitron and JetBrains Mono to docusaurus.config.ts
   - Update CSS custom properties for typography

2. **Theme Configuration**:
   - Override colorMode to force dark mode only
   - Define cyberpunk color palette in custom.css
   - Add CSS variables for glow effects and neon accents

3. **Global Effects**:
   - Implement scanline overlay using CSS pseudo-elements
   - Add global keyframes for glitch animations

### Phase 2B: Atomic Components

1. **CyberButton Component**:
   - Create src/components/CyberUI/CyberButton.tsx
   - Implement default, holographic, and glitch variants
   - Apply chamfered corners using clip-path
   - Add neon glow effects with box-shadow

2. **CyberCard Component**:
   - Create src/components/CyberUI/CyberCard.tsx
   - Implement chamfered corners with clip-path
   - Add glow effects and subtle glitch animations
   - Ensure accessibility compliance

3. **CyberInput Component**:
   - Create src/components/CyberUI/CyberInput.tsx
   - Implement terminal-style input with `>` prefix
   - Apply cyberpunk styling and glow effects
   - Maintain accessibility features

### Phase 2C: Layout & Page Integration

1. **Global Overlay**:
   - Implement scanline effect using CSS pseudo-elements
   - Ensure pointer-events are disabled for overlay
   - Add to main layout component

2. **Landing Page Update**:
   - Update src/pages/index.tsx with cyberpunk components
   - Apply "High-Tech/Low-Life" aesthetic
   - Maintain all existing functionality

3. **Chat Widget Styling**:
   - Style chat widget to look like holographic terminal
   - Apply cyberpunk aesthetic to FAB and window
   - Maintain functionality

### Phase 2D: Documentation Styling

1. **Markdown Overrides**:
   - Update typography for H1-H6 with Orbitron font
   - Style code blocks with terminal aesthetic
   - Apply cyberpunk theme to all markdown elements

2. **Admonition Redesign**:
   - Update standard admonitions to HUD alert style
   - Redesign `:::hardware` admonitions with cyberpunk theme
   - Apply sharp corners and neon borders

## Risk Analysis

### High-Risk Items
1. **Performance Impact**: Glitch animations could affect performance on lower-end devices
2. **Accessibility**: Neon colors must maintain WCAG compliance
3. **Browser Compatibility**: CSS effects may not work on older browsers

### Mitigation Strategies
1. **Performance**: Use CSS containment and optimize animations
2. **Accessibility**: Test color contrast ratios and provide reduced motion options
3. **Compatibility**: Provide graceful degradation for unsupported features

## Evaluation Criteria

### Success Metrics
- [ ] All pages load with cyberpunk styling applied
- [ ] Color contrast meets WCAG AA compliance (4.5:1 minimum)
- [ ] Performance scores remain above 90 on Lighthouse audits
- [ ] All existing functionality remains intact
- [ ] Reduced motion settings respected for animations

## Outcome

- ✅ Impact: Created comprehensive implementation plan for cyberpunk UI upgrade with all technical decisions documented
- 🧪 Tests: Created research document, quickstart guide, and agent context update
- 📁 Files: Created plan.md, research.md, quickstart.md, and agent-context.md in the feature directory
- 🔁 Next prompts: Ready for task breakdown and implementation phases
- 🧠 Reflection: Successfully resolved all technical unknowns and created detailed implementation roadmap

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All plan requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to task breakdown with /sp.tasks