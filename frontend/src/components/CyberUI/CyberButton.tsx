import React, { ReactNode } from 'react';
import clsx from 'clsx';

type CyberButtonVariant = 'default' | 'outline' | 'ghost';
type CyberButtonSize = 'sm' | 'md' | 'lg';

interface CyberButtonProps {
  children: ReactNode;
  variant?: CyberButtonVariant;
  size?: CyberButtonSize;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
  'data-text'?: string; // For glitch effect
  href?: string; // For link functionality
  target?: string;
  rel?: string;
}

const CyberButton: React.FC<CyberButtonProps> = ({
  children,
  variant = 'default',
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  'data-text': dataText,
  href,
  target,
  rel,
  ...props
}) => {
  const baseClasses = 'font-orbitron font-bold cursor-pointer transition-all duration-300 border-2 relative overflow-hidden uppercase tracking-wider';

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-6 py-2 text-base',
    lg: 'px-8 py-3 text-lg'
  };

  const variantClasses = {
    default: 'border-cyber-neon-green text-cyber-neon-green bg-transparent hover:bg-cyber-neon-green hover:text-cyber-black',
    outline: 'border-cyber-neon-green text-cyber-neon-green bg-transparent hover:glow-neon',
    ghost: 'border-transparent text-cyber-neon-green bg-transparent hover:bg-cyber-neon-green/20'
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

  // If href is provided, render as anchor tag, otherwise as button
  if (href) {
    return (
      <a
        href={href}
        className={classes}
        onClick={onClick}
        target={target}
        rel={rel}
        {...props}
      >
        {children}
      </a>
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