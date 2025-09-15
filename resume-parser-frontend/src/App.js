import React, { useState } from 'react';
import { Upload, FileText, Briefcase, User, Mail, MapPin, Clock, CheckCircle, AlertCircle, Loader } from 'lucide-react';

const ResumeParserApp = () => {
  const [activeTab, setActiveTab] = useState('resume');
  const [resumeFile, setResumeFile] = useState(null);
  const [parsedResume, setParsedResume] = useState(null);
  const [email, setEmail] = useState('');
  const [jobDescription, setJobDescription] = useState({
    job_title: '',
    company: '',
    location: '',
    job_type: '',
    description: '',
    required_skills: []
  });
  const [skillInput, setSkillInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const API_BASE = 'http://localhost:8000';

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%)',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    },
    innerContainer: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '32px 16px'
    },
    header: {
      textAlign: 'center',
      marginBottom: '32px'
    },
    headerTitle: {
      fontSize: '2.5rem',
      fontWeight: 'bold',
      color: '#1f2937',
      marginBottom: '8px'
    },
    headerSubtitle: {
      color: '#6b7280',
      fontSize: '1.1rem'
    },
    message: {
      marginBottom: '24px',
      padding: '16px',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      border: '1px solid'
    },
    messageSuccess: {
      backgroundColor: '#f0fdf4',
      color: '#15803d',
      borderColor: '#bbf7d0'
    },
    messageError: {
      backgroundColor: '#fef2f2',
      color: '#dc2626',
      borderColor: '#fecaca'
    },
    tabContainer: {
      marginBottom: '32px',
      display: 'flex',
      justifyContent: 'center'
    },
    tabNav: {
      display: 'flex',
      backgroundColor: 'white',
      borderRadius: '8px',
      padding: '4px',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      maxWidth: '400px'
    },
    tabButton: {
      flex: 1,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px',
      padding: '12px 16px',
      borderRadius: '6px',
      transition: 'all 0.2s',
      border: 'none',
      cursor: 'pointer',
      fontSize: '1rem',
      fontWeight: '500'
    },
    tabButtonActive: {
      backgroundColor: '#3b82f6',
      color: 'white',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
    },
    tabButtonInactive: {
      color: '#6b7280',
      backgroundColor: 'transparent'
    },
    card: {
      backgroundColor: 'white',
      borderRadius: '12px',
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
      padding: '24px',
      marginBottom: '24px'
    },
    cardTitle: {
      fontSize: '1.5rem',
      fontWeight: '600',
      color: '#1f2937',
      marginBottom: '16px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    },
    uploadArea: {
      border: '2px dashed #d1d5db',
      borderRadius: '8px',
      padding: '32px',
      textAlign: 'center',
      transition: 'border-color 0.2s',
      cursor: 'pointer'
    },
    uploadAreaHover: {
      borderColor: '#60a5fa'
    },
    hiddenInput: {
      display: 'none'
    },
    uploadContent: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    },
    uploadText: {
      color: '#6b7280',
      marginBottom: '8px'
    },
    uploadSubtext: {
      fontSize: '0.875rem',
      color: '#9ca3af'
    },
    fileInfo: {
      marginTop: '16px',
      padding: '12px',
      backgroundColor: '#eff6ff',
      borderRadius: '8px'
    },
    fileInfoTitle: {
      color: '#1d4ed8',
      fontWeight: '500'
    },
    fileInfoSize: {
      fontSize: '0.875rem',
      color: '#3730a3'
    },
    button: {
      width: '100%',
      marginTop: '24px',
      padding: '12px 24px',
      borderRadius: '8px',
      transition: 'all 0.2s',
      border: 'none',
      cursor: 'pointer',
      fontSize: '1rem',
      fontWeight: '600',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px'
    },
    buttonPrimary: {
      backgroundColor: '#3b82f6',
      color: 'white'
    },
    buttonPrimaryHover: {
      backgroundColor: '#2563eb'
    },
    buttonSuccess: {
      backgroundColor: '#10b981',
      color: 'white'
    },
    buttonSuccessHover: {
      backgroundColor: '#059669'
    },
    buttonDisabled: {
      backgroundColor: '#d1d5db',
      cursor: 'not-allowed',
      color: '#6b7280'
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '24px'
    },
    gridTwo: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '16px'
    },
    section: {
      marginBottom: '24px'
    },
    sectionTitle: {
      fontWeight: '600',
      color: '#374151',
      marginBottom: '8px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px'
    },
    infoCard: {
      backgroundColor: '#f9fafb',
      borderRadius: '8px',
      padding: '16px',
      fontSize: '0.9rem'
    },
    infoItem: {
      marginBottom: '8px'
    },
    infoLabel: {
      fontWeight: '500'
    },
    skillsContainer: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: '8px'
    },
    skill: {
      backgroundColor: '#dbeafe',
      color: '#1e40af',
      padding: '4px 8px',
      borderRadius: '4px',
      fontSize: '0.875rem'
    },
    experienceItem: {
      backgroundColor: '#f9fafb',
      borderRadius: '8px',
      padding: '16px',
      marginBottom: '16px'
    },
    expTitle: {
      fontWeight: '500',
      color: '#1f2937'
    },
    expCompany: {
      color: '#6b7280'
    },
    expDuration: {
      fontSize: '0.875rem',
      color: '#9ca3af'
    },
    formGroup: {
      marginBottom: '16px'
    },
    label: {
      display: 'block',
      fontSize: '0.875rem',
      fontWeight: '500',
      color: '#374151',
      marginBottom: '4px'
    },
    input: {
      width: '100%',
      padding: '8px 12px',
      border: '1px solid #d1d5db',
      borderRadius: '6px',
      fontSize: '1rem',
      transition: 'border-color 0.2s, box-shadow 0.2s',
      boxSizing: 'border-box'
    },
    inputFocus: {
      outline: 'none',
      borderColor: '#3b82f6',
      boxShadow: '0 0 0 3px rgba(59, 130, 246, 0.1)'
    },
    select: {
      width: '100%',
      padding: '8px 12px',
      border: '1px solid #d1d5db',
      borderRadius: '6px',
      fontSize: '1rem',
      backgroundColor: 'white',
      boxSizing: 'border-box'
    },
    textarea: {
      width: '100%',
      padding: '8px 12px',
      border: '1px solid #d1d5db',
      borderRadius: '6px',
      fontSize: '1rem',
      resize: 'none',
      fontFamily: 'inherit',
      boxSizing: 'border-box'
    },
    skillInput: {
      display: 'flex',
      gap: '8px',
      marginBottom: '8px'
    },
    skillInputField: {
      flex: 1,
      padding: '8px 12px',
      border: '1px solid #d1d5db',
      borderRadius: '6px',
      fontSize: '1rem'
    },
    addButton: {
      padding: '8px 16px',
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
      borderRadius: '6px',
      cursor: 'pointer',
      fontSize: '1rem'
    },
    skillTag: {
      backgroundColor: '#dbeafe',
      color: '#1e40af',
      padding: '6px 12px',
      borderRadius: '20px',
      fontSize: '0.875rem',
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      cursor: 'pointer',
      transition: 'background-color 0.2s'
    },
    skillTagHover: {
      backgroundColor: '#bfdbfe'
    },
    removeSkill: {
      color: '#3b82f6',
      fontWeight: 'bold',
      marginLeft: '4px'
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setMessage(null);
    } else {
      setMessage({ type: 'error', text: 'Please select a PDF file' });
    }
  };

  const parseResume = async () => {
    if (!resumeFile) {
      setMessage({ type: 'error', text: 'Please select a PDF file first' });
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', resumeFile);

    try {
      const response = await fetch(`${API_BASE}/parse_resume`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setParsedResume(data);
        setMessage({ type: 'success', text: 'Resume parsed successfully!' });
      } else {
        const error = await response.json();
        setMessage({ type: 'error', text: error.detail || 'Failed to parse resume' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const addSkill = () => {
    if (skillInput.trim() && !jobDescription.required_skills.includes(skillInput.trim())) {
      setJobDescription(prev => ({
        ...prev,
        required_skills: [...prev.required_skills, skillInput.trim()]
      }));
      setSkillInput('');
    }
  };

  const removeSkill = (skillToRemove) => {
    setJobDescription(prev => ({
      ...prev,
      required_skills: prev.required_skills.filter(skill => skill !== skillToRemove)
    }));
  };

  const saveJobDescription = async () => {
    if (!email) {
      setMessage({ type: 'error', text: 'Please enter your email' });
      return;
    }

    if (!jobDescription.job_title) {
      setMessage({ type: 'error', text: 'Please enter a job title' });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/save_jd/${email}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jobDescription),
      });

      if (response.ok) {
        setMessage({ type: 'success', text: 'Job description saved successfully!' });
        setJobDescription({
          job_title: '',
          company: '',
          location: '',
          job_type: '',
          description: '',
          required_skills: []
        });
      } else {
        const error = await response.json();
        setMessage({ type: 'error', text: error.detail || 'Failed to save job description' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.innerContainer}>
        {/* Header */}
        <div style={styles.header}>
          <h1 style={styles.headerTitle}>Resume Parser & Job Manager</h1>
          <p style={styles.headerSubtitle}>Parse resumes and manage job descriptions with AI-powered extraction</p>
        </div>

        {/* Message Alert */}
        {message && (
          <div style={{
            ...styles.message,
            ...(message.type === 'success' ? styles.messageSuccess : styles.messageError)
          }}>
            {message.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
            {message.text}
          </div>
        )}

        {/* Tab Navigation */}
        <div style={styles.tabContainer}>
          <div style={styles.tabNav}>
            <button
              onClick={() => setActiveTab('resume')}
              style={{
                ...styles.tabButton,
                ...(activeTab === 'resume' ? styles.tabButtonActive : styles.tabButtonInactive)
              }}
            >
              <FileText size={18} />
              Resume Parser
            </button>
            <button
              onClick={() => setActiveTab('job')}
              style={{
                ...styles.tabButton,
                ...(activeTab === 'job' ? styles.tabButtonActive : styles.tabButtonInactive)
              }}
            >
              <Briefcase size={18} />
              Job Description
            </button>
          </div>
        </div>

        {/* Resume Parser Tab */}
        {activeTab === 'resume' && (
          <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
            <div style={styles.card}>
              <h2 style={styles.cardTitle}>
                <Upload style={{ color: '#3b82f6' }} />
                Upload Resume
              </h2>
              
              <div style={styles.uploadArea}>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  style={styles.hiddenInput}
                  id="resume-upload"
                />
                <label htmlFor="resume-upload" style={{ cursor: 'pointer' }}>
                  <div style={styles.uploadContent}>
                    <FileText style={{ color: '#9ca3af', marginBottom: '16px' }} size={48} />
                    <p style={styles.uploadText}>Click to upload your resume (PDF only)</p>
                    <p style={styles.uploadSubtext}>Maximum file size: 10MB</p>
                  </div>
                </label>
                
                {resumeFile && (
                  <div style={styles.fileInfo}>
                    <p style={styles.fileInfoTitle}>{resumeFile.name}</p>
                    <p style={styles.fileInfoSize}>{(resumeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                )}
              </div>

              <button
                onClick={parseResume}
                disabled={!resumeFile || loading}
                style={{
                  ...styles.button,
                  ...((!resumeFile || loading) ? styles.buttonDisabled : styles.buttonPrimary)
                }}
              >
                {loading ? <Loader className="animate-spin" size={20} /> : <FileText size={20} />}
                {loading ? 'Parsing...' : 'Parse Resume'}
              </button>
            </div>

            {/* Parsed Resume Display */}
            {parsedResume && (
              <div style={styles.card}>
                <h3 style={{ ...styles.cardTitle, fontSize: '1.25rem' }}>Parsed Resume Data</h3>
                <div style={styles.grid}>
                  <div>
                    <h4 style={styles.sectionTitle}>
                      <User size={16} />
                      Personal Information
                    </h4>
                    <div style={styles.infoCard}>
                      <div style={styles.infoItem}>
                        <span style={styles.infoLabel}>Name:</span> {parsedResume.name || 'Not found'}
                      </div>
                      <div style={styles.infoItem}>
                        <span style={styles.infoLabel}>Email:</span> {parsedResume.email || 'Not found'}
                      </div>
                      <div style={styles.infoItem}>
                        <span style={styles.infoLabel}>Phone:</span> {parsedResume.phone || 'Not found'}
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 style={styles.sectionTitle}>Skills</h4>
                    <div style={styles.infoCard}>
                      {parsedResume.skills && parsedResume.skills.length > 0 ? (
                        <div style={styles.skillsContainer}>
                          {parsedResume.skills.map((skill, index) => (
                            <span key={index} style={styles.skill}>
                              {skill}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p style={{ color: '#6b7280' }}>No skills found</p>
                      )}
                    </div>
                  </div>
                </div>
                
                {parsedResume.experience && parsedResume.experience.length > 0 && (
                  <div style={styles.section}>
                    <h4 style={styles.sectionTitle}>Experience</h4>
                    <div>
                      {parsedResume.experience.map((exp, index) => (
                        <div key={index} style={styles.experienceItem}>
                          <h5 style={styles.expTitle}>{exp.title}</h5>
                          <p style={styles.expCompany}>{exp.company}</p>
                          <p style={styles.expDuration}>{exp.duration}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Job Description Tab */}
        {activeTab === 'job' && (
          <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <div style={styles.card}>
              <h2 style={styles.cardTitle}>
                <Briefcase style={{ color: '#3b82f6' }} />
                Job Description
              </h2>

              <div>
                {/* Email Input */}
                <div style={styles.formGroup}>
                  <label style={styles.label}>
                    <Mail size={16} style={{ display: 'inline', marginRight: '4px' }} />
                    Email *
                  </label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={styles.input}
                    placeholder="your@email.com"
                    required
                  />
                </div>

                {/* Job Title */}
                <div style={styles.formGroup}>
                  <label style={styles.label}>Job Title *</label>
                  <input
                    type="text"
                    value={jobDescription.job_title}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, job_title: e.target.value }))}
                    style={styles.input}
                    placeholder="Software Engineer, Product Manager, etc."
                    required
                  />
                </div>

                {/* Company */}
                <div style={styles.formGroup}>
                  <label style={styles.label}>Company</label>
                  <input
                    type="text"
                    value={jobDescription.company}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, company: e.target.value }))}
                    style={styles.input}
                    placeholder="Company name"
                  />
                </div>

                {/* Location and Job Type */}
                <div style={styles.gridTwo}>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>
                      <MapPin size={16} style={{ display: 'inline', marginRight: '4px' }} />
                      Location
                    </label>
                    <input
                      type="text"
                      value={jobDescription.location}
                      onChange={(e) => setJobDescription(prev => ({ ...prev, location: e.target.value }))}
                      style={styles.input}
                      placeholder="Remote, New York, etc."
                    />
                  </div>

                  <div style={styles.formGroup}>
                    <label style={styles.label}>
                      <Clock size={16} style={{ display: 'inline', marginRight: '4px' }} />
                      Job Type
                    </label>
                    <select
                      value={jobDescription.job_type}
                      onChange={(e) => setJobDescription(prev => ({ ...prev, job_type: e.target.value }))}
                      style={styles.select}
                    >
                      <option value="">Select type</option>
                      <option value="Full-time">Full-time</option>
                      <option value="Part-time">Part-time</option>
                      <option value="Contract">Contract</option>
                      <option value="Internship">Internship</option>
                    </select>
                  </div>
                </div>

                {/* Description */}
                <div style={styles.formGroup}>
                  <label style={styles.label}>Job Description</label>
                  <textarea
                    value={jobDescription.description}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, description: e.target.value }))}
                    rows={4}
                    style={styles.textarea}
                    placeholder="Describe the role, responsibilities, and requirements..."
                  />
                </div>

                {/* Skills */}
                <div style={styles.formGroup}>
                  <label style={styles.label}>Required Skills</label>
                  <div style={styles.skillInput}>
                    <input
                      type="text"
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && addSkill()}
                      style={styles.skillInputField}
                      placeholder="Add a skill and press Enter"
                    />
                    <button
                      type="button"
                      onClick={addSkill}
                      style={styles.addButton}
                    >
                      Add
                    </button>
                  </div>
                  
                  {jobDescription.required_skills.length > 0 && (
                    <div style={styles.skillsContainer}>
                      {jobDescription.required_skills.map((skill, index) => (
                        <span
                          key={index}
                          style={styles.skillTag}
                          onClick={() => removeSkill(skill)}
                        >
                          {skill}
                          <span style={styles.removeSkill}>×</span>
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Save Button */}
                <button
                  onClick={saveJobDescription}
                  disabled={loading}
                  style={{
                    ...styles.button,
                    ...(loading ? styles.buttonDisabled : styles.buttonSuccess)
                  }}
                >
                  {loading ? <Loader className="animate-spin" size={20} /> : <CheckCircle size={20} />}
                  {loading ? 'Saving...' : 'Save Job Description'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeParserApp;