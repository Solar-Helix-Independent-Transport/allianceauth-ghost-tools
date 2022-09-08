import React from "react";
import { Button, ButtonGroup } from "react-bootstrap";
import { OpenInGameButton } from "./OpenInGameButton";
import { ZkillButton } from "./ZkillButton";
import { EveWhoButton } from "./EveWhoButton";

export const OpenCharacterButtonGroup = ({ character_id, character_name }) => {
  return (
    <ButtonGroup style={{ display: "flex" }}>
      <OpenInGameButton {...{ character_id }} />
      <Button>{character_name}</Button>
      <ZkillButton {...{ character_name }} />
      <EveWhoButton {...{ character_id }} />
    </ButtonGroup>
  );
};
