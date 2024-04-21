import React, {useState, useEffect} from 'react'
import Sidebar from '../Sidebar'



function CoursesPage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/data') // Replace '/api/data' with your actual API endpoint
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return(
    <div>
      <Sidebar />
      <div className="dataDisplay">
        {data.map}
      </div>
    </div>
  )
}

export default CoursesPage