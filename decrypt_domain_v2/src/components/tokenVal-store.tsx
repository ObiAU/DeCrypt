import React from 'react';
import { AgGridReact } from 'ag-grid-react'; // React Grid Logic
import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-quartz.css"; // Theme
import { ColDef } from 'ag-grid-community';

export interface TokenRowData {
  'Token Name': string;
  Symbol: string;
  Balance: string;
  'Value (USD)': string;

}

// component props
export interface TokenBalanceProps {
  data: TokenRowData[]
}

const TokenStore: React.FC<TokenBalanceProps> = ({ data }) => {

  const colDefs: ColDef[] = [
    { field: "Token Name" },
    { field: "Symbol" },
    { field: "Balance" },
    { field: "Value (USD)" },
  ];

  return (
    <div
      className="ag-theme-quartz-dark"
      style={{ width: "100%", height: "255px" }}
    >
      <AgGridReact<TokenRowData> rowData={ data } columnDefs={colDefs} />
    </div>
  );
};

export default TokenStore;
