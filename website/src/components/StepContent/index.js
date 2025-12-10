import React, { useState, useEffect } from 'react';
import StepProgress from '../StepProgress';

// Mock API client for demonstration
const apiClient = {
  getStepContent: async (stepId) => {
    // In real implementation, this would call the backend API
    // to fetch the actual content for the step
    return {
      id: stepId,
      title: "Understanding AI Concepts",
      content: `# Understanding AI Concepts

## Introduction

Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving.

## Key Concepts

- **Machine Learning**: A subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.
- **Neural Networks**: Computing systems vaguely inspired by the biological neural networks that constitute animal brains.
- **Deep Learning**: Part of a broader family of machine learning methods based on artificial neural networks.

## Practical Example

Let's look at a simple implementation of a neural network concept:
\`\`\`python
# Simple example of neural network layer
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Sample input
input_data = np.array([0.5, 0.8, -0.2])
weights = np.array([0.4, -0.3, 0.9])
bias = 0.1

# Calculate output
output = sigmoid(np.dot(input_data, weights) + bias)
print(f"Neural network output: {output}")
\`\`\`

## Summary

This step introduced the fundamental concepts of AI, including machine learning, neural networks, and deep learning. Understanding these concepts is crucial for developing AI applications.`,
      step_type: "reading", // reading, quiz, exercise, video, interactive
      required_completion_criteria: {
        type: "time",
        value: 60 // seconds
      }
    };
  }
};

const StepContent = ({ stepId, chapterId }) => {
  const [stepData, setStepData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStepContent = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getStepContent(stepId);
        setStepData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (stepId) {
      fetchStepContent();
    }
  }, [stepId]);

  if (loading) {
    return <div>Loading step content...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="step-content-container">
      <article className="step-content">
        <header className="step-header">
          <h1>{stepData?.title || "Step Title"}</h1>
        </header>

        <section className="step-body">
          <div
            className="markdown-content"
            dangerouslySetInnerHTML={{ __html: convertMarkdownToHtml(stepData?.content || "") }}
          />
        </section>
      </article>

      <aside className="step-sidebar">
        <StepProgress stepId={stepId} chapterId={chapterId} />
      </aside>
    </div>
  );
};

// For demonstration purposes, we'll use a simple markdown-to-HTML conversion function
// In a real implementation, you'd use the marked library or Docusaurus's MDX capabilities
const convertMarkdownToHtml = (text) => {
  // Simple markdown to HTML conversion for demonstration
  let html = text;

  // Headers
  html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');
  html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
  html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');

  // Bold and italic
  html = html.replace(/\*\*(.*)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*)\*/g, '<em>$1</em>');

  // Code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

  // Inline code
  html = html.replace(/`(.*?)`/g, '<code>$1</code>');

  // Line breaks
  html = html.replace(/\n\n/g, '<br/><br/>');

  return html;
};

export default StepContent;