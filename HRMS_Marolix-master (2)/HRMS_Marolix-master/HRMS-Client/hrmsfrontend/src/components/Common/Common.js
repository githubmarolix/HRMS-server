import React, { useState, useEffect } from 'react';
import './styles.css';
import Recruitment from '../Recruitment/Recruitment';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">Company Name</div>
      <ul className="nav-links">
        <li><a href="#">About</a></li>
        <li><a href="#">Blogs</a></li>
        <li><a href="#">Contact Us</a></li>
      </ul>
      <TimerButton />
      <button className="logout-button">Logout</button>
    </nav>
  );
};

const Sidebar = ({ handleLinkClick }) => {
  return (
    <aside className="sidebar">
      <ul className="sidebar-links">
        <li><a href="#" onClick={() => handleLinkClick('recruitment')}>Recruitment</a></li>
        <li><a href="#" onClick={() => handleLinkClick('onboarding')}>Onboarding</a></li>
        <li><a href="#" onClick={() => handleLinkClick('attendance')}>Attendance</a></li>
        <li><a href="#" onClick={() => handleLinkClick('leave-management')}>Leave Management</a></li>
        <li><a href="#" onClick={() => handleLinkClick('payroll-management')}>Payroll Management</a></li>
        <li><a href="#" onClick={() => handleLinkClick('employee-information')}>Employee Information</a></li>
        <li><a href="#" onClick={() => handleLinkClick('employee-directory')}>Employee Directory</a></li>
      </ul>
    </aside>
  );
};

const Footer = () => {
  return (
    <footer className="footer">
      <p>© {new Date().getFullYear()} All Rights Reserved</p>
    </footer>
  );
};

const TimerButton = () => {
  const [timerRunning, setTimerRunning] = useState(false);
  const [timerValue, setTimerValue] = useState(0);

  useEffect(() => {
    let interval;
    if (timerRunning) {
      interval = setInterval(() => {
        setTimerValue(prevValue => prevValue + 1);
      }, 1000);
    } else {
      clearInterval(interval);
      stopTimer();
    }

    return () => clearInterval(interval);
  }, [timerRunning]);

  const formatTime = (time) => {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = Math.floor(time % 60);

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const startTimer = async () => {
    try {
      const response = await fetch('http://localhost:8000/startTimer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        console.log('Timer started');
      } else {
        console.error('Failed to start timer');
      }
    } catch (error) {
      console.error('Error occurred while starting timer', error);
    }
  };

  const stopTimer = async () => {
    try {
      const response = await fetch('http://localhost:8000/stopTimer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        console.log('Timer stopped');
      } else {
        console.error('Failed to stop timer');
      }
    } catch (error) {
      console.error('Error occurred while stopping timer', error);
    }
  };

  const handleTimerClick = () => {
    if (timerRunning) {
      setTimerRunning(false);
    } else {
      setTimerRunning(true);
      startTimer();
    }
  };

  return (
    <button className="timer-button" onClick={handleTimerClick}>
      {timerRunning ? 'Stop Timer' : 'Start Timer'}
      <span className="timer-value">{formatTime(timerValue)}</span>
    </button>
  );
};

const Common = () => {
  const [activeLink, setActiveLink] = useState(null);

  const handleLinkClick = (link) => {
    setActiveLink(link);
  };

  const renderContent = () => {
    switch (activeLink) {
      case 'recruitment':
        return <Recruitment />;
      // Add other case statements for different pages/components
      default:
        return null;
    }
  };

  return (
    <div className="container">
      <Navbar />
      <div className="content">
        <Sidebar handleLinkClick={handleLinkClick} />
        {renderContent()}
      </div>
      <Footer />
    </div>
  );
};

export default Common;
