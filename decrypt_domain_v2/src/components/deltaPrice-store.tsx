import React from 'react';
import { AgGridReact } from 'ag-grid-react'; 
import "ag-grid-community/styles/ag-grid.css"; 
import "ag-grid-community/styles/ag-theme-quartz.css";
import { ColDef } from 'ag-grid-community';

export interface PriceRowData {
  'Token Name': string;
  Symbol: string;
  'Quote Rate': string;
  'Quote Rate 24h': string;
  'Percentage Change': string;
}

export interface PriceProps {
  data: PriceRowData[]
}

const DeltaPrice: React.FC<PriceProps> = ({ data }) => {

  const colDefs: ColDef[] = [
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
      <AgGridReact<PriceRowData> rowData={data} columnDefs={colDefs} />
    </div>
  );
};

export default DeltaPrice;
// ['Token Name', 'Symbol', 'Quote Rate', 'Quote Rate 24h', 'Percentage Change']