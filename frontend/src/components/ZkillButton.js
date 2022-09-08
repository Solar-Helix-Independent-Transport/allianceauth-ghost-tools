import React from "react";
import { Button } from "react-bootstrap";

export const ZkillButton = ({ character_name }) => {
  return (
    <Button
      target="_blank"
      rel="noopener noreferrer"
      alt="zKillboard"
      href={`https://zkillboard.com/search/${character_name}/`}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="13.5"
        width="15"
        viewBox="0 0 32 21"
      >
        <polygon
          points="1,7 31,7 16,21"
          style={{
            fill: "currentColor",
            stroke: "currentColor",
            strokeWidth: 2,
          }}
        />
        <polygon
          points="1,2 31,2"
          style={{
            fill: "currentColor",
            stroke: "currentColor",
            strokeWidth: 2,
          }}
        />
      </svg>
    </Button>
  );
};
