import React, { useState } from "react";
import { Panel, Checkbox } from "react-bootstrap";
import { useQuery } from "react-query";
import { loadDash } from "../apis/Dashboard";
import { PanelLoader } from "./PanelLoader";
import { BaseTable, textColumnFilter, SelectColumnFilter } from "./BaseTable";
import { ErrorLoader } from "./ErrorLoader";
import ReactTimeAgo from "react-time-ago";
import { StagingSelect } from "./StagingFilters";
import { OpenCharacterButtonGroup } from "./OpenCharacterButtonGroup";

export const Dashboard = () => {
  const { isLoading, error, data, isFetching } = useQuery(
    ["dashboard"],
    () => loadDash(),
    {
      refetchOnWindowFocus: false,
    },
  );
  const [orphans, setOrphans] = useState(false);
  const [stagings, setStagings] = useState([]);

  const columns = React.useMemo(
    () => [
      {
        Header: "Character",
        accessor: "char.name",
        Filter: textColumnFilter,
        filter: "text",
        Cell: (props) => (
          <OpenCharacterButtonGroup
            character_id={props.row.original.char.id}
            character_name={props.value}
          />
        ),
      },
      {
        Header: "Main",
        accessor: "main.name",
        Filter: textColumnFilter,
        filter: "text",
        Cell: (props) => (
          <OpenCharacterButtonGroup
            character_id={props.row.original.main.id}
            character_name={props.value}
          />
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
        Header: "Alliance",
        accessor: "main.alli",
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
          <div style={{ whiteSpace: "nowrap" }}>
            {props.value ? (
              <ReactTimeAgo date={Date.parse(props.value)} />
            ) : (
              <></>
            )}
          </div>
        ),
      },
      {
        Header: "Join Date",
        accessor: "start_date",
        Cell: (props) => (
          <div style={{ whiteSpace: "nowrap" }}>
            {props.value ? (
              <ReactTimeAgo date={Date.parse(props.value)} />
            ) : (
              <></>
            )}
          </div>
        ),
      },
    ],
    [],
  );

  if (isLoading) return <PanelLoader />;

  if (error) return <ErrorLoader />;

  let graphData = data.characters;

  if (stagings.length > 0) {
    graphData = graphData.filter((row) => {
      return !stagings.includes(row.location.name);
    });
  }

  if (orphans) {
    graphData = graphData.filter((row) => {
      return !data.alliances.includes(row.main.alli_id);
    });
  }

  return (
    <Panel.Body>
      <div class={"col-xs-12"} style={{ display: "flex" }}>
        <div style={{ flexGrow: 1 }}>
          <StagingSelect
            data={data.stagings}
            setFilter={setStagings}
            labelText="Staging Filter"
            {...{ isFetching }}
          />
        </div>
        <Checkbox
          onChange={(e) => {
            setOrphans(e.target.checked);
          }}
        >
          Orphans Only
        </Checkbox>
      </div>
      <BaseTable
        data={graphData}
        {...{ isLoading, columns, error, isFetching }}
      />
    </Panel.Body>
  );
};
