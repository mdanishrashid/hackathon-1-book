import React, { useState, useEffect } from 'react';
import './LearningPathSelector.css';

const LearningPathSelector = ({ onPathSelect, currentPath }) => {
  const [availablePaths, setAvailablePaths] = useState([
    {
      id: 'default',
      name: 'Default Path',
      description: 'Standard learning path for all users',
      type: 'default',
      stepsCount: 10
    },
    {
      id: 'beginner',
      name: 'Beginner-Friendly Path',
      description: 'Simplified steps with more examples and explanations',
      type: 'personalized',
      stepsCount: 12
    },
    {
      id: 'advanced',
      name: 'Accelerated Path',
      description: 'Fast-paced path for experienced users',
      type: 'personalized',
      stepsCount: 8
    }
  ]);
  
  const [selectedPath, setSelectedPath] = useState(currentPath || 'default');

  useEffect(() => {
    // In a real app, this would fetch from the backend
    // fetchLearningPaths();
  }, []);

  const handlePathChange = (pathId) => {
    const path = availablePaths.find(p => p.id === pathId);
    setSelectedPath(pathId);
    if (onPathSelect) {
      onPathSelect(path);
    }
  };

  return (
    <div className="learning-path-selector">
      <h3>Select Your Learning Path</h3>
      <div className="path-options">
        {availablePaths.map((path) => (
          <div
            key={path.id}
            className={`path-option ${selectedPath === path.id ? 'selected' : ''}`}
            onClick={() => handlePathChange(path.id)}
          >
            <div className="path-header">
              <h4>{path.name}</h4>
              <span className={`path-type ${path.type}`}>{path.type}</span>
            </div>
            <p className="path-description">{path.description}</p>
            <div className="path-stats">
              <span>{path.stepsCount} steps</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningPathSelector;