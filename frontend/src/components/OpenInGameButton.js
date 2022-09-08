import React from "react";
import { Button } from "react-bootstrap";
import { postOpenChar } from "../apis/Dashboard";

export const OpenInGameButton = ({ character_id }) => {
  return (
    <Button
      bsStyle={"info"}
      onClick={() => {
        postOpenChar(character_id);
      }}
    >
      <i class="fas fa-external-link-alt"></i>
    </Button>
  );
};
