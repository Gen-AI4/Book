import React from 'react';
import Link from '@docusaurus/Link';
import clsx from 'clsx';
import CyberButton from '../CyberUI/CyberButton';
import CyberCard from '../CyberUI/CyberCard';

const Hero = () => {
  return (
    <div className="bg-cyber-black text-cyber-neon-green py-20">
      <div className="container mx-auto px-4 text-center">
        <h1
          className="text-5xl md:text-7xl font-orbitron font-bold mb-6 glitch-contained"
          data-text="PHYSICAL AI & HUMANOID ROBOTICS"
        >
          <span className="glitch" data-text="PHYSICAL AI & HUMANOID ROBOTICS">
            PHYSICAL AI & HUMANOID ROBOTICS
          </span>
        </h1>
        <p className="text-xl md:text-2xl font-jetbrains-mono mb-10 max-w-3xl mx-auto">
          A comprehensive textbook on building intelligent humanoid robots that bridge the gap between artificial intelligence and physical reality
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <CyberButton
            variant="default"
            size="lg"
            onClick={() => window.scrollTo({ top: 600, behavior: 'smooth' })}
          >
            ENTER SYSTEM
          </CyberButton>
          <CyberButton
            variant="outline"
            size="lg"
            href="/docs/intro/foundations"
          >
            ACCESS TEXTBOOK
          </CyberButton>
        </div>
      </div>
    </div>
  );
};

export default Hero;