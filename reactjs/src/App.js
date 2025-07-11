// src/App.js
import React, { useState } from "react";
import LeftPanel from "./components/LeftPanel/LeftPanel";
import MiddlePanel from "./components/MiddlePanel/MiddlePanel";
import RightPanel from "./components/RightPanel/RightPanel";
import "./App.css";

function App() {
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [selectedLoanType, setSelectedLoanType] = useState(null);
  const [selectedDocumentContent, setSelectedDocumentContent] = useState(null);



  return (
    <div className="App">
      <div className="main-layout">
        {/* Truyền hàm setSelectedCustomer xuống LeftPanel */}
        <LeftPanel
          onSelectCustomer={setSelectedCustomer}
          onSelectLoanType={(loanType) => {
            setSelectedLoanType(loanType);
            setSelectedDocumentContent(null); // Reset khi chọn loại hồ sơ
          }}
        />


        <MiddlePanel
          selectedLoanType={selectedLoanType}
          selectedDocumentContent={selectedDocumentContent}
          selectedCustomer={selectedCustomer}
        />

        {/* Truyền selectedCustomer sang RightPanel */}
        <RightPanel
          selectedCustomer={selectedCustomer}
          onSelectDocument={(doc) => setSelectedDocumentContent(doc?.Document_Content || "")}
        />
      </div>
    </div>
  );
}


export default App;
