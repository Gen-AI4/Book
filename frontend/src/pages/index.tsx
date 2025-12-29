import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Hero from '../components/HomepageFeatures/Hero';
import CyberCard from '../components/CyberUI/CyberCard';

import styles from './index.module.css';

function HomepageModules() {
  return (
    <section className={clsx(styles.modules, 'bg-cyber-black py-16')}>
      <div className="container padding-horiz--md">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider">
            Core Modules
          </h2>
          <p className="text-cyber-neon-green font-jetbrains-mono mt-2">
            Explore the foundations of Physical AI & Humanoid Robotics
          </p>
        </div>
        <div className="row">
          <div className="col col--4">
            <CyberCard variant="default">
              <div className="text--center">
                <h3 className="text-xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider mb-3">
                  ROS 2 Foundations
                </h3>
                <p className="text-cyber-neon-green font-jetbrains-mono">
                  The nervous system of robotic applications - communication, control, and coordination
                </p>
              </div>
            </CyberCard>
          </div>
          <div className="col col--4">
            <CyberCard variant="default">
              <div className="text--center">
                <h3 className="text-xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider mb-3">
                  Digital Twin
                </h3>
                <p className="text-cyber-neon-green font-jetbrains-mono">
                  Gazebo & Unity simulation environments for safe testing and development
                </p>
              </div>
            </CyberCard>
          </div>
          <div className="col col--4">
            <CyberCard variant="default">
              <div className="text--center">
                <h3 className="text-xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider mb-3">
                  NVIDIA Isaac
                </h3>
                <p className="text-cyber-neon-green font-jetbrains-mono">
                  AI-powered robotics framework for perception, planning, and control
                </p>
              </div>
            </CyberCard>
          </div>
        </div>
        <div className="row padding-top--md">
          <div className="col col--4 col--offset-2">
            <CyberCard variant="default">
              <div className="text--center">
                <h3 className="text-xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider mb-3">
                  Vision-Language-Action
                </h3>
                <p className="text-cyber-neon-green font-jetbrains-mono">
                  Foundation models that connect perception, language, and robotic action
                </p>
              </div>
            </CyberCard>
          </div>
          <div className="col col--4">
            <CyberCard variant="default">
              <div className="text--center">
                <h3 className="text-xl font-orbitron font-bold text-cyber-neon-green uppercase tracking-wider mb-3">
                  Hardware Integration
                </h3>
                <p className="text-cyber-neon-green font-jetbrains-mono">
                  From simulation to real-world deployment on humanoid platforms
                </p>
              </div>
            </CyberCard>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="A comprehensive textbook on building intelligent humanoid robots that bridge the gap between artificial intelligence and physical reality">
      <Hero />
      <main>
      </main>
    </Layout>
  );
}
