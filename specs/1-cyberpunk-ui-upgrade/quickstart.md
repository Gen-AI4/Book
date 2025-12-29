# Quickstart Guide: Cyberpunk UI Implementation

**Feature**: 1-cyberpunk-ui-upgrade
**Created**: 2025-12-19

## Overview

This guide provides step-by-step instructions to implement the cyberpunk UI upgrade on the Docusaurus-based Physical AI & Humanoid Robotics textbook website.

## Prerequisites

- Node.js >= 20.0 (as specified in package.json)
- Basic knowledge of React, TypeScript, and CSS
- Understanding of Docusaurus configuration

## Step 1: Set Up Cyberpunk Theme Infrastructure

### 1.1 Add Google Fonts

Update `frontend/docusaurus.config.ts` to include Orbitron and JetBrains Mono fonts:

```typescript
// In the headTags array in docusaurus.config.ts
{
  tagName: 'link',
  attributes: {
    rel: 'preconnect',
    href: 'https://fonts.googleapis.com',
  },
},
{
  tagName: 'link',
  attributes: {
    rel: 'preconnect',
    href: 'https://fonts.gstatic.com',
    crossOrigin: 'anonymous',
  },
},
{
  tagName: 'link',
  attributes: {
    rel: 'stylesheet',
    href: 'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700&display=swap',
  },
},
```

### 1.2 Configure Dark Mode Only

In `frontend/docusaurus.config.ts`, update the themeConfig.colorMode:

```typescript
colorMode: {
  defaultMode: 'dark',
  disableSwitch: true,
  respectPrefersColorScheme: false,
},
```

## Step 2: Update Custom CSS with Cyberpunk Theme

### 2.1 Update `frontend/src/css/custom.css`

Replace the existing color variables with cyberpunk palette:

```css
:root {
  /* Cyberpunk Theme Variables */
  --cyber-black: #000000;
  --cyber-neon-green: #39FF14;
  --cyber-neon-blue: #00FFFF;
  --cyber-neon-purple: #8A2BE2;
  --cyber-red: #FF0000;

  /* Override Infima variables for dark mode */
  --ifm-color-primary: var(--cyber-neon-green);
  --ifm-color-primary-dark: #32e012;
  --ifm-color-primary-darker: #2fda11;
  --ifm-color-primary-darkest: #28b50e;
  --ifm-color-primary-light: #4cff28;
  --ifm-color-primary-lighter: #56ff3c;
  --ifm-color-primary-lightest: #73ff61;

  /* Backgrounds */
  --ifm-background-color: var(--cyber-black);
  --ifm-background-surface-color: #0a0a0a;

  /* Code styling */
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(57, 255, 20, 0.1);

  /* Typography */
  --ifm-font-family-base: 'JetBrains Mono', monospace;
  --ifm-font-family-heading: 'Orbitron', sans-serif;
}

/* Dark mode (now default) */
[data-theme='dark'] {
  --ifm-color-primary: var(--cyber-neon-green);
  --ifm-color-primary-dark: #32e012;
  --ifm-color-primary-darker: #2fda11;
  --ifm-color-primary-darkest: #28b50e;
  --ifm-color-primary-light: #4cff28;
  --ifm-color-primary-lighter: #56ff3c;
  --ifm-color-primary-lightest: #73ff61;

  --ifm-background-color: var(--cyber-black);
  --ifm-background-surface-color: #0a0a0a;
  --docusaurus-highlighted-code-line-bg: rgba(57, 255, 20, 0.1);
}

/* Custom cyberpunk styling */
/* Headers use Orbitron font */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--ifm-font-family-heading);
  text-shadow: 0 0 5px var(--cyber-neon-green), 0 0 10px var(--cyber-neon-green);
}

/* Code blocks with terminal feel */
code {
  background-color: #0a0a0a;
  border: 1px solid var(--cyber-neon-green);
  box-shadow: 0 0 5px rgba(57, 255, 20, 0.5);
  font-family: var(--ifm-font-family-base);
}

/* Glow effect utility class */
.glow {
  box-shadow: 0 0 5px currentColor, 0 0 10px currentColor, 0 0 20px currentColor;
  transition: box-shadow 0.3s ease;
}

.glow:hover {
  box-shadow: 0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor;
}
```

### 2.2 Add Scanline Overlay

Add the following to `frontend/src/css/custom.css` for the scanline effect:

```css
/* Scanline overlay */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background:
    linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0) 50%,
      rgba(0, 255, 0, 0.05) 50%
    );
  background-size: 100% 4px;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.3;
}

/* Glitch animation keyframes */
@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-3px, 3px);
  }
  40% {
    transform: translate(-3px, -3px);
  }
  60% {
    transform: translate(3px, 3px);
  }
  80% {
    transform: translate(3px, -3px);
  }
  100% {
    transform: translate(0);
  }
}

/* Subtle glitch effect */
.glitch {
  position: relative;
  display: inline-block;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch::before {
  left: 2px;
  text-shadow: -1px 0 var(--cyber-neon-red);
  clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim 5s infinite linear alternate-reverse;
}

.glitch::after {
  left: -2px;
  text-shadow: -1px 0 var(--cyber-neon-blue);
  clip: rect(44px, 450px, 56px, 0);
  animation: glitch-anim 5s infinite linear alternate-reverse;
}

@keyframes glitch-anim {
  0% {
    clip: rect(42px, 9999px, 44px, 0);
  }
  10% {
    clip: rect(12px, 9999px, 59px, 0);
  }
  20% {
    clip: rect(48px, 9999px, 29px, 0);
  }
  30% {
    clip: rect(42px, 9999px, 73px, 0);
  }
  40% {
    clip: rect(63px, 9999px, 27px, 0);
  }
  50% {
    clip: rect(34px, 9999px, 55px, 0);
  }
  60% {
    clip: rect(86px, 9999px, 73px, 0);
  }
  70% {
    clip: rect(20px, 9999px, 20px, 0);
  }
  80% {
    clip: rect(26px, 9999px, 60px, 0);
  }
  90% {
    clip: rect(25px, 9999px, 66px, 0);
  }
  100% {
    clip: rect(76px, 9999px, 79px, 0);
  }
}
```

## Step 3: Create Cyberpunk Components

### 3.1 Create CyberButton Component

Create `frontend/src/components/CyberUI/CyberButton.tsx`:

```tsx
import React, { ReactNode } from 'react';
import clsx from 'clsx';

type CyberButtonVariant = 'default' | 'holographic' | 'glitch';
type CyberButtonSize = 'sm' | 'md' | 'lg';

interface CyberButtonProps {
  children: ReactNode;
  variant?: CyberButtonVariant;
  size?: CyberButtonSize;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
  'data-text'?: string; // For glitch effect
}

const CyberButton: React.FC<CyberButtonProps> = ({
  children,
  variant = 'default',
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  'data-text': dataText,
  ...props
}) => {
  const baseClasses = 'font-sans font-bold cursor-pointer transition-all duration-300 border-2 relative overflow-hidden';

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-6 py-2 text-base',
    lg: 'px-8 py-3 text-lg'
  };

  const variantClasses = {
    default: 'border-cyber-neon-green text-cyber-neon-green bg-transparent hover:bg-cyber-neon-green hover:text-cyber-black',
    holographic: 'border-cyber-neon-blue text-cyber-neon-blue bg-transparent hover:bg-cyber-neon-blue/20',
    glitch: 'border-cyber-red text-cyber-red bg-transparent'
  };

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';

  const classes = clsx(
    baseClasses,
    sizeClasses[size],
    variantClasses[variant],
    disabledClasses,
    'glow', // Apply glow effect
    className
  );

  if (variant === 'glitch') {
    return (
      <button
        className={clsx(classes, 'glitch')}
        onClick={onClick}
        disabled={disabled}
        data-text={dataText || (typeof children === 'string' ? children : '')}
        {...props}
      >
        {children}
      </button>
    );
  }

  return (
    <button
      className={classes}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default CyberButton;
```

### 3.2 Create CyberCard Component

Create `frontend/src/components/CyberUI/CyberCard.tsx`:

```tsx
import React, { ReactNode } from 'react';
import clsx from 'clsx';

interface CyberCardProps {
  children: ReactNode;
  className?: string;
  variant?: 'default' | 'glow' | 'terminal';
  'data-text'?: string;
}

const CyberCard: React.FC<CyberCardProps> = ({
  children,
  className = '',
  variant = 'default',
  'data-text': dataText,
  ...props
}) => {
  const baseClasses = 'relative overflow-hidden border-2 transition-all duration-300';

  const variantClasses = {
    default: 'border-cyber-neon-green bg-cyber-black',
    glow: 'border-cyber-neon-blue bg-cyber-black glow',
    terminal: 'border-cyber-neon-green bg-cyber-black font-mono'
  };

  // Apply chamfered corners using clip-path
  const chamferedStyle = {
    clipPath: 'polygon(0 10px, 10px 0, calc(100% - 10px) 0, 100% 10px, 100% calc(100% - 10px), calc(100% - 10px) 100%, 10px 100%, 0 calc(100% - 10px))'
  };

  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    'p-6',
    className
  );

  return (
    <div
      className={classes}
      style={chamferedStyle}
      {...props}
    >
      {children}
    </div>
  );
};

export default CyberCard;
```

### 3.3 Create CyberInput Component

Create `frontend/src/components/CyberUI/CyberInput.tsx`:

```tsx
import React from 'react';
import clsx from 'clsx';

interface CyberInputProps {
  label?: string;
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  type?: string;
  className?: string;
  disabled?: boolean;
}

const CyberInput: React.FC<CyberInputProps> = ({
  label,
  placeholder,
  value,
  onChange,
  type = 'text',
  className = '',
  disabled = false,
  ...props
}) => {
  const baseClasses = 'w-full px-4 py-3 bg-cyber-black border-2 border-cyber-neon-green text-cyber-neon-green font-mono focus:outline-none focus:ring-2 focus:ring-cyber-neon-green glow transition-all duration-300';

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';

  const classes = clsx(
    baseClasses,
    disabledClasses,
    className
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };

  return (
    <div className="flex flex-col space-y-2">
      {label && (
        <label className="text-cyber-neon-green font-mono font-bold">
          {label}
        </label>
      )}
      <div className="relative">
        <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyber-neon-green font-mono">
          &gt;
        </span>
        <input
          type={type}
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          className={clsx(classes, 'pl-8')} // Adjust padding for the > prefix
          disabled={disabled}
          {...props}
        />
      </div>
    </div>
  );
};

export default CyberInput;
```

## Step 4: Apply Cyberpunk Theme to Existing Pages

### 4.1 Update Landing Page

Update `frontend/src/pages/index.tsx` to use cyberpunk components:

```tsx
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import CyberButton from '../components/CyberUI/CyberButton';
import CyberCard from '../components/CyberUI/CyberCard';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title glitch" data-text={siteConfig.title}>
          {siteConfig.title}
        </h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <CyberButton
            variant="glitch"
            size="lg"
            data-text="ENTER SYSTEM"
            onClick={() => window.scrollTo({ top: 600, behavior: 'smooth' })}
          >
            ENTER SYSTEM
          </CyberButton>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div className="bg-cyber-black text-cyber-neon-green">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <CyberCard className="col col--4">
                <h3>Physical AI</h3>
                <p>Explore the intersection of artificial intelligence and embodied systems.</p>
              </CyberCard>
              <CyberCard className="col col--4">
                <h3>Humanoid Robotics</h3>
                <p>Learn about the design and control of human-like robots.</p>
              </CyberCard>
              <CyberCard className="col col--4">
                <h3>Cyberpunk Future</h3>
                <p>Experience the high-tech, low-life aesthetic of tomorrow.</p>
              </CyberCard>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
```

## Step 5: Update Documentation Styling

### 5.1 Update Admonitions

Update `frontend/src/css/custom.css` to style admonitions with cyberpunk theme:

```css
/* Cyberpunk admonitions */
.admonition {
  border-radius: 0; /* No rounded corners */
  border-left: 4px solid var(--cyber-neon-green);
  background-color: rgba(0, 0, 0, 0.7);
  box-shadow: 0 0 10px rgba(57, 255, 20, 0.3);
}

.admonition--note {
  border-left-color: var(--cyber-neon-blue);
}

.admonition--tip {
  border-left-color: var(--cyber-neon-green);
}

.admonition--caution {
  border-left-color: var(--cyber-neon-purple);
}

.admonition--danger {
  border-left-color: var(--cyber-red);
}

.admonition-heading h5 {
  color: var(--cyber-neon-green);
  font-family: var(--ifm-font-family-heading);
  text-shadow: 0 0 5px var(--cyber-neon-green);
}

/* Hardware admonition specific styling */
.admonition-hardware {
  border-left: 4px solid var(--cyber-neon-blue);
  background-color: rgba(0, 20, 30, 0.7);
}

.admonition-hardware .admonition-heading {
  color: var(--cyber-neon-blue);
}
```

## Step 6: Testing and Validation

### 6.1 Accessibility Testing

- Verify color contrast ratios meet WCAG AA standards (4.5:1 for normal text)
- Test with reduced motion settings enabled
- Ensure all interactive elements are keyboard accessible

### 6.2 Performance Testing

- Run Lighthouse audits to ensure scores remain above 90
- Test on lower-end devices to ensure animations perform well
- Verify page load times remain within acceptable limits

### 6.3 Cross-Browser Testing

- Test in Chrome, Firefox, Safari, and Edge
- Verify fallbacks work in browsers that don't support advanced CSS features
- Ensure scanline effect works across different browsers