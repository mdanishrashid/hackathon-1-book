
import React, { useState, useEffect } from 'react';
import ProgressBar from '../../components/ProgressBar';
import './Dashboard.css';

const Dashboard = () => {
  const [overallProgress, setOverallProgress] = useState({
    overall_completion_percentage: 0,
    total_steps: 0,
    completed_steps: 0,
    in_progress_steps: 0,
    not_started_steps: 0,
    chapters: []
  });

  // In a real app, this would be fetched from the backend
  useEffect(() => {
    // Mock API call to backend
    const fetchProgress = async () => {
      try {
        // This would actually be an API call to get user's overall progress
        // For now, using mock data
        const mockData = {
          overall_completion_percentage: 35.5,
          total_steps: 40,
          completed_steps: 14,
          in_progress_steps: 5,
          not_started_steps: 21,
          chapters: [
            {
              chapter_id: 'ch1',
              chapter_title: 'Introduction to AI',
              total_steps: 10,
              completed_steps: 8,
              in_progress_steps: 1,
              completion_percentage: 90
            },
            {
              chapter_id: 'ch2',
              chapter_title: 'Machine Learning Fundamentals',
              total_steps: 15,
              completed_steps: 6,
              in_progress_steps: 2,
              completion_percentage: 53.33
            },
            {
              chapter_id: 'ch3',
              chapter_title: 'Deep Learning Concepts',
              total_steps: 10,
              completed_steps: 0,
              in_progress_steps: 2,
              completion_percentage: 20
            },
            {
              chapter_id: 'ch4',
              chapter_title: 'Neural Networks',
              total_steps: 5,
              completed_steps: 0,
              in_progress_steps: 0,
              completion_percentage: 0
            }
          ]
        };
        setOverallProgress(mockData);
      } catch (error) {
        console.error('Error fetching progress:', error);
      }
    };

    fetchProgress();
  }, []);

  return (
    <div className="dashboard-container">
      <h1>Learning Dashboard</h1>
      
      <div className="overview-section">
        <h2>Overall Progress</h2>
        <div className="progress-summary">
          <ProgressBar 
            completedSteps={overallProgress.completed_steps}
            totalSteps={overallProgress.total_steps}
            percentage={overallProgress.overall_completion_percentage}
          />
          <div className="progress-stats">
            <div className="stat-card">
              <h3>{overallProgress.completed_steps}</h3>
              <p>Completed</p>
            </div>
            <div className="stat-card">
              <h3>{overallProgress.in_progress_steps}</h3>
              <p>In Progress</p>
            </div>
            <div className="stat-card">
              <h3>{overallProgress.not_started_steps}</h3>
              <p>Not Started</p>
            </div>
            <div className="stat-card">
              <h3>{overallProgress.total_steps}</h3>
              <p>Total Steps</p>
            </div>
          </div>
        </div>
      </div>

      <div className="chapters-section">
        <h2>Chapter Progress</h2>
        <div className="chapters-list">
          {overallProgress.chapters.map((chapter) => (
            <div key={chapter.chapter_id} className="chapter-card">
              <div className="chapter-header">
                <h3>{chapter.chapter_title}</h3>
                <span className="completion-percent">{chapter.completion_percentage}%</span>
              </div>
              <ProgressBar 
                completedSteps={chapter.completed_steps}
                totalSteps={chapter.total_steps}
                percentage={chapter.completion_percentage}
                height="10px"
                showLabels={false}
              />
              <div className="chapter-stats">
                <span>{chapter.completed_steps}/{chapter.total_steps} steps completed</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;