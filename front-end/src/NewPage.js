// import React, { useState, useEffect } from 'react';
// import axios from "axios";
// import './NewPage.css'; 
// import CameraView from './CameraView'; 

// function NewPage() {
//   const [selectedLevel, setSelectedLevel] = useState('');
//   const [cameraStream, setCameraStream] = useState(null);
//   const [isCameraPopupVisible, setIsCameraPopupVisible] = useState(false);

//   const levels = [
//     { value: 'road', label: 'ROAD' },
//     { value: 'public', label: 'PUBLIC' },
//     { value: 'domestic', label: 'DOMESTIC' },
//   ];

//   const items = {
//     road: ['Accident', 'Fire'],
//     public: ['Weapon', 'Fire'],
//     domestic: ['Human', 'Fire','Weapon'],
//   };

//   const handleChange = (event) => {
//     setSelectedLevel(event.target.value);
//   };

//   const handleLaunch = async () => {
//     if (selectedLevel) {
//       try {
//         const stream = await navigator.mediaDevices.getUserMedia({ video: true });
//         setCameraStream(stream);
//         console.log("Camera stream:", stream);
//         setIsCameraPopupVisible(true); 
//       } catch (error) {
//         console.error("Error accessing camera:", error);
//         alert('Camera access is not supported or denied.');
//       }
//     } else {
//       alert('Please select a plan before launching.');
//     }
//   };

  
//   useEffect(() => {
//     return () => {
//       if (cameraStream) {
//         cameraStream.getTracks().forEach((track) => track.stop());
//         setCameraStream(null);
//         setIsCameraPopupVisible(false); 
//       }
//     };
//   }, [cameraStream]);

//   return (
//     <div className="new-page">
//       <h1 className="head">ENVIRONMENT SETUP</h1>
//       <form className="check">
//         <div className="radio-container">
//           {levels.map((level) => (
//             <div key={level.value} className="radio-box">
//               <input
//                 type="radio"
//                 id={level.value}
//                 value={level.value}
//                 checked={selectedLevel === level.value}
//                 onChange={handleChange}
//                 className="radio-input"
//               />
//               <label htmlFor={level.value} className="radio-label">
//                 {level.label}
//               </label>
//               <div className="features">
//                 <h3>Detects: </h3>
//                 {items[level.value].map((item) => (
//                   <span key={item} className="feature">
//                     {item}
//                   </span>
//                 ))}
//               </div>
//             </div>
//           ))}
//         </div>
//       </form>
//       <button className="setup" onClick={handleLaunch}>
//         LAUNCH
//       </button>
//       {isCameraPopupVisible && <CameraView cameraStream={cameraStream} />}
//     </div>
//   );
// }

// export default NewPage;


import React from 'react';
import axios from 'axios';

function App() {
  const runScript = (script) => {
    axios.get(`http://localhost:5000/${script}`)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <button onClick={() => runScript('road')}>Road</button>
      <button onClick={() => runScript('public')}>Public</button>
      <button onClick={() => runScript('domestic')}>Domestic</button>
    </div>
  );
}

export default App;
