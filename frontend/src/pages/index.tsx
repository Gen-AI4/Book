import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import ChatWidget from '../components/ChatWidget';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Physical AI & Humanoid Robotics
        </Heading>
        <p className="hero__subtitle">A comprehensive textbook on building intelligent humanoid robots that bridge the gap between artificial intelligence and physical reality</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro/foundations">
            Start Learning - 6 Modules ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageModules() {
  return (
    <section className={styles.modules}>
      <div className="container padding-horiz--md">
        <div className="row">
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>ROS 2 Foundations</h3>
              <p>The nervous system of robotic applications - communication, control, and coordination</p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>Digital Twin</h3>
              <p>Gazebo & Unity simulation environments for safe testing and development</p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>NVIDIA Isaac</h3>
              <p>AI-powered robotics framework for perception, planning, and control</p>
            </div>
          </div>
        </div>
        <div className="row padding-top--md">
          <div className="col col--4 col--offset-2">
            <div className="text--center padding-horiz--md">
              <h3>Vision-Language-Action</h3>
              <p>Foundation models that connect perception, language, and robotic action</p>
            </div>
          </div>
          <div className="col col--4">
            <div className="text--center padding-horiz--md">
              <h3>Hardware Integration</h3>
              <p>From simulation to real-world deployment on humanoid platforms</p>
            </div>
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
      <HomepageHeader />
      <main>
        <HomepageModules />
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
          <h2>Chat with the AI Assistant</h2>
          <ChatWidget />
        </div>
      </main>
    </Layout>
  );
}
