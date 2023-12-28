import React from 'react';
import { AgGridReact } from 'ag-grid-react'; // React Grid Logic
import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme


const PriceChangeDataGrid = ({ data }) => {

  const colDefs = [
    { field: "Token Name" },
    { field: "Symbol" },
    { field: "Quote Rate" },
    { field: "Quote Rate 24h" },
    { field: "Percentage Change" },
  ];

  return (
    <div
      className="ag-theme-quartz-dark"
      style={{ width: "60%", height: "255px" }}
    >
      <AgGridReact rowData={data} columnDefs={colDefs} />
    </div>
  );
};

export default PriceChangeDataGrid;
// ['Token Name', 'Symbol', 'Quote Rate', 'Quote Rate 24h', 'Percentage Change']