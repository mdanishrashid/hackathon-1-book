// Navigation control utility for step-by-step progression
// Ensures users follow the correct sequence and can't skip steps

class StepNavigationControl {
  constructor(apiClient) {
    this.apiClient = apiClient;
  }

  // Check if a user can navigate to a specific step
  async canNavigateToStep(userId, stepId) {
    // In a real implementation, this would call the backend to check
    // if the current step's prerequisites have been completed
    // userId is passed as null since it's determined server-side from auth token
    try {
      const step = await this.apiClient.getStep(stepId);
      const progress = await this.apiClient.getProgressForStep(stepId);

      // If the step has a prerequisite, check if it's completed
      if (step.prerequisite_step_id) {
        const prereqProgress = await this.apiClient.getProgressForStep(
          step.prerequisite_step_id
        );
        return prereqProgress && prereqProgress.status === 'completed';
      }

      // If it's the first step in the chapter, user can access it
      if (step.order_index === 1) {
        return true;
      }

      // For steps 2+, check if the previous step is completed
      const prevStep = await this.apiClient.getPrevStep(stepId);
      if (prevStep) {
        const prevProgress = await this.apiClient.getProgressForStep(
          prevStep.id
        );
        return prevProgress && prevProgress.status === 'completed';
      }

      // Default: allow access if no specific constraints
      return true;
    } catch (error) {
      console.error("Error checking navigation permission:", error);
      return false;
    }
  }

  // Get the first incomplete step in a chapter for the user
  async getFirstIncompleteStep(userId, chapterId) {
    // userId is passed as null since it's determined server-side from auth token
    try {
      const steps = await this.apiClient.getStepsByChapter(chapterId);
      const progress = await this.apiClient.getProgressForChapter(chapterId);

      // Create a map of stepId to progress for quick lookup
      const progressMap = {};
      progress.forEach(p => {
        progressMap[p.step_id] = p;
      });

      // Find the first step that isn't completed
      for (const step of steps) {
        const stepProgress = progressMap[step.id];
        if (!stepProgress || stepProgress.status !== 'completed') {
          return step;
        }
      }

      // If all steps are completed, return null
      return null;
    } catch (error) {
      console.error("Error getting first incomplete step:", error);
      return null;
    }
  }

  // Get next step after completing the current step
  async getNextStep(userId, currentStepId) {
    // userId is passed as null since it's determined server-side from auth token
    try {
      // First verify that the current step is marked as completed
      const currentProgress = await this.apiClient.getProgressForStep(
        currentStepId
      );

      if (currentProgress?.status !== 'completed') {
        throw new Error('Current step must be completed before proceeding');
      }

      return await this.apiClient.getNextStep(currentStepId);
    } catch (error) {
      console.error("Error getting next step:", error);
      throw error;
    }
  }

  // Validate if a step can be marked as complete based on requirements
  async validateStepCompletion(stepId, validationData) {
    try {
      const step = await this.apiClient.getStep(stepId);
      const requiredCriteria = JSON.parse(step.required_completion_criteria || '{}');

      // Check time-based requirements
      if (requiredCriteria.type === 'time' && requiredCriteria.value) {
        const timeSpent = validationData.timeSpent || 0;
        if (timeSpent < requiredCriteria.value) {
          throw new Error(`Insufficient time spent. Required: ${requiredCriteria.value}s, Actual: ${timeSpent}s`);
        }
      }

      // Additional validation can be added here
      // For example: quiz scores, exercise completion, etc.

      return true;
    } catch (error) {
      console.error("Step completion validation failed:", error);
      throw error;
    }
  }
}

// Example usage:
/*
const navControl = new StepNavigationControl(apiClient);

// Check if user can navigate to a step
const canNavigate = await navControl.canNavigateToStep(userId, stepId);

// Get first incomplete step to resume from
const nextStep = await navControl.getFirstIncompleteStep(userId, chapterId);

// Validate completion of current step
await navControl.validateStepCompletion(currentStepId, { timeSpent: 120 });
*/

export default StepNavigationControl;