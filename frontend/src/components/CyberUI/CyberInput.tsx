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
  const baseClasses = 'w-full px-4 py-3 bg-cyber-black border-2 border-cyber-neon-green text-cyber-neon-green font-jetbrains-mono focus:outline-none focus:ring-2 focus:ring-cyber-neon-green glow transition-all duration-300';

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
        <label className="text-cyber-neon-green font-jetbrains-mono font-bold uppercase tracking-wider">
          {label}
        </label>
      )}
      <div className="relative">
        <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyber-neon-green font-jetbrains-mono text-lg">
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