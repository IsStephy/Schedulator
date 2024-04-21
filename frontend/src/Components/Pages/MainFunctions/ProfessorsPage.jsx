import React, { useEffect, useState } from 'react';
import Sidebar from '../Sidebar';
import "./MainFunctions.css";

function ProfessorsPage() {
  const [teachers, setTeachers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/professors', { method: 'GET', credentials: 'include' })
      .then(response => response.json())
      .then(data => setTeachers(data.teachers))
      .catch(error => console.error('Error fetching teacher data:', error));
  }, []);

  const filteredTeachers = teachers.filter(teacher =>
    teacher.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className='app_container'>
      <Sidebar />
      <div className='content_wrapper'>
    <div className='search-container'>
      <input
        type="text"
        placeholder="Search by professor name..."
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}
        className='search-box'
      />
    </div>
    <div className='display_box'>
        <table className='list_table'>
          <thead>
            <tr>
              <th>ID</th>
              <th>Professor</th>
              <th>Courses</th>
              <th>Language</th>
            </tr>
          </thead>
          <tbody>
            {filteredTeachers.map((teacher, index) => (
              <tr key={teacher.id}>
                <td>{index + 1}</td>
                <td>{teacher.name}</td>
                <td className='courses'>{teacher.courses.map(course => (
                  <span key={course}>{course}, </span>
                ))}</td>
                <td>{teacher.language}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
    </div>
  );
}

export default ProfessorsPage;
