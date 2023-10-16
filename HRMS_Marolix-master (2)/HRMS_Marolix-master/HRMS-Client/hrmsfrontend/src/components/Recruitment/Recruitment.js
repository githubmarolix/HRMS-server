import React, { useState, useEffect } from 'react';
import './Recruitment.css';

const Recruitment = () => {
  const [showForm, setShowForm] = useState(false);
  const [jobDetails, setJobDetails] = useState({
    role: '',
    responsibilities: '',
    qualifications: '',
    experience: '',
    jobPostingDate: '',
  });
  const [postedJobs, setPostedJobs] = useState([]);

  const handlePostJobClick = () => {
    setShowForm(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setJobDetails((prevJobDetails) => ({
      ...prevJobDetails,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Perform form submission logic or API call to post the job
    fetch('http://127.0.0.1:8000/recruitment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobDetails),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Job posted successfully:', data);
        // Reset the form
        setJobDetails({
          role: '',
          responsibilities: '',
          qualifications: '',
          experience: '',
          jobPostingDate: '',
        });
        setShowForm(false);
      })
      .catch((error) => {
        console.error('Error posting job:', error);
      });
  };

  const handleViewAllJobsClick = () => {
    // Fetch all posted jobs
    fetch('http://127.0.0.1:8000/viewAllJobs/')
      .then((response) => response.json())
      .then((data) => {
        console.log('Posted jobs:', data);
        setPostedJobs(data.data);
      })
      .catch((error) => {
        console.error('Error fetching posted jobs:', error);
      });
  };

  return (
    <div className="button-container">
      {!showForm && !postedJobs.length && (
        <button className="recruitment-button" onClick={handlePostJobClick}>
          Post a Job
        </button>
      )}

      {showForm ? (
        <form className="job-form" onSubmit={handleSubmit}>
          <h1>POST A JOB</h1>
          <label htmlFor="role">Role:</label>
          <input
            type="text"
            id="role"
            name="role"
            value={jobDetails.role}
            onChange={handleInputChange}
            required
          />

          <label htmlFor="responsibilities">Responsibilities:</label>
          <textarea
            id="responsibilities"
            name="responsibilities"
            value={jobDetails.responsibilities}
            onChange={handleInputChange}
            required
          ></textarea>

          <label htmlFor="qualifications">Qualifications:</label>
          <textarea
            id="qualifications"
            name="qualifications"
            value={jobDetails.qualifications}
            onChange={handleInputChange}
            required
          ></textarea>

          <label htmlFor="experience">Experience:</label>
          <input
            type="number"
            id="experience"
            name="experience"
            value={jobDetails.experience}
            onChange={handleInputChange}
            required
          />

          <button type="submit" className="recruitment-button">
            Submit
          </button>
        </form>
      ) : null}

      {!showForm && !postedJobs.length && (
        <button className="recruitment-button" onClick={handleViewAllJobsClick}>
          View All Posted Jobs
        </button>
      )}

      {!showForm && postedJobs.length > 0 && (
        <div className="job-list">
          <table className="job-table">
            <thead>
              <tr>
                <th>Designation</th>
                <th>Responsibilities</th>
                <th>Qualifications</th>
                <th>Experience</th>
                <th>Date Of Posting</th>
                <th>View Application Page</th>
              </tr>
            </thead>
            <tbody>
              {postedJobs.map((job) => (
                <tr key={job.pk} className="job-item">
                  <td>{job.fields.designation}</td>
                  <td>{job.fields.responsibilities}</td>
                  <td>{job.fields.qualifications}</td>
                  <td>{job.fields.experience} years</td>
                  <td>{job.fields.jobPostingDate}</td>
                  <td>
                    <button className="AppPageLink">Go to Application Page</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!showForm && !postedJobs.length && (
        <>
          <button className="recruitment-button">Applied Candidates</button>
          <button className="recruitment-button">Accepted Candidates</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
          <button className="recruitment-button">?</button>
        </>
      )}
    </div>
  );
};

export default Recruitment;

