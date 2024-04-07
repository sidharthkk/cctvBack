import React, { useState, useEffect } from 'react';

function CameraView({ cameraStream }) {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
    console.log("isVisible after toggle:", isVisible); // Log state for debugging
  };

  useEffect(() => {
    console.log("cameraStream:", cameraStream); // Log stream availability for debugging
  }, [cameraStream]);

  return (
    <div className="camera-popup" style={{ display: isVisible ? 'block' : 'none' }}>
      <button onClick={toggleVisibility}>Close</button>
      {cameraStream && (
        <video autoPlay muted width={320} height={240} srcObject={cameraStream} />
      )}
    </div>
  );
}

export default CameraView;
