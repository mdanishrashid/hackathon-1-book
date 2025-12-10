// API Client for interacting with the backend API
// Provides methods to interact with chapters, steps, and progress endpoints

class ApiClient {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  // Generic method to make API requests
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${url}:`, error);
      throw error;
    }
  }

  // Chapters API methods
  async getChapters() {
    return this.request('/v1/chapters');
  }

  async getChapter(chapterId) {
    return this.request(`/v1/chapters/${chapterId}`);
  }

  // Steps API methods
  async getStepsByChapter(chapterId) {
    return this.request(`/v1/steps/chapter/${chapterId}`);
  }

  async getStep(stepId) {
    return this.request(`/v1/steps/${stepId}`);
  }

  async getPrevStep(stepId) {
    // This would require backend implementation to get previous step
    // For now, we'll return null
    return null;
  }

  async getNextStep(stepId) {
    // This would require backend implementation to get next step
    // For now, we'll return null
    return null;
  }

  // Progress API methods
  async getProgress() {
    return this.request('/v1/progress');
  }

  async getProgressForChapter(chapterId) {
    // User context is determined server-side from auth token
    return this.request(`/v1/progress/chapters/${chapterId}`);
  }

  async getProgressForStep(stepId) {
    // User context is determined server-side from auth token
    return this.request(`/v1/progress/steps/${stepId}`);
  }

  async markStepComplete(stepId, validationData = null) {
    return this.request(`/v1/progress/steps/${stepId}/complete`, {
      method: 'POST',
      body: validationData ? JSON.stringify(validationData) : undefined,
    });
  }

  async resetStepProgress(stepId) {
    return this.request(`/v1/progress/steps/${stepId}/reset`, {
      method: 'PUT',
    });
  }

  // Authentication header can be added if needed
  setAuthHeader(token) {
    this.authToken = token;
  }
}

// Create a singleton instance
const apiClient = new ApiClient();

export default apiClient;