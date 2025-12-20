# Research Document: Cyberpunk UI Upgrade

**Feature**: 1-cyberpunk-ui-upgrade
**Created**: 2025-12-19

## Research Tasks & Outcomes

### 1. Tailwind vs Infima Decision

**Task**: Research whether to install Tailwind CSS or extend existing Infima framework for cyberpunk components

**Research Findings**:
- Docusaurus uses Infima as its default CSS framework, which is optimized for content-centric sites
- Installing Tailwind alongside Infima would add bundle size and potential conflicts
- Infima already provides a robust CSS framework that can be extended with custom properties
- The cyberpunk design can be implemented effectively using CSS custom properties and extensions

**Decision**: Use Docusaurus's native Infima CSS framework with custom CSS extensions

**Rationale**:
- More efficient than integrating Tailwind
- Maintains compatibility with existing Docusaurus components
- Reduces bundle size and potential conflicts
- Leverages existing Infima grid and utility classes

**Alternatives considered**:
- Installing Tailwind CSS (would add complexity and bundle size)
- Pure CSS approach without any framework (less maintainable)

### 2. Google Fonts Integration

**Task**: Research how to integrate Orbitron (headers) and JetBrains Mono (code/body) fonts in Docusaurus

**Research Findings**:
- Docusaurus provides multiple ways to load external fonts
- Option 1: Add CDN links in docusaurus.config.ts via head tags
- Option 2: Import in custom CSS file
- Option 3: Use Google Fonts npm package
- The docusaurus.config.ts approach is the most maintainable and performant

**Decision**: Load Google Fonts via docusaurus.config.ts head tags

**Rationale**:
- Docusaurus provides built-in font loading capabilities through the config file
- Better performance with preconnect hints
- Easier to maintain and update
- Proper loading order with other assets

**Implementation approach**:
- Add preconnect links for Google Fonts API
- Add stylesheet link for Orbitron and JetBrains Mono
- Configure font-display: swap for better performance

### 3. Scanline Overlay Implementation

**Task**: Research best approach for implementing scanline texture as pointer-events-none overlay

**Research Findings**:
- Option 1: CSS pseudo-elements (:before/:after) on body/html
- Option 2: React component overlay
- Option 3: CSS background image with repeating pattern
- CSS pseudo-elements are the most performant approach
- They don't add DOM elements and are optimized by browsers
- Using background-image with linear-gradient for scanline pattern

**Decision**: Implement scanline overlay using CSS pseudo-elements

**Rationale**:
- Most performant approach that doesn't require additional DOM elements
- Better memory usage
- Easier to maintain
- Can be easily toggled on/off

**Implementation approach**:
- Use ::before pseudo-element on body element
- Apply pointer-events: none to ensure it doesn't interfere with interactions
- Use CSS linear-gradient for scanline pattern
- Make it full viewport with fixed positioning

### 4. Dark Mode Enforcement

**Task**: Research how to override Docusaurus's colorMode to force dark mode only

**Research Findings**:
- Docusaurus has a colorMode configuration in docusaurus.config.ts
- Option 1: Set defaultMode to 'dark' and disable switch
- Option 2: Override the color mode provider
- Option 3: Use CSS-only approach with media queries
- The configuration approach is the most reliable and Docusaurus-native solution

**Decision**: Override colorMode in docusaurus.config.ts to enforce dark mode only

**Rationale**:
- Docusaurus provides configuration option to disable light mode
- Most reliable approach that works across all Docusaurus components
- Properly handles initial render and theme switching
- Maintains consistency across all pages

**Implementation approach**:
- Set defaultMode to 'dark' in themeConfig.colorMode
- Set disableSwitch to true to prevent user switching
- Set respectPrefersColorScheme to false

## Best Practices & Patterns

### CSS Architecture for Cyberpunk Theme

**Pattern**: Extending Infima with Cyberpunk Variables
- Use CSS custom properties for all cyberpunk-specific values
- Maintain Infima's base structure for compatibility
- Override specific properties for cyberpunk aesthetic

**Benefits**:
- Maintains Docusaurus compatibility
- Easier to update and maintain
- Clear separation between base and custom styles

### Component Architecture

**Pattern**: Cyberpunk Component Family
- Create components in src/components/CyberUI/ directory
- Use TypeScript interfaces for props
- Apply consistent styling patterns across components
- Include accessibility attributes by default

**Benefits**:
- Organized component structure
- Consistent cyberpunk aesthetic
- Easy to maintain and extend
- Accessible by default

### Animation Performance

**Pattern**: Optimized CSS Animations
- Use will-change and transform for performance
- Use requestAnimationFrame for complex animations
- Provide reduced motion alternatives
- Test on lower-end devices

**Benefits**:
- Better performance across devices
- Respects user preferences
- Maintains smooth animations
- Complies with accessibility standards