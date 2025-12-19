import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar structure for the textbook
  textbookSidebar: [
    {
      type: 'category',
      label: '01 - Foundations',
      items: [
        'intro/foundations',
        'intro/embodied-intelligence',
        'intro/hardware-lab',
        'intro/course-roadmap'
      ],
    },
    {
      type: 'category',
      label: '02 - The Nervous System (ROS 2)',
      items: [
        'module-1-ros2/ros2-architecture',
        'module-1-ros2/python-agents',
        'module-1-ros2/urdf-modeling',
        'module-1-ros2/launch-systems'
      ],
    },
    {
      type: 'category',
      label: '03 - Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/gazebo-physics',
        'module-2-digital-twin/unity-rendering',
        'module-2-digital-twin/sensor-sim',
        'module-2-digital-twin/urdf-to-sim'
      ],
    },
    {
      type: 'category',
      label: '04 - NVIDIA Isaac Brain',
      items: [
        'module-3-isaac/isaac-sim-setup',
        'module-3-isaac/isaac-ros-bridge',
        'module-3-isaac/visual-slam',
        'module-3-isaac/nav2-planning'
      ],
    },
    {
      type: 'category',
      label: '05 - Vision-Language-Action Models',
      items: [
        'module-4-vla/voice-interface',
        'module-4-vla/llm-planner',
        'module-4-vla/vla-models',
        'module-4-vla/action-decoding'
      ],
    },
    {
      type: 'category',
      label: '06 - Capstone Project',
      items: [
        'capstone/project-specs',
        'capstone/design-doc',
        'capstone/integration',
        'capstone/final-demo'
      ],
    },
  ],
};

export default sidebars;
