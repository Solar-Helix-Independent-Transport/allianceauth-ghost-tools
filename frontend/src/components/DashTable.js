import React from "react";
import { Panel, Label } from "react-bootstrap";
import { useQuery } from "react-query";
import { loadDash } from "../apis/Dashboard";
import { PanelLoader } from "./PanelLoader";
import { BaseTable, textColumnFilter, SelectColumnFilter } from "./BaseTable";
import Select from "react-select";
import { ErrorLoader } from "./ErrorLoader";

export const Dashboard = () => {
  const { isLoading, error, data, isFetching } = useQuery(["dashboard"], () =>
    loadDash(),
  );

  const columns = React.useMemo(
    () => [
      {
        Header: "Character",
        accessor: "char.name",
        Filter: textColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Main",
        accessor: "main.name",
        Filter: textColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Corp",
        accessor: "main.corp",
        Filter: SelectColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Location",
        accessor: "location.name",
        Filter: SelectColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Ship",
        accessor: "ship.name",
        Filter: SelectColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Death Clone",
        accessor: "death_clone.name",
        Filter: SelectColumnFilter,
        filter: "text",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      {
        Header: "Last Online",
        accessor: "logoff_date",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
      ,
      {
        Header: "Join Date",
        accessor: "start_date",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>{props.value}</div>
        ),
      },
    ],
    [],
  );

  if (isLoading) return <PanelLoader />;

  if (error) return <ErrorLoader />;

  return (
    <Panel.Body>
      <BaseTable {...{ isLoading, data, columns, error, isFetching }} />
    </Panel.Body>
  );
};
