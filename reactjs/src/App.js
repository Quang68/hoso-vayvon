// src/App.js
import React, { useState } from "react";
import LeftPanel from "./components/LeftPanel/LeftPanel";
import MiddlePanel from "./components/MiddlePanel/MiddlePanel";
import RightPanel from "./components/RightPanel/RightPanel";
import "./App.css";

function App() {
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  const handleCreateNewCustomer = () => {
    alert("👉 Chức năng tạo khách hàng mới sẽ xử lý tại đây!");
  };

  return (
    <div className="App">
      <div className="main-layout">
        <LeftPanel onCreateNewCustomer={handleCreateNewCustomer} />
        <MiddlePanel />
        <RightPanel selectedCustomer={selectedCustomer} />
      </div>
    </div>
  );
}


export default App;
