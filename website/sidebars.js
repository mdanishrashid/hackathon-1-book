// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'introduction',
      ],
    },
    {
      type: 'category',
      label: 'Textbook Chapters',
      items: [
        'chapters/introduction-to-physical-ai',
        'chapters/humanoid-robotics-overview',
        'chapters/embodied-cognition-and-ai',
        'chapters/locomotion-and-movement-control',
        'chapters/perception-systems',
        'chapters/manipulation-and-dexterity',
        'chapters/human-robot-interaction',
        'chapters/ai-learning-in-physical-systems',
        'chapters/applications-and-ethics',
        'chapters/future-of-physical-ai',
        'chapters/building-your-first-physical-ai',
        'chapters/case-studies',
      ],
    },
    {
      type: 'category',
      label: 'Learning Tools',
      items: [
        'user-guide',
        'developer-guide',
      ],
    },
  ],
};

module.exports = sidebars;