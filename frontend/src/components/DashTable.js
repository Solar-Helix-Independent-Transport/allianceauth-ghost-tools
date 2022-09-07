import React, { useState } from "react";
import { Panel, Checkbox, Button, ButtonGroup } from "react-bootstrap";
import { useQuery } from "react-query";
import { loadDash, postOpenChar } from "../apis/Dashboard";
import { PanelLoader } from "./PanelLoader";
import { BaseTable, textColumnFilter, SelectColumnFilter } from "./BaseTable";
import Select from "react-select";
import { ErrorLoader } from "./ErrorLoader";
import ReactTimeAgo from "react-time-ago";
import { StagingSelect } from "./StagingFilters";

export const Dashboard = () => {
  const { isLoading, error, data, isFetching } = useQuery(["dashboard"], () =>
    loadDash(),
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
          <div>
            <ButtonGroup style={{ display: "flex" }}>
              <Button
                bsStyle={"info"}
                onClick={() => {
                  postOpenChar(props.row.original.char.id);
                }}
              >
                <i class="fas fa-external-link-alt"></i>
              </Button>
              <Button
                target="_blank"
                rel="noopener noreferrer"
                href={`https://zkillboard.com/search/${props.value}/`}
              >
                {props.value}{" "}
              </Button>
            </ButtonGroup>
          </div>
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
      <StagingSelect
        data={data.stagings}
        setFilter={setStagings}
        labelText="Staging Filter"
        {...{ isFetching }}
      />
      <Checkbox
        onChange={(e) => {
          setOrphans(e.target.checked);
        }}
      >
        Orphans Only
      </Checkbox>

      <BaseTable
        data={graphData}
        {...{ isLoading, columns, error, isFetching }}
      />
    </Panel.Body>
  );
};
