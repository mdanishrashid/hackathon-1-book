import React, { useState, useEffect } from 'react';
import './Profile.css';

const Profile = () => {
  const [profile, setProfile] = useState({
    background_level: 'beginner',
    preferred_language: 'en',
    learning_preferences: '{}'
  });
  
  const [isEditing, setIsEditing] = useState(false);
  const [tempProfile, setTempProfile] = useState({...profile});

  useEffect(() => {
    // In a real app, this would fetch from the backend
    // fetchUserProfile();
  }, []);

  const handleEdit = () => {
    setTempProfile({...profile});
    setIsEditing(true);
  };

  const handleSave = () => {
    setProfile({...tempProfile});
    setIsEditing(false);
    // In a real app, this would save to the backend
    // saveUserProfile(tempProfile);
  };

  const handleCancel = () => {
    setTempProfile({...profile});
    setIsEditing(false);
  };

  const handleInputChange = (field, value) => {
    setTempProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="profile-container">
      <h1>User Profile</h1>
      
      <div className="profile-card">
        <div className="profile-header">
          <h2>Learning Profile</h2>
          {!isEditing && (
            <button className="edit-button" onClick={handleEdit}>
              Edit Profile
            </button>
          )}
        </div>
        
        {isEditing ? (
          <div className="profile-form">
            <div className="form-group">
              <label htmlFor="background_level">Background Level:</label>
              <select
                id="background_level"
                value={tempProfile.background_level}
                onChange={(e) => handleInputChange('background_level', e.target.value)}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="preferred_language">Preferred Language:</label>
              <select
                id="preferred_language"
                value={tempProfile.preferred_language}
                onChange={(e) => handleInputChange('preferred_language', e.target.value)}
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="learning_preferences">Learning Preferences (JSON):</label>
              <textarea
                id="learning_preferences"
                value={tempProfile.learning_preferences}
                onChange={(e) => handleInputChange('learning_preferences', e.target.value)}
                rows="4"
              />
            </div>
            
            <div className="form-actions">
              <button className="save-button" onClick={handleSave}>
                Save Changes
              </button>
              <button className="cancel-button" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="profile-display">
            <div className="profile-field">
              <strong>Background Level:</strong> {profile.background_level}
            </div>
            <div className="profile-field">
              <strong>Preferred Language:</strong> {profile.preferred_language}
            </div>
            <div className="profile-field">
              <strong>Learning Preferences:</strong> {profile.learning_preferences}
            </div>
          </div>
        )}
      </div>
      
      <div className="profile-card">
        <h2>Learning Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>24</h3>
            <p>Steps Completed</p>
          </div>
          <div className="stat-card">
            <h3>8</h3>
            <p>Chapters Completed</p>
          </div>
          <div className="stat-card">
            <h3>12h</h3>
            <p>Time Spent</p>
          </div>
          <div className="stat-card">
            <h3>92%</h3>
            <p>Completion Rate</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;