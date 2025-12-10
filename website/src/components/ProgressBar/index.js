import React from 'react';
import './ProgressBar.css';

const ProgressBar = ({ 
  completedSteps = 0, 
  totalSteps = 0, 
  percentage = 0, 
  showLabels = true,
  height = '8px',
  color = '#4CAF50',
  backgroundColor = '#e0e0e0'
}) => {
  const calculatedPercentage = totalSteps > 0 ? (completedSteps / totalSteps) * 100 : 0;

  return (
    <div className="progress-container">
      {showLabels && (
        <div className="progress-labels">
          <span className="label-left">Step {completedSteps} of {totalSteps}</span>
          <span className="label-right">{Math.round(percentage || calculatedPercentage)}%</span>
        </div>
      )}
      <div 
        className="progress-bar-background"
        style={{ 
          height: height,
          backgroundColor: backgroundColor,
          borderRadius: height,
          overflow: 'hidden'
        }}
      >
        <div 
          className="progress-bar-fill"
          style={{ 
            width: `${percentage || calculatedPercentage}%`,
            height: '100%',
            backgroundColor: color,
            transition: 'width 0.3s ease-in-out',
            borderRadius: height
          }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;