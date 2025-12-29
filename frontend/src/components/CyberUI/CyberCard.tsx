import React, { ReactNode } from 'react';
import clsx from 'clsx';

type CyberCardVariant = 'default' | 'terminal' | 'holographic';

interface CyberCardProps {
  children: ReactNode;
  className?: string;
  variant?: CyberCardVariant;
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
    default: 'border-cyber-neon-green bg-cyber-black text-cyber-neon-green',
    terminal: 'border-cyber-neon-blue bg-cyber-black text-cyber-neon-blue font-jetbrains-mono',
    holographic: 'border-cyber-neon-purple bg-cyber-black/80 text-cyber-neon-purple backdrop-filter backdrop-blur-sm'
  };

  // Apply chamfered corners using clip-path
  const chamferedStyle = {
    clipPath: 'polygon(0 10px, 10px 0, calc(100% - 10px) 0, 100% 10px, 100% calc(100% - 10px), calc(100% - 10px) 100%, 10px 100%, 0 calc(100% - 10px))'
  };

  const classes = clsx(
    baseClasses,
    variantClasses[variant],
    'p-6',
    'glow', // Apply glow effect
    className
  );

  return (
    <div
      className={classes}
      style={chamferedStyle}
      {...props}
    >
      {variant === 'terminal' && (
        <div className="flex items-center mb-3">
          <div className="flex space-x-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div className="ml-2 text-xs text-cyber-neon-blue font-jetbrains-mono">
            TERMINAL
          </div>
        </div>
      )}
      {children}
    </div>
  );
};

export default CyberCard;