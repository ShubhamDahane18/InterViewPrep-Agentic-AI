

// import React, { useState } from 'react';
// import './App.css';

// const App = () => {
//   const [activeTab, setActiveTab] = useState('resume');
//   const [resumeFile, setResumeFile] = useState(null);
//   const [parsedResume, setParsedResume] = useState(null);
//   const [email, setEmail] = useState('');
//   const [jobDescription, setJobDescription] = useState({
//     job_title: '',
//     company: '',
//     location: '',
//     job_type: '',
//     description: '',
//     required_skills: []
//   });
//   const [skillInput, setSkillInput] = useState('');
//   const [loading, setLoading] = useState(false);
//   const [message, setMessage] = useState(null);
  
//   // Chat states
//   const [activeAgent, setActiveAgent] = useState('hr');
//   const [chatMessages, setChatMessages] = useState({
//     hr: [],
//     project: [],
//     tech: []
//   });
//   const [currentMessage, setCurrentMessage] = useState('');
//   const [chatLoading, setChatLoading] = useState(false);

//   const API_BASE = 'http://localhost:8000';

//   const handleFileUpload = (event) => {
//     const file = event.target.files[0];
//     if (file && file.type === 'application/pdf') {
//       setResumeFile(file);
//       setMessage(null);
//     } else {
//       setMessage({ type: 'error', text: 'Please select a PDF file' });
//     }
//   };

//   const parseResume = async () => {
//     if (!resumeFile) {
//       setMessage({ type: 'error', text: 'Please select a PDF file first' });
//       return;
//     }

//     setLoading(true);
//     const formData = new FormData();
//     formData.append('file', resumeFile);

//     try {
//       const response = await fetch(`${API_BASE}/parse_resume`, {
//         method: 'POST',
//         body: formData,
//       });

//       if (response.ok) {
//         const data = await response.json();
//         setParsedResume(data);
//         setMessage({ type: 'success', text: 'Resume parsed successfully!' });
//       } else {
//         const error = await response.json();
//         setMessage({ type: 'error', text: error.detail || 'Failed to parse resume' });
//       }
//     } catch (error) {
//       setMessage({ type: 'error', text: 'Network error. Please try again.' });
//     } finally {
//       setLoading(false);
//     }
//   };

//   const addSkill = () => {
//     if (skillInput.trim() && !jobDescription.required_skills.includes(skillInput.trim())) {
//       setJobDescription(prev => ({
//         ...prev,
//         required_skills: [...prev.required_skills, skillInput.trim()]
//       }));
//       setSkillInput('');
//     }
//   };

//   const removeSkill = (skillToRemove) => {
//     setJobDescription(prev => ({
//       ...prev,
//       required_skills: prev.required_skills.filter(skill => skill !== skillToRemove)
//     }));
//   };

//   const saveJobDescription = async () => {
//     if (!email) {
//       setMessage({ type: 'error', text: 'Please enter your email' });
//       return;
//     }

//     if (!jobDescription.job_title) {
//       setMessage({ type: 'error', text: 'Please enter a job title' });
//       return;
//     }

//     setLoading(true);
//     try {
//       const response = await fetch(`${API_BASE}/save_jd/${email}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(jobDescription),
//       });

//       if (response.ok) {
//         setMessage({ type: 'success', text: 'Job description saved successfully!' });
//         setJobDescription({
//           job_title: '',
//           company: '',
//           location: '',
//           job_type: '',
//           description: '',
//           required_skills: []
//         });
//       } else {
//         const error = await response.json();
//         setMessage({ type: 'error', text: error.detail || 'Failed to save job description' });
//       }
//     } catch (error) {
//       setMessage({ type: 'error', text: 'Network error. Please try again.' });
//     } finally {
//       setLoading(false);
//     }
//   };

//   const sendMessage = async () => {
//     if (!currentMessage.trim() || !email) {
//       setMessage({ type: 'error', text: 'Please enter your email and a message' });
//       return;
//     }

//     const userMessage = { type: 'user', content: currentMessage };
//     setChatMessages(prev => ({
//       ...prev,
//       [activeAgent]: [...prev[activeAgent], userMessage]
//     }));

//     setChatLoading(true);
//     const messageToSend = currentMessage;
//     setCurrentMessage('');

//     try {
//       const endpoint = `${API_BASE}/${activeAgent}-agent`;
//       const response = await fetch(endpoint, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           email: email,
//           user_input: messageToSend
//         }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         const botMessage = { type: 'bot', content: data };
//         setChatMessages(prev => ({
//           ...prev,
//           [activeAgent]: [...prev[activeAgent], botMessage]
//         }));
//       } else {
//         const error = await response.json();
//         setMessage({ type: 'error', text: error.detail || 'Failed to get response' });
//       }
//     } catch (error) {
//       setMessage({ type: 'error', text: 'Network error. Please try again.' });
//     } finally {
//       setChatLoading(false);
//     }
//   };

//   const handleKeyPress = (e) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       if (activeTab === 'chat') {
//         sendMessage();
//       } else {
//         addSkill();
//       }
//     }
//   };

//   return (
//     <div className="container">
//       <div className="inner-container">
//         {/* Header */}
//         <div className="header">
//           <h1 className="header-title">AI Interview Assistant</h1>
//           <p className="header-subtitle">Parse resumes, manage job descriptions, and conduct AI-powered interviews</p>
//         </div>

//         {/* Message Alert */}
//         {message && (
//           <div className={`message ${message.type === 'success' ? 'message-success' : 'message-error'}`}>
//             <span className="message-icon">
//               {message.type === 'success' ? '✓' : '⚠'}
//             </span>
//             {message.text}
//           </div>
//         )}

//         {/* Tab Navigation */}
//         <div className="tab-container">
//           <div className="tab-nav">
//             <button
//               onClick={() => setActiveTab('resume')}
//               className={`tab-button ${activeTab === 'resume' ? 'tab-button-active' : 'tab-button-inactive'}`}
//             >
//               📄 Resume Parser
//             </button>
//             <button
//               onClick={() => setActiveTab('job')}
//               className={`tab-button ${activeTab === 'job' ? 'tab-button-active' : 'tab-button-inactive'}`}
//             >
//               💼 Job Description
//             </button>
//             <button
//               onClick={() => setActiveTab('chat')}
//               className={`tab-button ${activeTab === 'chat' ? 'tab-button-active' : 'tab-button-inactive'}`}
//             >
//               🤖 AI Interview
//             </button>
//           </div>
//         </div>

//         {/* Resume Parser Tab */}
//         {activeTab === 'resume' && (
//           <div className="tab-content">
//             <div className="card">
//               <h2 className="card-title">
//                 📤 Upload Resume
//               </h2>
              
//               <div className="upload-area">
//                 <input
//                   type="file"
//                   accept=".pdf"
//                   onChange={handleFileUpload}
//                   className="hidden-input"
//                   id="resume-upload"
//                 />
//                 <label htmlFor="resume-upload" className="upload-label">
//                   <div className="upload-content">
//                     <div className="upload-icon">📄</div>
//                     <p className="upload-text">Click to upload your resume (PDF only)</p>
//                     <p className="upload-subtext">Maximum file size: 10MB</p>
//                   </div>
//                 </label>
                
//                 {resumeFile && (
//                   <div className="file-info">
//                     <p className="file-info-title">{resumeFile.name}</p>
//                     <p className="file-info-size">{(resumeFile.size / 1024 / 1024).toFixed(2)} MB</p>
//                   </div>
//                 )}
//               </div>

//               <button
//                 onClick={parseResume}
//                 disabled={!resumeFile || loading}
//                 className={`button ${(!resumeFile || loading) ? 'button-disabled' : 'button-primary'}`}
//               >
//                 {loading ? '⏳ Parsing...' : '🔍 Parse Resume'}
//               </button>
//             </div>

//             {/* Parsed Resume Display */}
//             {parsedResume && (
//               <div className="card">
//                 <h3 className="card-title">📋 Parsed Resume Data</h3>
//                 <div className="grid">
//                   <div>
//                     <h4 className="section-title">👤 Personal Information</h4>
//                     <div className="info-card">
//                       <div className="info-item">
//                         <span className="info-label">Name:</span> {parsedResume.name || 'Not found'}
//                       </div>
//                       <div className="info-item">
//                         <span className="info-label">Email:</span> {parsedResume.email || 'Not found'}
//                       </div>
//                       <div className="info-item">
//                         <span className="info-label">Phone:</span> {parsedResume.phone || 'Not found'}
//                       </div>
//                     </div>
//                   </div>
                  
//                   <div>
//                     <h4 className="section-title">🎯 Skills</h4>
//                     <div className="info-card">
//                       {parsedResume.skills && parsedResume.skills.length > 0 ? (
//                         <div className="skills-container">
//                           {parsedResume.skills.map((skill, index) => (
//                             <span key={index} className="skill">
//                               {skill}
//                             </span>
//                           ))}
//                         </div>
//                       ) : (
//                         <p className="no-data">No skills found</p>
//                       )}
//                     </div>
//                   </div>
//                 </div>
                
//                 {parsedResume.experience && parsedResume.experience.length > 0 && (
//                   <div className="section">
//                     <h4 className="section-title">💼 Experience</h4>
//                     <div>
//                       {parsedResume.experience.map((exp, index) => (
//                         <div key={index} className="experience-item">
//                           <h5 className="exp-title">{exp.title}</h5>
//                           <p className="exp-company">{exp.company}</p>
//                           <p className="exp-duration">{exp.duration}</p>
//                         </div>
//                       ))}
//                     </div>
//                   </div>
//                 )}
//               </div>
//             )}
//           </div>
//         )}

//         {/* Job Description Tab */}
//         {activeTab === 'job' && (
//           <div className="tab-content-centered">
//             <div className="card">
//               <h2 className="card-title">
//                 💼 Job Description
//               </h2>

//               <div>
//                 {/* Email Input */}
//                 <div className="form-group">
//                   <label className="label">📧 Email *</label>
//                   <input
//                     type="email"
//                     value={email}
//                     onChange={(e) => setEmail(e.target.value)}
//                     className="input"
//                     placeholder="your@email.com"
//                     required
//                   />
//                 </div>

//                 {/* Job Title */}
//                 <div className="form-group">
//                   <label className="label">Job Title *</label>
//                   <input
//                     type="text"
//                     value={jobDescription.job_title}
//                     onChange={(e) => setJobDescription(prev => ({ ...prev, job_title: e.target.value }))}
//                     className="input"
//                     placeholder="Software Engineer, Product Manager, etc."
//                     required
//                   />
//                 </div>

//                 {/* Company */}
//                 <div className="form-group">
//                   <label className="label">Company</label>
//                   <input
//                     type="text"
//                     value={jobDescription.company}
//                     onChange={(e) => setJobDescription(prev => ({ ...prev, company: e.target.value }))}
//                     className="input"
//                     placeholder="Company name"
//                   />
//                 </div>

//                 {/* Location and Job Type */}
//                 <div className="grid-two">
//                   <div className="form-group">
//                     <label className="label">📍 Location</label>
//                     <input
//                       type="text"
//                       value={jobDescription.location}
//                       onChange={(e) => setJobDescription(prev => ({ ...prev, location: e.target.value }))}
//                       className="input"
//                       placeholder="Remote, New York, etc."
//                     />
//                   </div>

//                   <div className="form-group">
//                     <label className="label">⏰ Job Type</label>
//                     <select
//                       value={jobDescription.job_type}
//                       onChange={(e) => setJobDescription(prev => ({ ...prev, job_type: e.target.value }))}
//                       className="select"
//                     >
//                       <option value="">Select type</option>
//                       <option value="Full-time">Full-time</option>
//                       <option value="Part-time">Part-time</option>
//                       <option value="Contract">Contract</option>
//                       <option value="Internship">Internship</option>
//                     </select>
//                   </div>
//                 </div>

//                 {/* Description */}
//                 <div className="form-group">
//                   <label className="label">Job Description</label>
//                   <textarea
//                     value={jobDescription.description}
//                     onChange={(e) => setJobDescription(prev => ({ ...prev, description: e.target.value }))}
//                     rows={4}
//                     className="textarea"
//                     placeholder="Describe the role, responsibilities, and requirements..."
//                   />
//                 </div>

//                 {/* Skills */}
//                 <div className="form-group">
//                   <label className="label">Required Skills</label>
//                   <div className="skill-input">
//                     <input
//                       type="text"
//                       value={skillInput}
//                       onChange={(e) => setSkillInput(e.target.value)}
//                       onKeyPress={handleKeyPress}
//                       className="skill-input-field"
//                       placeholder="Add a skill and press Enter"
//                     />
//                     <button
//                       type="button"
//                       onClick={addSkill}
//                       className="add-button"
//                     >
//                       Add
//                     </button>
//                   </div>
                  
//                   {jobDescription.required_skills.length > 0 && (
//                     <div className="skills-container">
//                       {jobDescription.required_skills.map((skill, index) => (
//                         <span
//                           key={index}
//                           className="skill-tag"
//                           onClick={() => removeSkill(skill)}
//                         >
//                           {skill}
//                           <span className="remove-skill">×</span>
//                         </span>
//                       ))}
//                     </div>
//                   )}
//                 </div>

//                 {/* Save Button */}
//                 <button
//                   onClick={saveJobDescription}
//                   disabled={loading}
//                   className={`button ${loading ? 'button-disabled' : 'button-success'}`}
//                 >
//                   {loading ? '⏳ Saving...' : '✅ Save Job Description'}
//                 </button>
//               </div>
//             </div>
//           </div>
//         )}

//         {/* AI Interview Tab */}
//         {activeTab === 'chat' && (
//           <div className="tab-content">
//             {/* Email Input for Chat */}
//             {!email && (
//               <div className="card">
//                 <h3 className="card-title">📧 Enter Your Email</h3>
//                 <div className="form-group">
//                   <input
//                     type="email"
//                     value={email}
//                     onChange={(e) => setEmail(e.target.value)}
//                     className="input"
//                     placeholder="your@email.com"
//                     required
//                   />
//                 </div>
//               </div>
//             )}

//             {email && (
//               <>
//                 {/* Agent Selection */}
//                 <div className="agent-selector">
//                   <h3 className="section-title">Choose Interview Agent</h3>
//                   <div className="agent-tabs">
//                     <button
//                       onClick={() => setActiveAgent('hr')}
//                       className={`agent-button ${activeAgent === 'hr' ? 'agent-button-active' : 'agent-button-inactive'}`}
//                     >
//                       👨‍💼 HR Agent
//                     </button>
//                     <button
//                       onClick={() => setActiveAgent('project')}
//                       className={`agent-button ${activeAgent === 'project' ? 'agent-button-active' : 'agent-button-inactive'}`}
//                     >
//                       📊 Project Agent
//                     </button>
//                     <button
//                       onClick={() => setActiveAgent('tech')}
//                       className={`agent-button ${activeAgent === 'tech' ? 'agent-button-active' : 'agent-button-inactive'}`}
//                     >
//                       🔧 Technical Agent
//                     </button>
//                   </div>
//                 </div>

//                 {/* Chat Interface */}
//                 <div className="chat-container">
//                   <div className="chat-messages">
//                     {chatMessages[activeAgent].length === 0 && (
//                       <div className="welcome-message">
//                         <h4>Welcome to the {activeAgent.toUpperCase()} Interview!</h4>
//                         <p>Ask me anything related to {activeAgent === 'hr' ? 'HR and behavioral questions' : activeAgent === 'project' ? 'project management and experience' : 'technical skills and coding'}.</p>
//                       </div>
//                     )}
                    
//                     {chatMessages[activeAgent].map((msg, index) => (
//                       <div key={index} className={`message-bubble ${msg.type === 'user' ? 'user-message' : 'bot-message'}`}>
//                         <div className="message-content">
//                           {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
//                         </div>
//                       </div>
//                     ))}
                    
//                     {chatLoading && (
//                       <div className="message-bubble bot-message">
//                         <div className="message-content">
//                           <div className="typing-indicator">
//                             <span></span>
//                             <span></span>
//                             <span></span>
//                           </div>
//                         </div>
//                       </div>
//                     )}
//                   </div>

//                   {/* Chat Input */}
//                   <div className="chat-input-container">
//                     <div className="chat-input">
//                       <textarea
//                         value={currentMessage}
//                         onChange={(e) => setCurrentMessage(e.target.value)}
//                         onKeyPress={handleKeyPress}
//                         className="chat-textarea"
//                         placeholder={`Ask the ${activeAgent} agent a question...`}
//                         rows={2}
//                         disabled={chatLoading}
//                       />
//                       <button
//                         onClick={sendMessage}
//                         disabled={!currentMessage.trim() || chatLoading}
//                         className={`send-button ${(!currentMessage.trim() || chatLoading) ? 'send-button-disabled' : 'send-button-active'}`}
//                       >
//                         {chatLoading ? '⏳' : '🚀'}
//                       </button>
//                     </div>
//                   </div>
//                 </div>
//               </>
//             )}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default App;




import React, { useState } from 'react';
import './App.css';

const App = () => {
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
  
  // Chat states
  const [activeAgent, setActiveAgent] = useState('hr');
  const [chatMessages, setChatMessages] = useState({
    hr: [],
    project: [],
    tech: []
  });
  const [currentMessage, setCurrentMessage] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  // Evaluation states
  const [evaluations, setEvaluations] = useState({
    hr: null,
    tech: null,
    project: null
  });
  const [evaluationLoading, setEvaluationLoading] = useState({
    hr: false,
    tech: false,
    project: false
  });

  const API_BASE = 'http://localhost:8000';

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

  const sendMessage = async () => {
    if (!currentMessage.trim() || !email) {
      setMessage({ type: 'error', text: 'Please enter your email and a message' });
      return;
    }

    const userMessage = { type: 'user', content: currentMessage };
    setChatMessages(prev => ({
      ...prev,
      [activeAgent]: [...prev[activeAgent], userMessage]
    }));

    setChatLoading(true);
    const messageToSend = currentMessage;
    setCurrentMessage('');

    try {
      const endpoint = `${API_BASE}/${activeAgent}-agent`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          user_input: messageToSend
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = { type: 'bot', content: data };
        setChatMessages(prev => ({
          ...prev,
          [activeAgent]: [...prev[activeAgent], botMessage]
        }));
      } else {
        const error = await response.json();
        setMessage({ type: 'error', text: error.detail || 'Failed to get response' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setChatLoading(false);
    }
  };

  const evaluateInterview = async (type) => {
    if (!email) {
      setMessage({ type: 'error', text: 'Please enter your email first' });
      return;
    }

    setEvaluationLoading(prev => ({ ...prev, [type]: true }));

    try {
      const endpoint = `${API_BASE}/${type}_evaluation/${email}`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setEvaluations(prev => ({ ...prev, [type]: data }));
        setMessage({ type: 'success', text: `${type.toUpperCase()} evaluation completed successfully!` });
      } else {
        const error = await response.json();
        setMessage({ type: 'error', text: error.detail || `Failed to evaluate ${type} interview` });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please try again.' });
    } finally {
      setEvaluationLoading(prev => ({ ...prev, [type]: false }));
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (activeTab === 'chat') {
        sendMessage();
      } else {
        addSkill();
      }
    }
  };

  return (
    <div className="container">
      <div className="inner-container">
        {/* Header */}
        <div className="header">
          <h1 className="header-title">AI Interview Assistant</h1>
          <p className="header-subtitle">Parse resumes, manage job descriptions, and conduct AI-powered interviews</p>
        </div>

        {/* Message Alert */}
        {message && (
          <div className={`message ${message.type === 'success' ? 'message-success' : 'message-error'}`}>
            <span className="message-icon">
              {message.type === 'success' ? '✓' : '⚠'}
            </span>
            {message.text}
          </div>
        )}

        {/* Tab Navigation */}
        <div className="tab-container">
          <div className="tab-nav">
            <button
              onClick={() => setActiveTab('resume')}
              className={`tab-button ${activeTab === 'resume' ? 'tab-button-active' : 'tab-button-inactive'}`}
            >
              📄 Resume Parser
            </button>
            <button
              onClick={() => setActiveTab('job')}
              className={`tab-button ${activeTab === 'job' ? 'tab-button-active' : 'tab-button-inactive'}`}
            >
              💼 Job Description
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`tab-button ${activeTab === 'chat' ? 'tab-button-active' : 'tab-button-inactive'}`}
            >
              🤖 AI Interview
            </button>
            <button
              onClick={() => setActiveTab('evaluation')}
              className={`tab-button ${activeTab === 'evaluation' ? 'tab-button-active' : 'tab-button-inactive'}`}
            >
              📊 Evaluation
            </button>
          </div>
        </div>

        {/* Resume Parser Tab */}
        {activeTab === 'resume' && (
          <div className="tab-content">
            <div className="card">
              <h2 className="card-title">
                📤 Upload Resume
              </h2>
              
              <div className="upload-area">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="hidden-input"
                  id="resume-upload"
                />
                <label htmlFor="resume-upload" className="upload-label">
                  <div className="upload-content">
                    <div className="upload-icon">📄</div>
                    <p className="upload-text">Click to upload your resume (PDF only)</p>
                    <p className="upload-subtext">Maximum file size: 10MB</p>
                  </div>
                </label>
                
                {resumeFile && (
                  <div className="file-info">
                    <p className="file-info-title">{resumeFile.name}</p>
                    <p className="file-info-size">{(resumeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                )}
              </div>

              <button
                onClick={parseResume}
                disabled={!resumeFile || loading}
                className={`button ${(!resumeFile || loading) ? 'button-disabled' : 'button-primary'}`}
              >
                {loading ? '⏳ Parsing...' : '🔍 Parse Resume'}
              </button>
            </div>

            {/* Parsed Resume Display */}
            {parsedResume && (
              <div className="card">
                <h3 className="card-title">📋 Parsed Resume Data</h3>
                <div className="grid">
                  <div>
                    <h4 className="section-title">👤 Personal Information</h4>
                    <div className="info-card">
                      <div className="info-item">
                        <span className="info-label">Name:</span> {parsedResume.name || 'Not found'}
                      </div>
                      <div className="info-item">
                        <span className="info-label">Email:</span> {parsedResume.email || 'Not found'}
                      </div>
                      <div className="info-item">
                        <span className="info-label">Phone:</span> {parsedResume.phone || 'Not found'}
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="section-title">🎯 Skills</h4>
                    <div className="info-card">
                      {parsedResume.skills && parsedResume.skills.length > 0 ? (
                        <div className="skills-container">
                          {parsedResume.skills.map((skill, index) => (
                            <span key={index} className="skill">
                              {skill}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="no-data">No skills found</p>
                      )}
                    </div>
                  </div>
                </div>
                
                {parsedResume.experience && parsedResume.experience.length > 0 && (
                  <div className="section">
                    <h4 className="section-title">💼 Experience</h4>
                    <div>
                      {parsedResume.experience.map((exp, index) => (
                        <div key={index} className="experience-item">
                          <h5 className="exp-title">{exp.title}</h5>
                          <p className="exp-company">{exp.company}</p>
                          <p className="exp-duration">{exp.duration}</p>
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
          <div className="tab-content-centered">
            <div className="card">
              <h2 className="card-title">
                💼 Job Description
              </h2>

              <div>
                {/* Email Input */}
                <div className="form-group">
                  <label className="label">📧 Email *</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input"
                    placeholder="your@email.com"
                    required
                  />
                </div>

                {/* Job Title */}
                <div className="form-group">
                  <label className="label">Job Title *</label>
                  <input
                    type="text"
                    value={jobDescription.job_title}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, job_title: e.target.value }))}
                    className="input"
                    placeholder="Software Engineer, Product Manager, etc."
                    required
                  />
                </div>

                {/* Company */}
                <div className="form-group">
                  <label className="label">Company</label>
                  <input
                    type="text"
                    value={jobDescription.company}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, company: e.target.value }))}
                    className="input"
                    placeholder="Company name"
                  />
                </div>

                {/* Location and Job Type */}
                <div className="grid-two">
                  <div className="form-group">
                    <label className="label">📍 Location</label>
                    <input
                      type="text"
                      value={jobDescription.location}
                      onChange={(e) => setJobDescription(prev => ({ ...prev, location: e.target.value }))}
                      className="input"
                      placeholder="Remote, New York, etc."
                    />
                  </div>

                  <div className="form-group">
                    <label className="label">⏰ Job Type</label>
                    <select
                      value={jobDescription.job_type}
                      onChange={(e) => setJobDescription(prev => ({ ...prev, job_type: e.target.value }))}
                      className="select"
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
                <div className="form-group">
                  <label className="label">Job Description</label>
                  <textarea
                    value={jobDescription.description}
                    onChange={(e) => setJobDescription(prev => ({ ...prev, description: e.target.value }))}
                    rows={4}
                    className="textarea"
                    placeholder="Describe the role, responsibilities, and requirements..."
                  />
                </div>

                {/* Skills */}
                <div className="form-group">
                  <label className="label">Required Skills</label>
                  <div className="skill-input">
                    <input
                      type="text"
                      value={skillInput}
                      onChange={(e) => setSkillInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      className="skill-input-field"
                      placeholder="Add a skill and press Enter"
                    />
                    <button
                      type="button"
                      onClick={addSkill}
                      className="add-button"
                    >
                      Add
                    </button>
                  </div>
                  
                  {jobDescription.required_skills.length > 0 && (
                    <div className="skills-container">
                      {jobDescription.required_skills.map((skill, index) => (
                        <span
                          key={index}
                          className="skill-tag"
                          onClick={() => removeSkill(skill)}
                        >
                          {skill}
                          <span className="remove-skill">×</span>
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Save Button */}
                <button
                  onClick={saveJobDescription}
                  disabled={loading}
                  className={`button ${loading ? 'button-disabled' : 'button-success'}`}
                >
                  {loading ? '⏳ Saving...' : '✅ Save Job Description'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* AI Interview Tab */}
        {activeTab === 'chat' && (
          <div className="tab-content">
            {/* Email Input for Chat */}
            {!email && (
              <div className="card">
                <h3 className="card-title">📧 Enter Your Email</h3>
                <div className="form-group">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input"
                    placeholder="your@email.com"
                    required
                  />
                </div>
              </div>
            )}

            {email && (
              <>
                {/* Agent Selection */}
                <div className="agent-selector">
                  <h3 className="section-title">Choose Interview Agent</h3>
                  <div className="agent-tabs">
                    <button
                      onClick={() => setActiveAgent('hr')}
                      className={`agent-button ${activeAgent === 'hr' ? 'agent-button-active' : 'agent-button-inactive'}`}
                    >
                      👨‍💼 HR Agent
                    </button>
                    <button
                      onClick={() => setActiveAgent('project')}
                      className={`agent-button ${activeAgent === 'project' ? 'agent-button-active' : 'agent-button-inactive'}`}
                    >
                      📊 Project Agent
                    </button>
                    <button
                      onClick={() => setActiveAgent('tech')}
                      className={`agent-button ${activeAgent === 'tech' ? 'agent-button-active' : 'agent-button-inactive'}`}
                    >
                      🔧 Technical Agent
                    </button>
                  </div>
                </div>

                {/* Chat Interface */}
                <div className="chat-container">
                  <div className="chat-messages">
                    {chatMessages[activeAgent].length === 0 && (
                      <div className="welcome-message">
                        <h4>Welcome to the {activeAgent.toUpperCase()} Interview!</h4>
                        <p>Ask me anything related to {activeAgent === 'hr' ? 'HR and behavioral questions' : activeAgent === 'project' ? 'project management and experience' : 'technical skills and coding'}.</p>
                      </div>
                    )}
                    
                    {chatMessages[activeAgent].map((msg, index) => (
                      <div key={index} className={`message-bubble ${msg.type === 'user' ? 'user-message' : 'bot-message'}`}>
                        <div className="message-content">
                          {typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content)}
                        </div>
                      </div>
                    ))}
                    
                    {chatLoading && (
                      <div className="message-bubble bot-message">
                        <div className="message-content">
                          <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Chat Input */}
                  <div className="chat-input-container">
                    <div className="chat-input">
                      <textarea
                        value={currentMessage}
                        onChange={(e) => setCurrentMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        className="chat-textarea"
                        placeholder={`Ask the ${activeAgent} agent a question...`}
                        rows={2}
                        disabled={chatLoading}
                      />
                      <button
                        onClick={sendMessage}
                        disabled={!currentMessage.trim() || chatLoading}
                        className={`send-button ${(!currentMessage.trim() || chatLoading) ? 'send-button-disabled' : 'send-button-active'}`}
                      >
                        {chatLoading ? '⏳' : '🚀'}
                      </button>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* Evaluation Tab */}
        {activeTab === 'evaluation' && (
          <div className="tab-content">
            {/* Email Input for Evaluation */}
            {!email && (
              <div className="card">
                <h3 className="card-title">📧 Enter Your Email</h3>
                <div className="form-group">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="input"
                    placeholder="your@email.com"
                    required
                  />
                </div>
              </div>
            )}

            {email && (
              <>
                {/* Evaluation Controls */}
                <div className="card">
                  <h2 className="card-title">📊 Interview Evaluations</h2>
                  <p className="card-subtitle">Generate comprehensive evaluations for each interview round</p>
                  
                  <div className="evaluation-controls">
                    <div className="evaluation-buttons">
                      <button
                        onClick={() => evaluateInterview('hr')}
                        disabled={evaluationLoading.hr}
                        className={`button ${evaluationLoading.hr ? 'button-disabled' : 'button-primary'}`}
                      >
                        {evaluationLoading.hr ? '⏳ Evaluating...' : '👨‍💼 Evaluate HR Round'}
                      </button>
                      
                      <button
                        onClick={() => evaluateInterview('tech')}
                        disabled={evaluationLoading.tech}
                        className={`button ${evaluationLoading.tech ? 'button-disabled' : 'button-primary'}`}
                      >
                        {evaluationLoading.tech ? '⏳ Evaluating...' : '🔧 Evaluate Technical Round'}
                      </button>
                      
                      <button
                        onClick={() => evaluateInterview('project')}
                        disabled={evaluationLoading.project}
                        className={`button ${evaluationLoading.project ? 'button-disabled' : 'button-primary'}`}
                      >
                        {evaluationLoading.project ? '⏳ Evaluating...' : '📊 Evaluate Project Round'}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Evaluation Results */}
                {(evaluations.hr || evaluations.tech || evaluations.project) && (
                  <div className="evaluation-results">
                    <h3 className="section-title">📋 Evaluation Results</h3>
                    
                    {evaluations.hr && (
                      <div className="card">
                        <h4 className="card-title">👨‍💼 HR Round Evaluation</h4>
                        <div className="evaluation-content">
                          <pre className="evaluation-text">
                            {typeof evaluations.hr === 'string' ? evaluations.hr : JSON.stringify(evaluations.hr, null, 2)}
                          </pre>
                        </div>
                      </div>
                    )}
                    
                    {evaluations.tech && (
                      <div className="card">
                        <h4 className="card-title">🔧 Technical Round Evaluation</h4>
                        <div className="evaluation-content">
                          <pre className="evaluation-text">
                            {typeof evaluations.tech === 'string' ? evaluations.tech : JSON.stringify(evaluations.tech, null, 2)}
                          </pre>
                        </div>
                      </div>
                    )}
                    
                    {evaluations.project && (
                      <div className="card">
                        <h4 className="card-title">📊 Project Round Evaluation</h4>
                        <div className="evaluation-content">
                          <pre className="evaluation-text">
                            {typeof evaluations.project === 'string' ? evaluations.project : JSON.stringify(evaluations.project, null, 2)}
                          </pre>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* No Evaluations Message */}
                {!evaluations.hr && !evaluations.tech && !evaluations.project && (
                  <div className="card">
                    <div className="no-evaluations">
                      <h4>🎯 Ready to Evaluate</h4>
                      <p>Click the buttons above to generate comprehensive evaluations for each interview round. Make sure you've completed some interview sessions first!</p>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;