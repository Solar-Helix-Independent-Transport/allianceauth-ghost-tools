import React from "react";
import { Button } from "react-bootstrap";

export const EveWhoButton = ({ character_id }) => {
  return (
    <Button
      target="_blank"
      rel="noopener noreferrer"
      alt="Eve Who"
      href={`https://evewho.com/character/${character_id}/`}
    >
      <i class="fas fa-user"></i>
    </Button>
  );
};
