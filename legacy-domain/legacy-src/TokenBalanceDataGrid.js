import React from 'react';
import { AgGridReact } from 'ag-grid-react'; // React Grid Logic
import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme

const TokenBalanceTreeDataGrid = ({ data }) => {

  const colDefs = [
    { field: "Token Name" },
    { field: "Symbol" },
    { field: "Balance" },
    { field: "Value (USD)" },
  ];

  return (
    <div
      className="ag-theme-quartz-dark"
      style={{ width: "44%", height: "255px" }}
    >
      <AgGridReact rowData={ data } columnDefs={colDefs} />
    </div>
  );
};

export default TokenBalanceTreeDataGrid;
