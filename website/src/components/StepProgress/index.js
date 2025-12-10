import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from '@docusaurus/router';
import { useUserData } from '@docusaurus/theme-common';
import ProgressBar from '../ProgressBar';
import apiClient from '../../services/api-client';
import StepNavigationControl from '../../services/navigation-control';

const StepProgress = ({ stepId, chapterId }) => {
  const [progress, setProgress] = useState(null);
  const [chapterSteps, setChapterSteps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [canGoNext, setCanGoNext] = useState(false);

  // Initialize navigation control with the API client
  const navControl = new StepNavigationControl(apiClient);

  useEffect(() => {
    const fetchProgressData = async () => {
      try {
        setLoading(true);

        // Get all steps in the chapter to show progress
        const stepsData = await apiClient.getStepsByChapter(chapterId);

        // Get user's progress for the current step
        // In a real implementation, the user context comes from the auth token in headers
        const progressData = await apiClient.getProgressForStep(null, stepId);

        setProgress(progressData);
        setChapterSteps(stepsData);

        // Check if user can proceed to next step
        // In a real implementation, the user context comes from the auth token in headers
        const canNavigate = await navControl.canNavigateToStep(null, stepId);
        setCanGoNext(canNavigate && progressData.status === "completed");

      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (stepId && chapterId) {
      fetchProgressData();
    }
  }, [stepId, chapterId]);

  const markStepComplete = async () => {
    try {
      // Validate step completion before marking as complete
      await navControl.validateStepCompletion(stepId, { timeSpent: 120 }); // Example validation data

      const updatedProgress = await apiClient.markStepComplete(stepId);
      setProgress(updatedProgress);

      // Check if user can now navigate to next step
      const canNavigate = await navControl.canNavigateToStep(null, stepId);
      setCanGoNext(canNavigate && updatedProgress.status === "completed");
    } catch (err) {
      setError(err.message);
    }
  };

  const navigate = useNavigate();

  const handleNextStep = async () => {
    if (canGoNext) {
      try {
        // Get the next step after completing the current one
        // In a real implementation, the user context comes from the auth token in headers
        const nextStep = await navControl.getNextStep(null, stepId);
        if (nextStep) {
          // Navigate to the next step
          navigate(`/chapters/${chapterId}/steps/${nextStep.id}`);
        } else {
          alert("No next step available or you haven't completed the current step.");
        }
      } catch (error) {
        setError(error.message);
      }
    }
  };

  if (loading) {
    return <div>Loading progress...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  const currentStep = chapterSteps.find(step => step.id === stepId);
  const completedSteps = chapterSteps.filter(step => step.status === "completed").length;
  const totalSteps = chapterSteps.length;
  const chapterProgress = Math.round((completedSteps / totalSteps) * 100);

  return (
    <div className="step-progress-container">
      <div className="step-navigation">
        <div className="chapter-progress">
          <h4>Chapter Progress</h4>
          <ProgressBar
            completedSteps={completedSteps}
            totalSteps={totalSteps}
            percentage={chapterProgress}
            height="12px"
          />
          <div className="step-list">
            {chapterSteps.map(step => (
              <div
                key={step.id}
                className={`step-item ${step.id === stepId ? 'current' : ''} ${step.status}`}
                onClick={() => {
                  // Check if user can navigate to this step
                  navControl.canNavigateToStep(null, step.id)
                    .then(canNavigate => {
                      if (canNavigate) {
                        navigate(`/chapters/${chapterId}/steps/${step.id}`);
                      } else {
                        alert("You must complete previous steps first!");
                      }
                    });
                }}
              >
                <span className="step-number">{step.order_index}</span>
                <span className="step-title">{step.title}</span>
                <span className="step-status">
                  {step.status === 'completed' ? '✓' :
                   step.status === 'in_progress' ? '→' : '○'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="current-step-info">
        <h3>{currentStep?.title || "Current Step"}</h3>
        <div className="step-progress">
          <ProgressBar
            completedSteps={progress?.completion_percentage ? 1 : 0}
            totalSteps={100}
            percentage={progress?.completion_percentage || 0}
            height="10px"
          />
        </div>

        <div className="step-actions">
          {progress?.status !== "completed" ? (
            <button
              className="button button--primary"
              onClick={markStepComplete}
            >
              Mark as Complete
            </button>
          ) : (
            <p>✓ Step completed</p>
          )}

          <button
            className={`button ${canGoNext ? "button--primary" : "button--secondary"}`}
            onClick={handleNextStep}
            disabled={!canGoNext}
          >
            Next Step →
          </button>
        </div>
      </div>
    </div>
  );
};

export default StepProgress;